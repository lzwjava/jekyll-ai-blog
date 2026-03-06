import argparse
import os
import time

import torch
from torch.nn import functional as F

from bow import Bow
from config import ModelConfig
from dataset import create_datasets, InfiniteDataLoader


@torch.no_grad()
def generate(model, idx, max_new_tokens, temperature=1.0, do_sample=False, top_k=None):
    block_size = model.get_block_size()

    for _ in range(max_new_tokens):
        idx_cond = idx if idx.size(1) <= block_size else idx[:, -block_size:]
        print(idx_cond)
        print(f"{idx_cond.size()=}")

        logits, _ = model(idx_cond)

        print("logits")
        print(logits)
        print(f"{logits.size()=}")

        logits = logits[:, -1, :] / temperature

        if top_k is not None:
            v, _ = torch.topk(logits, top_k)
            print(f"{v=}")
            logits[logits < v[:, [-1]]] = -float("inf")

        probs = F.softmax(logits, dim=-1)

        if do_sample:
            idx_next = torch.multinomial(probs, num_samples=1)
        else:
            _, idx_next = torch.topk(probs, k=1, dim=-1)

        idx = torch.cat((idx, idx_next), dim=1)

    return idx


def print_samples(num=10):
    X_init = torch.zeros(num, 1, dtype=torch.long).to("cuda")
    top_k = None
    steps = train_dataset.get_output_length() - 1
    X_samp = generate(model, X_init, steps, top_k=top_k, do_sample=True).to("cpu")
    train_samples, test_samples, new_samples = [], [], []
    for i in range(X_samp.size(0)):
        row = X_samp[i, 1:].tolist()
        crop_index = row.index(0) if 0 in row else len(row)
        row = row[:crop_index]
        word_samp = train_dataset.decode(row)
        if train_dataset.contains(word_samp):
            train_samples.append(word_samp)
        elif test_dataset.contains(word_samp):
            test_samples.append(word_samp)
        else:
            new_samples.append(word_samp)

    print("-" * 80)
    for lst, desc in [
        (train_samples, "in train"),
        (test_samples, "in test"),
        (new_samples, "new"),
    ]:
        print(f"{len(lst)} samples that are in {desc}")
        for word in lst:
            print(word)
    print("-" * 80)


if __name__ == "__main__":
    print("main")
    parser = argparse.ArgumentParser(description="make more")
    parser.add_argument(
        "--input-file", type=str, default="names.txt", help="input file"
    )
    parser.add_argument("--seed", type=int, default=3047, help="seed")
    parser.add_argument(
        "--work-dir", type=str, default="out", help="output working directory"
    )
    args = parser.parse_args()
    print(vars(args))

    torch.manual_seed(args.seed)

    torch.cuda.manual_seed_all(args.seed)

    os.makedirs(args.work_dir, exist_ok=True)

    train_dataset, test_dataset = create_datasets(args.input_file)

    contains = train_dataset.contains("jack")
    print(contains)
    test_contains = test_dataset.contains("jack")
    print(test_contains)

    ix = train_dataset.encode("jack")
    print(ix)
    word = train_dataset.decode(ix.tolist())
    print(word)

    x0, y0 = train_dataset[0]
    print(f"x0={x0}")
    print(f"y0={y0}")

    vocab_size = train_dataset.get_vocab_size()
    block_size = train_dataset.get_output_length()

    print(f"{vocab_size=}, {block_size=}")

    n_layer = 4
    n_head = 4
    n_embd = 64
    n_embd2 = 64
    device = "cuda"
    learning_rate = 5e-4
    weight_decay = 0.01
    batch_size = 32
    num_workers = 4
    max_steps = 1000

    config = ModelConfig(
        vocab_size=vocab_size,
        block_size=block_size,
        n_layer=n_layer,
        n_head=n_head,
        n_embd=n_embd,
        n_embd2=n_embd2,
    )

    model = Bow(config)

    model.to(device)

    print(f"model #params: {sum(p.numel() for p in model.parameters())}")

    for p in model.parameters():
        # print(p)
        print(p.size())

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=learning_rate,
        weight_decay=weight_decay,
        betas=(0.9, 0.99),
        eps=1e-8,
    )

    batch_loader = InfiniteDataLoader(
        train_dataset, batch_size=batch_size, pin_memory=False, num_workers=4
    )

    best_loss = None
    step = 0

    while True:
        t0 = time.time()

        batch = batch_loader.next()
        batch = [t.to(device) for t in batch]
        X, Y = batch

        logits, loss = model(X, Y)

        # print(logits)
        # print(loss)

        model.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

        if step % 10 == 0:
            print(f"step {step} | loss {loss.item():.4f}")

        step += 1
        if step >= max_steps:
            break

    X_init = torch.zeros(10, 1, dtype=torch.long).to(device)

    output_len = train_dataset.get_output_length() - 1

    result = generate(model, X_init, output_len, top_k=2, do_sample=True)

    print("result")
    print(result)

    print_samples(num=10)
