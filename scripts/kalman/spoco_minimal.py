# spoco_minimal.py
# Python 3.10+, PyTorch 2.x
from typing import Dict, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F


# ----------------------------
# 1) Tiny U-Net-ish embedding net
# ----------------------------
class DoubleConv(nn.Module):
    def __init__(self, c_in, c_out):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(c_in, c_out, 3, padding=1),
            nn.GroupNorm(8, c_out),
            nn.ReLU(inplace=True),
            nn.Conv2d(c_out, c_out, 3, padding=1),
            nn.GroupNorm(8, c_out),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.net(x)


class Down(nn.Module):
    def __init__(self, c_in, c_out):
        super().__init__()
        self.net = nn.Sequential(nn.MaxPool2d(2), DoubleConv(c_in, c_out))

    def forward(self, x):
        return self.net(x)


class Up(nn.Module):
    def __init__(self, c_in, c_out):
        super().__init__()
        self.up = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=False)
        self.conv = DoubleConv(c_in, c_out)

    def forward(self, x1, x2):
        x1 = self.up(x1)
        # pad if needed
        dy, dx = x2.size(-2) - x1.size(-2), x2.size(-1) - x1.size(-1)
        x1 = F.pad(x1, (dx // 2, dx - dx // 2, dy // 2, dy - dy // 2))
        return self.conv(torch.cat([x2, x1], dim=1))


class PixelEmbeddingNet(nn.Module):
    def __init__(self, emb_dim=16):
        super().__init__()
        self.inc = DoubleConv(3, 32)
        self.d1 = Down(32, 64)
        self.d2 = Down(64, 128)
        self.u1 = Up(128 + 64, 64)
        self.u2 = Up(64 + 32, 32)
        self.head = nn.Conv2d(32, emb_dim, 1)

    def forward(self, x):
        x0 = self.inc(x)  # B,32,H,W
        x1 = self.d1(x0)  # B,64,H/2,W/2
        x2 = self.d2(x1)  # B,128,H/4,W/4
        z = self.u1(x2, x1)  # B,64,H/2,W/2
        z = self.u2(z, x0)  # B,32,H,W
        emb = self.head(z)  # B,D,H,W
        # L2-normalize embeddings (common in metric learning)
        return F.normalize(emb, dim=1)


# ---------------------------------------------
# 2) Sparse instance loss (pull/push in embedding space)
#    - labels: int32 map with 0 for background/unlabeled, >0 for instance IDs
#    - mask_labeled: bool map where True indicates pixels belonging to a FEW annotated instances
#    Strategy:
#      * sample K pixels per annotated instance (anchors)
#      * pull: same-instance pairs close
#      * push: different-instance pairs far (margin)
# ---------------------------------------------
def sample_instance_pixels(
    labels: torch.Tensor, mask_labeled: torch.Tensor, K: int = 50
) -> Dict[int, torch.Tensor]:
    """
    labels: [B,H,W] int
    mask_labeled: [B,H,W] bool (True only on those few annotated instances)
    returns dict: inst_id -> indices tensor of shape [N, 3] with (b,y,x)
    """
    B, H, W = labels.shape
    outs = {}
    for b in range(B):
        lb = labels[b]
        mk = mask_labeled[b]
        # instances present in labeled area
        inst_ids = torch.unique(lb[(lb > 0) & mk])
        for iid in inst_ids.tolist():
            coords = torch.nonzero((lb == iid) & mk, as_tuple=False)
            if coords.numel() == 0:
                continue
            # random subset up to K
            idx = torch.randperm(coords.shape[0])[: min(K, coords.shape[0])]
            sel = torch.cat(
                [torch.full((idx.numel(), 1), b, dtype=torch.long), coords[idx]], dim=1
            )
            outs.setdefault((b, iid), sel)  # key separates by batch, id
    return outs  # keys: (b,iid) -> [N,3] (b,y,x)


def sparse_instance_contrastive_loss(
    emb: torch.Tensor,
    labels: torch.Tensor,
    mask_labeled: torch.Tensor,
    K: int = 50,
    margin: float = 0.5,
) -> torch.Tensor:
    """
    emb: [B,D,H,W] normalized
    labels: [B,H,W] ints (0 = bg/unlabeled, >0 = instance id)
    mask_labeled: [B,H,W] bool for sparse annotated regions
    """
    D = emb.size(1)
    samples = sample_instance_pixels(labels, mask_labeled, K)
    if not samples:
        return torch.tensor(0.0, device=emb.device, requires_grad=True)

    # Collect instance means
    inst_means: Dict[Tuple[int, int], torch.Tensor] = {}
    for key, idx in samples.items():
        b = idx[:, 0]
        y = idx[:, 1]
        x = idx[:, 2]
        vecs = emb[b, :, y, x]  # [N,D]
        inst_means[key] = vecs.mean(0)  # [D]

    # Pull: L2 to own mean
    pull_losses = []
    for key, idx in samples.items():
        b = idx[:, 0]
        y = idx[:, 1]
        x = idx[:, 2]
        vecs = emb[b, :, y, x]  # [N,D]
        mean = inst_means[key].unsqueeze(0)  # [1,D]
        pull_losses.append(((vecs - mean) ** 2).sum(dim=1).mean())
    pull = torch.stack(pull_losses).mean()

    # Push: different instance means at least margin apart (hinge)
    if len(inst_means) > 1:
        means = torch.stack(list(inst_means.values()))  # [M,D]
        # cosine distance ~= since normalized: ||a-b||^2 = 2(1 - cos)
        dists = torch.cdist(means, means, p=2)  # [M,M]
        M = dists.shape[0]
        mask = ~torch.eye(M, dtype=torch.bool, device=emb.device)
        push = F.relu(margin - dists[mask]).mean()
    else:
        push = torch.tensor(0.0, device=emb.device)

    return pull + push


# ---------------------------------------------
# 3) Consistency loss for unlabeled pixels
#    Two strong augmentations of the same image → embeddings should agree
#    We assume the two views are aligned (or we pass augmentations that preserve geometry)
# ---------------------------------------------
def consistency_loss(
    emb1: torch.Tensor, emb2: torch.Tensor, mask_unlabeled: torch.Tensor
) -> torch.Tensor:
    """
    emb1/emb2: [B,D,H,W] normalized
    mask_unlabeled: [B,H,W] bool (True where there is no annotation)
    """
    # cosine similarity ~ 1 for consistent; convert to distance
    cos = (emb1 * emb2).sum(dim=1)  # [B,H,W]
    dist = 1 - cos  # [B,H,W]
    loss = (
        dist[mask_unlabeled].mean()
        if mask_unlabeled.any()
        else torch.tensor(0.0, device=emb1.device)
    )
    return loss


# ---------------------------------------------
# 4) Example training step
#    Your dataloader should return:
#      - img: [B,3,H,W] float in [0,1]
#      - labels: [B,H,W] ints (0=bg/unlabeled, >0 instance id)  (only some instances annotated!)
#      - mask_labeled: [B,H,W] bool (True only on those annotated instances)
# ---------------------------------------------
class SPOCOLearner:
    def __init__(self, emb_dim=16, lr=1e-3, lambda_consistency=0.3, device="cuda"):
        self.net = PixelEmbeddingNet(emb_dim).to(device)
        self.opt = torch.optim.AdamW(self.net.parameters(), lr=lr, weight_decay=1e-4)
        self.lambda_consistency = lambda_consistency
        self.device = device

    def train_step(self, batch: Dict[str, torch.Tensor]) -> Dict[str, float]:
        img = batch["img"].to(self.device)  # [B,3,H,W]
        labels = batch["labels"].to(self.device).long()  # [B,H,W]
        mask_labeled = batch["mask_labeled"].to(self.device).bool()  # [B,H,W]

        # two views for consistency (use your own augmentations; here we just add noise)
        img2 = torch.clamp(img + 0.03 * torch.randn_like(img), 0, 1)

        emb1 = self.net(img)  # [B,D,H,W]
        emb2 = self.net(img2)  # [B,D,H,W]

        # masks
        mask_unlabeled = ~(mask_labeled & (labels > 0))

        L_sup = sparse_instance_contrastive_loss(emb1, labels, mask_labeled)
        L_con = consistency_loss(
            emb1.detach(), emb2, mask_unlabeled
        )  # stop-grad on one branch is common

        loss = L_sup + self.lambda_consistency * L_con

        self.opt.zero_grad(set_to_none=True)
        loss.backward()
        self.opt.step()

        return {
            "loss": float(loss.item()),
            "L_sup": float(L_sup.item()),
            "L_con": float(L_con.item()),
        }


# ---------------------------------------------
# 5) Inference: cluster embeddings → instance masks
#    Here: simple MeanShift via sklearn (install scikit-learn), or fallback to KMeans.
# ---------------------------------------------
@torch.no_grad()
def embeddings_to_instances(
    emb: torch.Tensor, bandwidth: float = 0.5, min_cluster_size: int = 20
):
    """
    emb: [1,D,H,W] (normalized). Returns an instance map [H,W] with {0,1,2,...}
    """
    from sklearn.cluster import MeanShift

    emb = emb[0].permute(1, 2, 0).contiguous()  # [H,W,D]
    H, W, D = emb.shape
    flat = emb.view(H * W, D).cpu().numpy()

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    labels = ms.fit_predict(flat)  # [H*W]
    inst = torch.from_numpy(labels).view(H, W)

    # clean up tiny clusters → 0
    ids, counts = inst.unique(return_counts=True)
    keep = ids[counts >= min_cluster_size]
    remap = torch.zeros(int(ids.max().item()) + 1, dtype=torch.long)
    next_id = 1
    for i in keep.tolist():
        remap[i] = next_id
        next_id += 1
    inst = remap[inst.clamp(min=0)]
    return inst  # [H,W] ints


# ---------------------------------------------
# 6) Tiny demo loop (pseudo-data)
# ---------------------------------------------
if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    learner = SPOCOLearner(emb_dim=16, lr=1e-3, lambda_consistency=0.3, device=device)

    # Fake batch: one 128x128 image, with TWO annotated instances sparsely marked
    B, H, W = 1, 128, 128
    img = torch.rand(B, 3, H, W)
    labels = torch.zeros(B, H, W, dtype=torch.long)
    mask_labeled = torch.zeros(B, H, W, dtype=torch.bool)

    # draw two circles as labeled instances (toy)
    yy, xx = torch.meshgrid(torch.arange(H), torch.arange(W), indexing="ij")
    inst1 = (yy - 40) ** 2 + (xx - 40) ** 2 <= 18**2
    inst2 = (yy - 88) ** 2 + (xx - 80) ** 2 <= 20**2
    labels[0][inst1] = 1
    labels[0][inst2] = 2

    # mark only sparse points from each instance as "labeled"
    s1 = torch.nonzero(inst1, as_tuple=False)
    s2 = torch.nonzero(inst2, as_tuple=False)
    pick1 = s1[torch.randperm(s1.size(0))[:200]]
    pick2 = s2[torch.randperm(s2.size(0))[:180]]
    mask_labeled[0, pick1[:, 0], pick1[:, 1]] = True
    mask_labeled[0, pick2[:, 0], pick2[:, 1]] = True

    batch = {"img": img, "labels": labels, "mask_labeled": mask_labeled}
    for step in range(50):
        logs = learner.train_step(batch)
        if step % 10 == 0:
            print(step, logs)

    with torch.no_grad():
        emb = learner.net(img.to(device)).cpu()
        inst = embeddings_to_instances(emb, bandwidth=0.6, min_cluster_size=30)
        print("Instances map shape:", inst.shape, "Unique IDs:", inst.unique().tolist())
