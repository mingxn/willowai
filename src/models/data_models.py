"""
Data models for the plant analysis application.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class PlantInfo:
    """Information about a plant species."""
    scientific_name: Optional[str] = None
    common_name: Optional[str] = None
    family: Optional[str] = None
    characteristics: List[str] = field(default_factory=list)
    confidence: Optional[float] = None
    origin: Optional[str] = None
    growing_season: Optional[str] = None

@dataclass
class HealthStatus:
    """Health status of a plant."""
    overall_status: str = "unknown"  # healthy, diseased, weak
    diseases_detected: List[str] = field(default_factory=list)
    disease_names: List[str] = field(default_factory=list)
    severity_level: str = "unknown"  # mild, moderate, severe
    symptoms: List[str] = field(default_factory=list)
    possible_causes: List[str] = field(default_factory=list)

@dataclass
class GrowthAnalysis:
    """Growth analysis of a plant."""
    growth_stage: str = "unknown"  # seedling, juvenile, mature, old
    nutrition_status: str = "unknown"  # sufficient, deficient, excessive
    environmental_conditions: Dict[str, str] = field(default_factory=dict)
    growth_rate: str = "unknown"  # slow, normal, fast
    estimated_harvest_time: Optional[str] = None

@dataclass
class Recommendations:
    """Care and treatment recommendations."""
    treatment_steps: List[str] = field(default_factory=list)
    care_instructions: List[str] = field(default_factory=list)
    fertilization_schedule: List[str] = field(default_factory=list)
    watering_schedule: List[str] = field(default_factory=list)
    prevention_measures: List[str] = field(default_factory=list)
    optimal_conditions: Dict[str, str] = field(default_factory=dict)

@dataclass
class AnalysisMetadata:
    """Metadata about the analysis."""
    timestamp: datetime = field(default_factory=datetime.now)
    analysis_type: str = "complete"
    model_used: str = "unknown"
    image_size: tuple = (0, 0)
    processing_time: Optional[float] = None
    confidence_threshold: float = 0.7

@dataclass
class CompleteAnalysis:
    """Complete plant analysis result."""
    plant_info: PlantInfo = field(default_factory=PlantInfo)
    health_status: HealthStatus = field(default_factory=HealthStatus)
    growth_analysis: GrowthAnalysis = field(default_factory=GrowthAnalysis)
    recommendations: Recommendations = field(default_factory=Recommendations)
    metadata: AnalysisMetadata = field(default_factory=AnalysisMetadata)
    raw_response: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "plant_info": {
                "scientific_name": self.plant_info.scientific_name,
                "common_name": self.plant_info.common_name,
                "family": self.plant_info.family,
                "characteristics": self.plant_info.characteristics,
                "confidence": self.plant_info.confidence,
                "origin": self.plant_info.origin,
                "growing_season": self.plant_info.growing_season
            },
            "health_status": {
                "overall_status": self.health_status.overall_status,
                "diseases_detected": self.health_status.diseases_detected,
                "disease_names": self.health_status.disease_names,
                "severity_level": self.health_status.severity_level,
                "symptoms": self.health_status.symptoms,
                "possible_causes": self.health_status.possible_causes
            },
            "growth_analysis": {
                "growth_stage": self.growth_analysis.growth_stage,
                "nutrition_status": self.growth_analysis.nutrition_status,
                "environmental_conditions": self.growth_analysis.environmental_conditions,
                "growth_rate": self.growth_analysis.growth_rate,
                "estimated_harvest_time": self.growth_analysis.estimated_harvest_time
            },
            "recommendations": {
                "treatment_steps": self.recommendations.treatment_steps,
                "care_instructions": self.recommendations.care_instructions,
                "fertilization_schedule": self.recommendations.fertilization_schedule,
                "watering_schedule": self.recommendations.watering_schedule,
                "prevention_measures": self.recommendations.prevention_measures,
                "optimal_conditions": self.recommendations.optimal_conditions
            },
            "metadata": {
                "timestamp": self.metadata.timestamp.isoformat(),
                "analysis_type": self.metadata.analysis_type,
                "model_used": self.metadata.model_used,
                "image_size": self.metadata.image_size,
                "processing_time": self.metadata.processing_time,
                "confidence_threshold": self.metadata.confidence_threshold
            },
            "raw_response": self.raw_response
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompleteAnalysis':
        """Create from dictionary representation."""
        analysis = cls()
        
        if "plant_info" in data:
            pi = data["plant_info"]
            analysis.plant_info = PlantInfo(
                scientific_name=pi.get("scientific_name"),
                common_name=pi.get("common_name"),
                family=pi.get("family"),
                characteristics=pi.get("characteristics", []),
                confidence=pi.get("confidence"),
                origin=pi.get("origin"),
                growing_season=pi.get("growing_season")
            )
        
        if "health_status" in data:
            hs = data["health_status"]
            analysis.health_status = HealthStatus(
                overall_status=hs.get("overall_status", "unknown"),
                diseases_detected=hs.get("diseases_detected", []),
                disease_names=hs.get("disease_names", []),
                severity_level=hs.get("severity_level", "unknown"),
                symptoms=hs.get("symptoms", []),
                possible_causes=hs.get("possible_causes", [])
            )
        
        if "growth_analysis" in data:
            ga = data["growth_analysis"]
            analysis.growth_analysis = GrowthAnalysis(
                growth_stage=ga.get("growth_stage", "unknown"),
                nutrition_status=ga.get("nutrition_status", "unknown"),
                environmental_conditions=ga.get("environmental_conditions", {}),
                growth_rate=ga.get("growth_rate", "unknown"),
                estimated_harvest_time=ga.get("estimated_harvest_time")
            )
        
        if "recommendations" in data:
            rec = data["recommendations"]
            analysis.recommendations = Recommendations(
                treatment_steps=rec.get("treatment_steps", []),
                care_instructions=rec.get("care_instructions", []),
                fertilization_schedule=rec.get("fertilization_schedule", []),
                watering_schedule=rec.get("watering_schedule", []),
                prevention_measures=rec.get("prevention_measures", []),
                optimal_conditions=rec.get("optimal_conditions", {})
            )
        
        if "metadata" in data:
            meta = data["metadata"]
            timestamp = datetime.fromisoformat(meta["timestamp"]) if "timestamp" in meta else datetime.now()
            analysis.metadata = AnalysisMetadata(
                timestamp=timestamp,
                analysis_type=meta.get("analysis_type", "complete"),
                model_used=meta.get("model_used", "unknown"),
                image_size=tuple(meta.get("image_size", (0, 0))),
                processing_time=meta.get("processing_time"),
                confidence_threshold=meta.get("confidence_threshold", 0.7)
            )
        
        analysis.raw_response = data.get("raw_response")
        
        return analysis
