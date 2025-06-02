# Framework/InputManager/textbench.py
import tkinter as tk

class TextBench:
    def __init__(self, on_commit_callback=None):
        self.on_commit_callback = on_commit_callback
        self.root = tk.Tk()
        self.root.title("Text Bench")
        self.root.geometry("800x200")
        
        self._create_widgets()
    
    def _create_widgets(self):
        self.text_area = tk.Entry(self.root, font=("Times New Roman", 20), width=50)
        self.text_area.pack(padx=20, pady=10)
        
        self.submit_button = tk.Button(
            self.root,
            text="SEND",
            command=self._on_commit,
            bg="#4CAF50",
            fg="white",
            font=("Cascadia Mono", 20),
            width=20
        )
        self.submit_button.pack(pady=5)
    
    def _on_commit(self):
        text = self.text_area.get().strip()
        if text:
            self.text_area.delete(0, tk.END)
            if self.on_commit_callback:
                self.on_commit_callback(text)
            return text
        
    def get_text(self):
        return self.text_area.get().strip()
    
    def run(self):
        self.root.mainloop()
