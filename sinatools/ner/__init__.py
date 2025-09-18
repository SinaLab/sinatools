from sinatools.DataDownload import downloader
import os
from sinatools.ner.helpers import load_object
from sinatools.ner.tag_vocab import load_tag_vocab
import torch
import json
from argparse import Namespace

tagger = None
tag_vocab = None
train_config = None

filename = 'Wj27012000.tar'
path =downloader.get_appdatadir()
model_path = os.path.join(path, filename)

_path = os.path.join(model_path, "tag_vocab.pkl")
tag_vocab = load_tag_vocab(_path)

train_config = Namespace()
args_path = os.path.join(model_path, "args.json")

with open(args_path, "r") as fh:
    train_config.__dict__ = json.load(fh)

model = load_object(train_config.network_config["fn"], train_config.network_config["kwargs"])
model = torch.nn.DataParallel(model)

if torch.cuda.is_available():
    model = model.cuda()

train_config.trainer_config["kwargs"]["model"] = model
tagger = load_object(train_config.trainer_config["fn"], train_config.trainer_config["kwargs"])
tagger.load(os.path.join(model_path,"checkpoints"))
