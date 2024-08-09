from sinatools.DataDownload import downloader
import os
from sinatools.ner.helpers import load_object
import pickle
import os
import torch
import pickle
import json
from argparse import Namespace
from transformers import pipeline

tagger = None
tag_vocab = None
train_config = None

filename = 'Wj27012000.tar'
path =downloader.get_appdatadir()
model_path = os.path.join(path, filename)

_path = os.path.join(model_path, "tag_vocab.pkl")

with open(_path, "rb") as fh:
    tag_vocab = pickle.load(fh)

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

pipe = pipeline("sentiment-analysis", model="best_model", device=0, return_all_scores =True, max_length=128, truncation=True)
