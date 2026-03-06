import torch

b, t, n_embd = 2, 3, 4  # Example dimensions
tok_emb = torch.ones(b, t, n_embd)  # All 1s
pos_emb = torch.arange(t * n_embd).view(t, n_embd).float()  # Some values

x = tok_emb + pos_emb
print(x.shape)  # Outputs: torch.Size([2, 3, 4])
print(x)  # Shows pos_emb added to each batch element
