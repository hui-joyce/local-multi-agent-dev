from typing import Optional
from langgraph_orchestration.agents.base import SyncBaseAgent
from langgraph_orchestration.inference.inference_engine import (
    MLXInferenceEngine,
    GenerationConfig,
)

class MLXAgent:
    def __init__(self, inference_engine: MLXInferenceEngine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inference_engine = inference_engine
    
    def _build_agent_prompt(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        """
        Build prompt for this agent with RAG context.
        Override in subclasses to customize prompt format.
        """
        system_prompt = f"{self.description}\n\nBe concise and actionable."
        
        return self.inference_engine.build_prompt(
            user_input=user_input,
            context=context,
            system_prompt=system_prompt,
        )
    
    def _generate_response(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None,
    ) -> str:
        return self.inference_engine.generate(prompt, config=config, stream=False)


class MLXCodeGenerationAgent(MLXAgent, SyncBaseAgent):
    
    def __init__(self, inference_engine: MLXInferenceEngine):
        super().__init__(
            inference_engine=inference_engine,
            name="code_generation",
            description=(
                "Generates production-ready code based on requirements. "
                "You are expert at Python, creating clean, well-documented code."
            ),
        )
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        prompt = self._build_agent_prompt(user_input, context)
        
        # Customize generation for code
        config = GenerationConfig(
            max_tokens=4096,
            temperature=0.3,  # Lower temp for code
        )
        
        response = self._generate_response(prompt, config)
        return response

class MLXUnitTestingAgent(MLXAgent, SyncBaseAgent):
    """Unit test generation using MLX-based Qwen model."""
    
    def __init__(self, inference_engine: MLXInferenceEngine):
        super().__init__(
            inference_engine=inference_engine,
            name="unit_testing",
            description=(
                "Generates comprehensive unit tests with high code coverage. "
                "You are expert at Python testing, using pytest and mocking."
            ),
        )
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        """
        Generate unit tests.
        
        Args:
            user_input: Code or requirements to test
            context: Testing best practices from RAG
            
        Returns:
            Generated test suite
        """
        prompt = self._build_agent_prompt(user_input, context)
        
        config = GenerationConfig(
            max_tokens=4096,
            temperature=0.2,  # Lower temp for tests
        )
        
        response = self._generate_response(prompt, config)
        return response

class MLXArchitecturalReviewAgent(MLXAgent, SyncBaseAgent):    
    def __init__(self, inference_engine: MLXInferenceEngine):
        super().__init__(
            inference_engine=inference_engine,
            name="architectural_review",
            description=(
                "Reviews code for architectural fitness and best practices. "
                "You are expert at software architecture and design patterns."
            ),
        )
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        prompt = self._build_agent_prompt(user_input, context)
        
        config = GenerationConfig(
            max_tokens=3000,
            temperature=0.5,
        )
        
        response = self._generate_response(prompt, config)
        return response

class MLXPlanningAgent(MLXAgent, SyncBaseAgent):    
    def __init__(self, inference_engine: MLXInferenceEngine):
        super().__init__(
            inference_engine=inference_engine,
            name="planning",
            description=(
                "Plans complex reverse engineering tasks. "
                "You create structured, methodical analysis plans."
            ),
        )
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        prompt = self._build_agent_prompt(user_input, context)
        
        config = GenerationConfig(
            max_tokens=2048,
            temperature=0.5,
        )
        
        response = self._generate_response(prompt, config)
        return response

class MLXCodeAnalysisAgent(MLXAgent, SyncBaseAgent):    
    def __init__(self, inference_engine: MLXInferenceEngine):
        super().__init__(
            inference_engine=inference_engine,
            name="code_analysis",
            description=(
                "Analyzes code structure, patterns, and logic flow. "
                "You are expert at reverse engineering and binary analysis."
            ),
        )
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        prompt = self._build_agent_prompt(user_input, context)
        
        config = GenerationConfig(
            max_tokens=3000,
            temperature=0.4,
        )
        
        response = self._generate_response(prompt, config)
        return response

class MLXVulnerabilityDetectionAgent(MLXAgent, SyncBaseAgent):    
    def __init__(self, inference_engine: MLXInferenceEngine):
        super().__init__(
            inference_engine=inference_engine,
            name="vulnerability_detection",
            description=(
                "Detects security vulnerabilities and weaknesses. "
                "You are expert at security analysis, threat modeling, and CVEs."
            ),
        )
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        prompt = self._build_agent_prompt(user_input, context)
        
        config = GenerationConfig(
            max_tokens=4096,
            temperature=0.3,  # Lower for security analysis
        )
        
        response = self._generate_response(prompt, config)
        return response