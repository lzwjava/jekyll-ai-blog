import argparse
import math
import os.path
import time

import torch
from torch import nn

from word_language_model import data

from dataclasses import dataclass
import model


@dataclass
class Args:
    data: str = "./data/wikitext-2"
    model: str = "LSTM"
    emsize: int = 200
    nhid: int = 200
    nlayers: int = 2
    lr: float = 20
    clip: float = 0.25
    epochs: int = 40
    batch_size: int = 20
    bptt: int = 35
    dropout: float = 0.2
    tied: bool = True
    seed: int = 1111
    cuda: bool = False
    log_interval: int = 200
    save: str = "model.pt"
    onnx_export: str = ""
    nhead: int = 2
    dry_run: bool = False


def batchify(data: torch.Tensor, bsz, device):
    nbatch = data.size(0) // bsz
    data = data.narrow(0, 0, nbatch * bsz)
    data = data.view(bsz, -1).t().contiguous()
    return data.to(device)


def main():
    parser = argparse.ArgumentParser(
        description="PyTorch Wikitext-2 RNN/LSTM/GRU/Transformer Language Model"
    )
    parser.add_argument("--data", type=str, default=Args.data)
    parser.add_argument("--model", type=str, default=Args.model)
    parser.add_argument("--emsize", type=int, default=Args.emsize)
    parser.add_argument("--nhid", type=int, default=Args.nhid)
    parser.add_argument("--nlayers", type=int, default=Args.nlayers)
    parser.add_argument("--lr", type=float, default=Args.lr)
    parser.add_argument("--clip", type=float, default=Args.clip)
    parser.add_argument("--epochs", type=int, default=Args.epochs)
    parser.add_argument("--batch-size", type=int, default=Args.batch_size)
    parser.add_argument("--bptt", type=int, default=Args.bptt)
    parser.add_argument("--dropout", type=float, default=Args.dropout)
    parser.add_argument("--tied", default=Args.tied)
    parser.add_argument("--seed", type=int, default=Args.seed)
    parser.add_argument("--cuda", action="store_true")
    parser.add_argument("--log-interval", type=int, default=Args.log_interval)
    parser.add_argument("--save", type=str, default=Args.save)
    parser.add_argument("--onnx-export", type=str, default=Args.onnx_export)
    parser.add_argument("--nhead", type=int, default=Args.nhead)
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    args = Args(**vars(args))

    print(args)
    print(args.nhid)

    work(args)


def get_device(args: Args):
    if args.cuda:
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    return device


def work(args: Args):
    torch.manual_seed(args.seed)

    corpus = data.Corpus(args.data)

    eval_batch_size = 10

    device = get_device(args)

    val_data = batchify(corpus.valid, eval_batch_size, device)

    ntokens = len(corpus.dictionary)

    if args.model == "Transformer":
        tmodel = model.TransformerModel(
            ntokens, args.emsize, args.nhead, args.nhid, args.nlayers, args.dropout
        ).to(device)
    else:
        tmodel = model.RNNModel(
            args.model,
            ntokens,
            args.emsize,
            args.nhid,
            args.nlayers,
            args.dropout,
            args.tied,
        ).to(device)

    lr = args.lr
    best_val_loss = None
    try:
        for epoch in range(1, args.epochs + 1):
            epoch_start_time = time.time()
            train(args, tmodel, corpus, epoch)
            val_loss = evaluate(args, tmodel, val_data, corpus, eval_batch_size)
            print("-" * 89)
            print(
                "| end of epoch {:3d} | time: {:5.2f}s | valid loss {:5.2f} | valid ppl {:8.2f}".format(
                    epoch,
                    (time.time() - epoch_start_time),
                    val_loss,
                    math.exp(val_loss),
                )
            )
            print("-" * 89)
            if not best_val_loss or val_loss < best_val_loss:
                with open(args.save, "wb") as f:
                    torch.save(tmodel, f)
                best_val_loss = val_loss
            else:
                lr /= 4.0
    except KeyboardInterrupt:
        print("-" * 89)
        print("Exit early")

    test(args, corpus, eval_batch_size)


def export_onnx(args: Args, tmodel: nn.Module, batch_size):
    path = args.onnx_export
    seq_len = args.bptt
    device = get_device(args)

    print("export onnx at {}.".format(os.path.realpath(path)))
    tmodel.eval()
    dummy_input = (
        torch.LongTensor(seq_len * batch_size).zero_().view(-1, batch_size).to(device)
    )
    hidden = tmodel.init_hidden(batch_size)
    torch.onnx.export(tmodel, (dummy_input, hidden), path)


def test(args: Args, corpus: data.Corpus, eval_batch_size):
    test_data = batchify(corpus.test, eval_batch_size, get_device(args))

    with open(args.save, "rb") as f:
        tmodel = torch.load(f)
        if args.model in ["RNN_TANH", "RNN_RELU", "LSTM", "GRU"]:
            tmodel.rnn.flatten_parameters()

    test_loss = evaluate(args, tmodel, test_data, corpus, eval_batch_size)
    print("=" * 89)
    print(
        "| End of training | test loss {:5.2f} | test ppl {:8.2f}".format(
            test_loss, math.exp(test_loss)
        )
    )
    print("=" * 89)

    if len(args.onnx_export) > 0:
        export_onnx(args, tmodel, batch_size=1)


def repackage_hidden(h):
    if isinstance(h, torch.Tensor):
        return h.detach()
    else:
        return tuple(repackage_hidden(v) for v in h)


def train(args: Args, tmodel: nn.Module, corpus: data.Corpus, epoch):
    device = get_device(args)

    train_data = batchify(corpus.train, args.batch_size, device)

    ntokens = len(corpus.dictionary)

    tmodel.train()
    total_loss = 0
    start_time = time.time()
    if args.model != "Transformer":
        hidden = tmodel.init_hidden(args.batch_size)

    for batch, i in enumerate(range(0, train_data.size(0) - 1, args.bptt)):
        data, targets = get_batch(train_data, i, args.bptt)
        tmodel.zero_grad()
        if args.model == "Transformer":
            output = tmodel(data)
            output = output.view(-1, ntokens)
        else:
            hidden = repackage_hidden(hidden)
            output, hidden = tmodel(data, hidden)

        loss = loss_fn(output, targets)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(tmodel.parameters(), args.clip)
        for p in tmodel.parameters():
            p.data.add_(p.grad, alpha=-args.lr)

        total_loss += loss.item()

        if batch % args.log_interval == 0 and batch > 0:
            cur_loss = total_loss / args.log_interval
            elapsed = time.time() - start_time
            print(
                "| epoch {:3d} | {:5d}/{:5d} batches| lr {:2.2f}| ms/batch {:5.2f}| loss {:5.2f}| ppl{:8.2f}".format(
                    epoch,
                    batch,
                    len(train_data) // args.bptt,
                    args.lr,
                    elapsed * 1000 / args.log_interval,
                    cur_loss,
                    math.exp(cur_loss),
                )
            )
            total_loss = 0
            start_time = time.time()
        if args.dry_run:
            break


def get_batch(source, i, bptt):
    seq_len = min(bptt, len(source) - 1 - i)
    data = source[i : i + seq_len]
    target = source[i + 1 : i + 1 + seq_len].view(-1)
    return data, target


loss_fn = nn.NLLLoss()


def evaluate(
    args: Args, model: nn.Module, data_source, corpus: data.Corpus, eval_batch_size
):
    model.eval()
    total_loss = 0.0
    ntokens = len(corpus.dictionary)
    if args.model != "Transformer":
        hidden = model.init_hidden(eval_batch_size)
    with torch.no_grad():
        for i in range(0, data_source.size(0) - 1, args.bptt):
            data, targets = get_batch(data_source, i, args.bptt)
            if args.model == "Transformer":
                output = model(data)
                output = output.view(-1, ntokens)
            else:
                output, hidden = model(data, hidden)
            total_loss += len(data) * loss_fn(output, targets).item()

    return total_loss / (len(data_source) - 1)


if __name__ == "__main__":
    main()
