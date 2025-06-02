# Core/LLM/langmodel.py
from llama_cpp import Llama
import torch

class LangModel:
    """Language Model"""
    def __init__(
            self,
            model_path: str,
            n_gpu_layers: int = -1,
            main_gpu: int = 0,
            vocab_only: bool = False,
            use_mmap:bool = True,
            n_ctx: int = 4096,
            n_threads: int = 12
            ):
        """
        Constructor of LangModel.

        Args:
            model_path (str): Path to your model file (.gguf).
            n_gpu_layers (int): Number of layers to offload to GPU. If -1, all layers are offloaded.
            main_gpu (int): X for GPU X. If you have more GPUs, you can specify which one to use.
            vocab_only (bool): Only load the vocabulary no weights. 
            use_mmap (bool): Use mmap if possible.
            n_ctx (int): Limit of the context length.
            n_threads (int): Number of threads to use for generation.
        """
        self.llm = Llama(
            model_path,
            n_gpu_layers = n_gpu_layers if torch.cuda.is_available() else 0,
            main_gpu = main_gpu,
            vocab_only = vocab_only,
            use_mmap = use_mmap,
            n_ctx = n_ctx,
            n_threads = n_threads
        )
    
    def generate(
            self,
            prompt: str,
            temperature: float = 0.8,
            repeat_penalty: float = 1.2,
            max_tokens: int = 512
            ):
        """
        Generate the response with pure prompt.

        Args:
            prompt (str): The prompt used by the model.
            temperature (float, optional): Temperature for generation. Normally `0.8`.
            repeat_penalty (float, optional): Repeat-penalty for generation. Normally `1.2`.
            max_token (int, optional): Max number of tokens for generation. Normally `512`.
        
        Returns:
            str: Response from the model.
        """
        return self.llm(
            prompt = prompt,
            temperature = temperature,
            repeat_penalty = repeat_penalty,
            max_tokens = max_tokens,
            stop = ["<end_of_turn>", "<eos>", "\n"]
        )["choices"][0]["text"].strip()