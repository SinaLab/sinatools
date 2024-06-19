import torch
from transformers import BertTokenizer
from functools import partial
import re
import itertools
from nlptools.arabiner.data import datasets
class BertSeqTransform:
    def __init__(self, bert_model, vocab, max_seq_len=512):
        self.tokenizer = BertTokenizer.from_pretrained(bert_model)
        self.encoder = partial(
            self.tokenizer.encode,
            max_length=max_seq_len,
            truncation=True,
        )
        self.max_seq_len = max_seq_len
        self.vocab = vocab

    def __call__(self, segment):
        subwords, tags, tokens = list(), list(), list()
        unk_token = datasets.Token(text="UNK")

        for token in segment:
            token_subwords = self.encoder(token.text)[1:-1]
            subwords += token_subwords
            tags += [self.vocab.tags[0].get_stoi()[token.gold_tag[0]]] + [self.vocab.tags[0].get_stoi()["O"]] * (len(token_subwords) - 1)
            tokens += [token] + [unk_token] * (len(token_subwords) - 1)

        # Truncate to max_seq_len
        if len(subwords) > self.max_seq_len - 2:
            text = " ".join([t.text for t in tokens if t.text != "UNK"])
          
            subwords = subwords[:self.max_seq_len - 2]
            tags = tags[:self.max_seq_len - 2]
            tokens = tokens[:self.max_seq_len - 2]

        subwords.insert(0, self.tokenizer.cls_token_id)
        subwords.append(self.tokenizer.sep_token_id)

        tags.insert(0, self.vocab.tags[0].get_stoi()["O"])
        tags.append(self.vocab.tags[0].get_stoi()["O"])

        tokens.insert(0, unk_token)
        tokens.append(unk_token)

        return torch.LongTensor(subwords), torch.LongTensor(tags), tokens, len(tokens)


class NestedTagsTransform:
    def __init__(self, bert_model, vocab, max_seq_len=512):
        self.tokenizer = BertTokenizer.from_pretrained(bert_model)
        self.encoder = partial(
            self.tokenizer.encode,
            max_length=max_seq_len,
            truncation=True,
        )
        self.max_seq_len = max_seq_len
        self.vocab = vocab

    def __call__(self, segment):
        tags, tokens, subwords = list(), list(), list()
        unk_token = datasets.Token(text="UNK")

        # Encode each token and get its subwords and IDs
        for token in segment:
            token.subwords = self.encoder(token.text)[1:-1]
            subwords += token.subwords
            tokens += [token] + [unk_token] * (len(token.subwords ) - 1)

        # Construct the labels for each tag type
        # The sequence will have a list of tags for each type
        # The final tags for a sequence is a matrix NUM_TAG_TYPES x SEQ_LEN
        # Example:
        #   [
        #       [O,     O,     B-PERS, I-PERS, O, O, O]
        #       [B-ORG, I-ORG, O,      O,      O, O, O]
        #       [O,     O,     O,      O,      O, O, B-GPE]
        #   ]
        for vocab in self.vocab.tags[1:]:
            vocab_tags = "|".join([t for t in vocab.get_itos() if "-" in t])
            r = re.compile(vocab_tags)

            # This is really messy
            # For a given token we find a matching tag_name, BUT we might find
            # multiple matches (i.e. a token can be labeled B-ORG and I-ORG) in this
            # case we get only the first tag as we do not have overlapping of same type
            single_type_tags = [[(list(filter(r.match, token.gold_tag))
                                or ["O"])[0]] + ["O"] * (len(token.subwords) - 1)
                                for token in segment]
            single_type_tags = list(itertools.chain(*single_type_tags))
            tags.append([vocab.get_stoi()[tag] for tag in single_type_tags])

        # Truncate to max_seq_len
        if len(subwords) > self.max_seq_len - 2:
            text = " ".join([t.text for t in tokens if t.text != "UNK"])
          
            subwords = subwords[:self.max_seq_len - 2]
            tags = [t[:self.max_seq_len - 2] for t in tags]
            tokens = tokens[:self.max_seq_len - 2]

        # Add dummy token at the start end of sequence
        tokens.insert(0, unk_token)
        tokens.append(unk_token)

        # Add CLS and SEP at start end of subwords
        subwords.insert(0, self.tokenizer.cls_token_id)
        subwords.append(self.tokenizer.sep_token_id)
        subwords = torch.LongTensor(subwords)

        # Add "O" tags for the first and last subwords
        tags = torch.Tensor(tags)
        tags = torch.column_stack((
            torch.Tensor([vocab.get_stoi()["O"] for vocab in self.vocab.tags[1:]]),
            tags,
            torch.Tensor([vocab.get_stoi()["O"] for vocab in self.vocab.tags[1:]]),
        )).unsqueeze(0)

        mask = torch.ones_like(tags)
        return subwords, tags, tokens, mask, len(tokens)