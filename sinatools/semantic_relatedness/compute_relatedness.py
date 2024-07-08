import torch
from . import tokenizer 
from . import model 

#cosine using average embedding 
def get_similarity_score(sentence1, sentence2):

  # Tokenize and encode sentences
  inputs1 = tokenizer(sentence1, return_tensors="pt")
  inputs2 = tokenizer(sentence2, return_tensors="pt")

  # Extract embeddings
  with torch.no_grad():
      outputs1 = model(**inputs1)
      outputs2 = model(**inputs2)
      
      embeddings1 = outputs1.last_hidden_state
      embeddings2 = outputs2.last_hidden_state

  # Mask padding tokens
  attention_mask1 = inputs1["attention_mask"]
  attention_mask2 = inputs2["attention_mask"]

  # Average pool across tokens, excluding padding
  embeddings1_avg = torch.sum(embeddings1 * attention_mask1.unsqueeze(-1), dim=1) / torch.sum(attention_mask1, dim=1, keepdim=True)
  embeddings2_avg = torch.sum(embeddings2 * attention_mask2.unsqueeze(-1), dim=1) / torch.sum(attention_mask2, dim=1, keepdim=True)

  # Calculate cosine similarity
  similarity = torch.nn.functional.cosine_similarity(embeddings1_avg, embeddings2_avg)

  return similarity.item()