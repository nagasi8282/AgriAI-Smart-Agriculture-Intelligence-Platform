from typing import Generic, Optional, TypeVar, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime, timezone

T = TypeVar("T")


class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Service status indicator")
    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="API Version")
    environment: str = Field(..., description="Runtime environment")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    database_status: str = Field(default="connected", description="Database connectivity state")
    services: Dict[str, str] = Field(default_factory=dict, description="Status of auxiliary services")


class StandardResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[T] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str
    message: str
    details: Optional[Any] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
