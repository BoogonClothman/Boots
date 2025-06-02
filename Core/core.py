# Core/core.py
from .Context.context import ContextManager
from .Memory.memory import MemoryManager
from .LLM.langmodel import LangModel
from .Filter.filter import Filter
from .TTS.tts import TTSEngine
import asyncio

class BootsCore:
    """Boots Core"""
    def __init__(self):
        """
        Constructor of BootsCore.
        
        Attributes:
            ctx (ContextManager): Context Manager.
            system_prompt (str): System prompt.
            rag (MemoryManager): Retrieval Augmented Generation.
            llm (LangModel): Language Model.
            flt (Filter): Filter.
            ttse (TTSEngine): Text-to-Speech Engine.
        """
        # Context
        self.ctx = ContextManager()
        self.system_prompt = ""

        # Memory
        self.rag = MemoryManager(
            ragmodel_path="GanymedeNil/text2vec-large-chinese",
            device="cpu",
            cache_dir="./resources/.rag/models",
            local_file_only=False,
            index_path="./resources/.rag/index.faiss",
            pickle_path="./resources/.rag/texts.pkl",
            txts_dir="./documents"
        )
        self.rag.create_index()

        # LLM
        self.llm = LangModel(
            model_path="./resources/.llm/<your-llm-gguf>",
            n_gpu_layers=-1,
            main_gpu=0,
            vocab_only=False,
            use_mmap=True,
            n_ctx=4096,
            n_threads=12,
        )

        # Filter
        self.flt = Filter(
            badwords_path="./resources/.bad/badwords.txt"
        )

        # TTS
        self.ttse = TTSEngine(
            "zh-CN-XiaoyiNeural",  # change it if you need another voice
            volume="+0%",
            rate="+0%",
            pitch="+0Hz",
            save_path="./output/.tts/response.mp3"
        )

    def set_sysprompt(self, system_prompt: str):
        """
        Set the system prompt.
        
        Args:
            system_prompt (str): The system prompt.
        """
        self.system_prompt = system_prompt

    def generate(self, user_input: str):
        """
        Generate the response with user input.
        
        Args:
            user_input (str): The user input.
            
        Returns:
            str: The response.
        """
        reference = self.rag.query(user_input, 3, 0.5)
        prompt = self.ctx.format_prompt(self.system_prompt, user_input, reference)
        raw_response = self.llm.generate(prompt)
        filtered_response = self.flt.filter_text(raw_response)
        self.ctx.on_update(user_input, filtered_response)
        print(f"[Brollo] {filtered_response}")
        asyncio.run(self.ttse.synthesize(filtered_response))
        return filtered_response
