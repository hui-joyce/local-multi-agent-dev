from typing import Optional, Tuple
from langgraph_orchestration.inference.model_loader import MLXModelLoader
from langgraph_orchestration.inference.inference_engine import MLXInferenceEngine
from langgraph_orchestration.agents.mlx_agents import (
    MLXCodeGenerationAgent,
    MLXUnitTestingAgent,
    MLXArchitecturalReviewAgent,
    MLXPlanningAgent,
    MLXCodeAnalysisAgent,
    MLXVulnerabilityDetectionAgent,
)

class MLXAgentFactory:
    def __init__(
        self,
        model_name: str = "qwen-3.5-9b",
        quantization: Optional[str] = "4bit",
    ):
        self.model_name = model_name
        self.quantization = quantization
        self.inference_engine: Optional[MLXInferenceEngine] = None
        self._model_loaded = False
    
    def load_model(self) -> MLXInferenceEngine:
        print(f"Loading MLX model: {self.model_name}")
        
        # Load model
        loader = MLXModelLoader(
            model_name=self.model_name,
            quantization=self.quantization,
        )
        model, tokenizer = loader.load()
        
        # Create inference engine
        self.inference_engine = MLXInferenceEngine(
            model=model,
            tokenizer=tokenizer,
        )
        
        self._model_loaded = True
        print("✓ MLX model loaded and ready")
        
        return self.inference_engine
    
    def create_code_generation_agent(self):
        if not self._model_loaded:
            self.load_model()
        return MLXCodeGenerationAgent(self.inference_engine)
    
    def create_unit_testing_agent(self):
        if not self._model_loaded:
            self.load_model()
        return MLXUnitTestingAgent(self.inference_engine)
    
    def create_architectural_review_agent(self):
        if not self._model_loaded:
            self.load_model()
        return MLXArchitecturalReviewAgent(self.inference_engine)
    
    def create_planning_agent(self):
        if not self._model_loaded:
            self.load_model()
        return MLXPlanningAgent(self.inference_engine)
    
    def create_code_analysis_agent(self):
        if not self._model_loaded:
            self.load_model()
        return MLXCodeAnalysisAgent(self.inference_engine)
    
    def create_vulnerability_detection_agent(self):
        if not self._model_loaded:
            self.load_model()
        return MLXVulnerabilityDetectionAgent(self.inference_engine)
    
    def create_all_agents(self) -> dict:
        if not self._model_loaded:
            self.load_model()
        
        return {
            "code_generation": MLXCodeGenerationAgent(self.inference_engine),
            "unit_testing": MLXUnitTestingAgent(self.inference_engine),
            "architectural_review": MLXArchitecturalReviewAgent(self.inference_engine),
            "planning": MLXPlanningAgent(self.inference_engine),
            "code_analysis": MLXCodeAnalysisAgent(self.inference_engine),
            "vulnerability_detection": MLXVulnerabilityDetectionAgent(self.inference_engine),
        }
    
    def get_model_info(self) -> dict:
        """Get information about loaded model."""
        if not self._model_loaded:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": self.model_name,
            "quantization": self.quantization,
            "inference_engine": self.inference_engine.get_model_info(),
        }