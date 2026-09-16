from pydantic import BaseModel, Field
from typing import Optional


class SourceLocation(BaseModel):
    page: int = Field(ge=1)
    text: str
    x0: Optional[float] = None
    y0: Optional[float] = None
    x1: Optional[float] = None
    y1: Optional[float] = None


class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    stated_total: Optional[float] = None
    source: SourceLocation


class DeliveryDate(BaseModel):
    value: str
    source: SourceLocation


class Offer(BaseModel):
    filename: str
    currency: Optional[str] = None
    line_items: list[LineItem] = []
    stated_grand_total: Optional[float] = None
    grand_total_source: Optional[SourceLocation] = None

    # Document dates
    date: Optional[DeliveryDate] = None
    revision_date: Optional[DeliveryDate] = None
    delivery_date: Optional[DeliveryDate] = None


class MatchResult(BaseModel):
    original_index: Optional[int] = None
    revised_index: Optional[int] = None
    status: str
    confidence: float
    reason: str


class Change(BaseModel):
    change_type: str
    description: str
    original_value: Optional[str] = None
    revised_value: Optional[str] = None
    original_source: Optional[SourceLocation] = None
    revised_source: Optional[SourceLocation] = None
    severity: str = "info"


class ComparisonResult(BaseModel):
    currency: Optional[str] = None
    matches: list[MatchResult] = []
    changes: list[Change] = []
    original_calculated_total: Optional[float] = None
    revised_calculated_total: Optional[float] = None
    original_stated_total: Optional[float] = None
    revised_stated_total: Optional[float] = None