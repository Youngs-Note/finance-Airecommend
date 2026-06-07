from pydantic import BaseModel, Field


class AIProductExplanation(BaseModel):
    product_id: str
    summary: str = Field(min_length=1, max_length=300)
    warnings: list[str] = Field(default_factory=list, max_length=3)


class AIRecommendationExplanations(BaseModel):
    items: list[AIProductExplanation] = Field(default_factory=list, max_length=10)


class ComparisonSummary(BaseModel):
    summary: str
    highlights: list[str]
    warnings: list[str]
    ai_generated: bool = False


class AIComparisonSummary(BaseModel):
    summary: str = Field(min_length=1, max_length=300)
    highlights: list[str] = Field(default_factory=list, max_length=5)
    warnings: list[str] = Field(default_factory=list, max_length=3)
