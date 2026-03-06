import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

word_to_ix = {"hello": 0, "world": 1}
embeds = nn.Embedding(2, 5)
print(embeds.weight)

lookup_tensor = torch.tensor([word_to_ix["hello"]], dtype=torch.long)
hello_embed = embeds(lookup_tensor)
print(hello_embed)

print(embeds(torch.tensor(1)))

CONTEXT_SIZE = 2
EMBEDDING_DIM = 10

test_sentence = """When forty winters shall besiege thy brow,
And dig deep trenches in thy beauty's field,
Thy youth's proud livery so gazed on now,
Will be a totter'd weed of small worth held:
Then being asked, where all thy beauty lies,
Where all the treasure of thy lusty days;
To say, within thine own deep sunken eyes,
Were an all-eating shame, and thriftless praise.
How much more praise deserv'd thy beauty's use,
If thou couldst answer 'This fair child of mine
Shall sum my count, and make my old excuse,'
Proving his beauty by succession thine!
This were to be new made when thou art old,
And see thy blood warm when thou feel'st it cold.""".split()

print(test_sentence)

ngrams = [
    ([test_sentence[i - j - 1] for j in range(CONTEXT_SIZE)], test_sentence[i])
    for i in range(CONTEXT_SIZE, len(test_sentence))
]

print(ngrams[:3])

vocab = set(test_sentence)
word_to_ix = {word: i for i, word in enumerate(vocab)}

print(word_to_ix)


class NGramLanguageModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, context_size):
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.linear1 = nn.Linear(context_size * embedding_dim, 128)
        self.linear2 = nn.Linear(128, vocab_size)

    def forward(self, inputs):
        embeds = self.embeddings(inputs).view((1, -1))
        out = F.relu(self.linear1(embeds))
        out = self.linear2(out)
        log_probs = F.log_softmax(out, dim=1)
        return log_probs


x = torch.randn(10)
print(f"{x=}")

soft = F.softmax(x, 0)
print(f"{soft=}")

print(F.log_softmax(x, dim=0))

losses = []
loss_fn = nn.NLLLoss()
model = NGramLanguageModel(len(vocab), EMBEDDING_DIM, CONTEXT_SIZE)
optimizer = optim.SGD(model.parameters(), lr=1e-4)

for epoch in range(1):
    total_loss = 0
    for context, target in ngrams[:1]:
        context_ids = [word_to_ix[word] for word in context]
        # print(f'{context=}')
        # print(f'{context_ids}')
        target_ids = [word_to_ix[target]]

        model.zero_grad()

        output = model(torch.tensor(context_ids))
        loss = loss_fn(output, torch.tensor(target_ids))

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    losses.append(total_loss)

print(losses)

print(model.embeddings.weight[word_to_ix["beauty"]])
