# Core/Context/context.py
class ContextManager:
    """Manager of Context."""
    def __init__(self):
        """
        Construtor of ContextManager.

        Attributes:
            history (list[tuple[str, str]]): Dialog history.
        """
        self.history = []

    def _format_sysprompt(self, sys_prompt: str):
        """Format the system prompt. Using Llama 2."""
        return f"<start_of_turn>system\n{sys_prompt}<end_of_turn>\n"
    
    def _format_userinput(self, user_input: str):
        """Format the user's input. Using Llama 2."""
        return f"<start_of_turn>user\n{user_input}<end_of_turn>\n"
    
    def _format_history(self):
        """Format the history. Using Llama 2. No Args."""
        return "\n".join([f"<start_of_turn>user\n{user}<end_of_turn><start_of_turn>assistant\n{assistant}<end_of_turn>" for user, assistant in self.history]) + "\n"
    
    def _format_reference(self, reference: list[str]):
        """Format the reference. Using Llama 2."""
        sep = "\n"
        return f"<start_of_turn>reference\n{sep.join(reference)}<end_of_turn>\n"
    
    def format_prompt(self, sys_prompt: str, user_input: str, reference: list[str]):
        """
        Format the whole prompt. Using Llama 2.
        """
        return self._format_sysprompt(sys_prompt) + self._format_history() + self._format_reference(reference) + self._format_userinput(user_input) + "<start_of_turn>assistant\n"
    
    def on_update(self, user_input: str, assistant: str):
        """
        Update the history.
        
        Args:
            user_input (str): User's input.
            assistant (str): Assistant's answer.
        """
        self.history.append((user_input, assistant))
        if len(self.history) > 5:
            self.history = self.history[-5:]