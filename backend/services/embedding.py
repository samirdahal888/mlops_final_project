from transformers import AutoModel, AutoTokenizer
from backend.config import ModelConfig
from backend.utils.get_device import get_device
import torch


class EmbeddingService:
    def __init__(self, config: ModelConfig):
        self.model_name = config.embedding_model_name
        self.device = get_device()
        self.tokenizer = None
        self.model = None

    def load(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.model.to(self.device)

    def embed(self, text: str):
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Convert a batch of texts into vector embeddings."""
        self._ensure_model_loaded()

        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        ).to(self.device)

        with torch.no_grad():
            output = self.model(**encoded)

        embeddings = self._mean_pooling(output, encoded["attention_mask"])
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

        return embeddings.cpu().tolist()

    def _ensure_model_loaded(self) -> None:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError(
                "Embedding model not loaded. Call load() before embed()."
            )

    @staticmethod
    def _mean_pooling(model_output, attention_mask) -> torch.Tensor:
        token_embeddings = model_output[0]
        input_mask = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        summed = torch.sum(token_embeddings * input_mask, dim=1)
        counted = torch.clamp(input_mask.sum(dim=1), min=1e-9)
        return summed / counted
