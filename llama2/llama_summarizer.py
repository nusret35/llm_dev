import subprocess
from transformers import pipeline
import torch

class LlamaSummarizer :

    def __init__(self,model_path=None):
        self.model_path = model_path

    def get_llama_response(self, prompt: str) -> None:
        pipe = pipeline("text-generation", model="meta-llama/Llama-2-70b-chat-hf",torch_dtype=torch.float16)
        output = pipe(prompt)
        print(output)

    