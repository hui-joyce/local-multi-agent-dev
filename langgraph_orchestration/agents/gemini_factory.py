from typing import Optional
from langgraph_orchestration.inference.inference_engine import GeminiInferenceEngine
from langgraph_orchestration.agents.mlx_agents import (
    MLXCodeGenerationAgent,
    MLXUnitTestingAgent,
    MLXArchitecturalReviewAgent,
    MLXPlanningAgent,
    MLXCodeAnalysisAgent,
    MLXVulnerabilityDetectionAgent,
)
from langgraph_orchestration.agents.supervisor import SupervisorAgent

class GeminiAgentFactory:
    def __init__(self, model_name: str = "gemini-3.1-flash-lite"):
        self.model_name = model_name
        self.inference_engine: Optional[GeminiInferenceEngine] = None
        self._model_loaded = False

    def ensure_loaded(self) -> GeminiInferenceEngine:
        if not self._model_loaded or self.inference_engine is None:
            self.load_model()

        if self.inference_engine is None:
            raise RuntimeError("Inference engine is unavailable after load attempt")

        return self.inference_engine
    
    def load_model(self) -> GeminiInferenceEngine:
        print(f"Loading Gemini model: {self.model_name}")
        self.inference_engine = GeminiInferenceEngine()
        self.inference_engine.model_name = self.model_name
        self._model_loaded = True
        print("✓ Gemini model loaded and ready")
        
        return self.inference_engine
    
    def create_code_generation_agent(self):
        return MLXCodeGenerationAgent(self.ensure_loaded())

    def create_supervisor_agent(self):
        return SupervisorAgent(self.ensure_loaded())
    
    def create_unit_testing_agent(self):
        return MLXUnitTestingAgent(self.ensure_loaded())
    
    def create_architectural_review_agent(self):
        return MLXArchitecturalReviewAgent(self.ensure_loaded())
    
    def create_planning_agent(self):
        return MLXPlanningAgent(self.ensure_loaded())
    
    def create_code_analysis_agent(self):
        return MLXCodeAnalysisAgent(self.ensure_loaded())
    
    def create_vulnerability_detection_agent(self):
        return MLXVulnerabilityDetectionAgent(self.ensure_loaded())
    
    def create_all_agents(self) -> dict:
        engine = self.ensure_loaded()
        
        return {
            "code_generation": MLXCodeGenerationAgent(engine),
            "unit_testing": MLXUnitTestingAgent(engine),
            "architectural_review": MLXArchitecturalReviewAgent(engine),
            "planning": MLXPlanningAgent(engine),
            "code_analysis": MLXCodeAnalysisAgent(engine),
            "vulnerability_detection": MLXVulnerabilityDetectionAgent(engine),
        }
    
    def get_model_info(self) -> dict:
        """Get information about loaded model."""
        if not self._model_loaded:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": self.model_name,
        }