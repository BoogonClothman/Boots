# Framework/InputManager/inputmgr.py
from .textbench import TextBench

class InputManager:
    def __init__(self, mode="text", on_commit_callback=None):
        self.mode = mode

        if self.mode == "text":
            self.bench = TextBench(on_commit_callback=on_commit_callback)
        else:
            raise ValueError("Invalid mode")
        
    def get_input(self):
        if self.mode == "text":
            return self.bench.get_text()
        else:
            return None
    