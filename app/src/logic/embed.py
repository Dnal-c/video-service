import numpy
import torch
from transformers import AutoTokenizer, AutoModel

device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")


class EmbeddingService:

    def __init__(self):
        # Load AutoModel from huggingface model repository
        tokenizer = AutoTokenizer.from_pretrained("ai-forever/sbert_large_nlu_ru")
        model = AutoModel.from_pretrained("ai-forever/sbert_large_nlu_ru")
        model = model.to(device)
        self.model = model
        self.tokenizer = tokenizer

    # Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def calc(self, text: str) -> numpy.ndarray:
        # Tokenize sentences
        encoded_input = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=10000,
            return_tensors='pt').to(device)

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)

        # Perform pooling. In this case, mean pooling
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        return sentence_embeddings[0].cpu().detach().numpy()
