"""
Supervisor agent for domain routing and orchestration.

The Supervisor analyzes incoming requests and routes them to the
appropriate domain (software development or reverse engineering).
"""

from typing import Literal, Optional
from .base import SyncBaseAgent


class SupervisorAgent(SyncBaseAgent):
    """
    In a production system, this would use an LLM for intelligent routing.
    For now, we use heuristic-based routing on keywords.
    """
    
    SOFTWARE_DEV_KEYWORDS = {
        "code", "generate", "implement", "unit test", "testing",
        "architecture", "design", "refactor", "review", "optimize",
        "debug", "fix", "error", "feature", "function", "method",
        "class", "module", "import", "dependency", "api", "endpoint",
    }
    
    REVERSE_ENG_KEYWORDS = {
        "reverse engineer", "decompile", "assembly", "binary", "vulnerability",
        "security", "exploit", "threat", "attack", "analysis", "malware",
        "disassemble", "bytecode", "hex", "buffer overflow", "injection",
        "analyze code", "examine binary", "inspect",
    }
    
    def __init__(self):
        super().__init__(
            name="supervisor",
            description="Routes user requests to appropriate domain based on content",
        )
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> Literal["software_dev", "reverse_engineering"]:
        """        
        This heuristic implementation counts keyword matches.
        In production, this would use an LLM for nuanced understanding.
        """
        user_lower = user_input.lower()
        
        software_dev_score = sum(
            1 for keyword in self.SOFTWARE_DEV_KEYWORDS
            if keyword in user_lower
        )
        
        reverse_eng_score = sum(
            1 for keyword in self.REVERSE_ENG_KEYWORDS
            if keyword in user_lower
        )
        
        # If both domains score equally or neither scores, default to software_dev
        if reverse_eng_score > software_dev_score:
            return "reverse_engineering"
        else:
            return "software_dev"