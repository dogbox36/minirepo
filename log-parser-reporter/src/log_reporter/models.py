from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict

class LogLevel(str, Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    FATAL = "FATAL"
    UNKNOWN = "UNKNOWN"

class LogEvent(BaseModel):
    model_config = ConfigDict(extra='ignore')

    timestamp: datetime
    level: LogLevel
    message: str
    service: str = "unknown"
    request_id: Optional[str] = None
    status_code: Optional[int] = None
    duration_ms: Optional[float] = None
