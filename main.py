# main.py
from Framework.InputManager.inputmgr import InputManager
from Framework.Frontend.frontend import Frontend
from Core.core import BootsCore
import threading

class Boots:
    """Brollo Original and Open-Source Testing System, Boots"""
    def __init__(self):
        self.core = BootsCore()
        self.core.set_sysprompt("")  # set system prompt
        self.inputmgr = InputManager("text", on_commit_callback=self.handle_input)
        self.frontend = Frontend("localhost", 5000)

    def handle_input(self, text):
        """Handle input from the input manager"""
        generated_text = self.core.generate(text)
        self.frontend.push_subtitle(generated_text)
        self.core.ttse.play()

    def run(self):
        """Run the Boots system"""
        frontend_thread = threading.Thread(target=self.frontend.run, daemon=True)
        frontend_thread.start()

        self.inputmgr.bench.run()

if __name__ == "__main__":
    boots = Boots()
    boots.run()
