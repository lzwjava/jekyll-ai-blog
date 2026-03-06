import argparse
import torch

import data

from dataclasses import dataclass


@dataclass
class Args:
    data: str = "./data/wikitext-2"
    checkpoint: str = "./model.pt"
    outf: str = "generated.txt"
    words: int = 1000
    seed: int = 1111
    cuda: bool = True
    temperature: float = 1.0
    log_interval: int = 100


def main():
    parser = argparse.ArgumentParser("PyTorch Word Language Model")
    parser.add_argument("--data", type=str, default=Args.data, help="location of data")
    parser.add_argument(
        "--checkpoint", type=str, default=Args.checkpoint, help="checkpoint"
    )
    parser.add_argument("--outf", type=str, default=Args.outf, help="output file")
    parser.add_argument("--words", type=int, default=Args.words, help="words")
    parser.add_argument("--seed", type=int, default=Args.seed, help="seed")
    parser.add_argument("--cuda", type=bool, default=Args.cuda, help="cuda")
    parser.add_argument(
        "--temperature", type=float, default=Args.temperature, help="temperature"
    )
    parser.add_argument(
        "--log-interval", type=int, default=Args.log_interval, help="log interval"
    )

    args = parser.parse_args()

    args = Args(**vars(args))

    torch.manual_seed(args.seed)

    if args.cuda:
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    if args.temperature < 1e-3:
        parser.error("temperature has to be greater or equal 1e-3")

    with open(args.checkpoint, "rb") as f:
        model = torch.load(f, map_location=device)

    model.eval()

    corpus = data.Corpus(args.data)
    ntokens = len(corpus.dictionary)

    is_transformer_model = (
        hasattr(model, "model_type") and model.model_type == "Transformer"
    )
    if not is_transformer_model:
        hidden = model.init_hidden(1)

    input = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device)
    print(ntokens)
    print(input)

    with open(args.outf, "w") as outf:
        with torch.no_grad():
            for i in range(args.words):
                if is_transformer_model:
                    output = model(input, False)
                    word_weights = (
                        output[-1].squeeze().div(args.temperature).exp().cpu()
                    )
                    word_idx = torch.multinomial(word_weights, 1)[0]
                    word_tensor = torch.Tensor([[word_idx]]).long().to(device)
                    input = torch.cat([input, word_tensor], 0)
                else:
                    output, hidden = model(input, hidden)
                    word_weights = output.squeeze().div(args.temperature).exp().cpu()
                    word_idx = torch.multinomial(word_weights, 1)[0]
                    input.fill_(word_idx)

                word = corpus.dictionary.idx2word[word_idx]
                outf.write(word + ("\n" if i % 20 == 19 else " "))

                if i % args.log_interval == 0:
                    print(" | Generated {}/{} words".format(i, args.words))


if __name__ == "__main__":
    main()
