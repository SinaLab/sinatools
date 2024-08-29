from sinatools.DataDownload import downloader
import os
from transformers import pipeline

path =downloader.get_appdatadir()

pipe = pipeline("sentiment-analysis", model= os.path.join(path, "relation_model"), return_all_scores =True, max_length=128, truncation=True)