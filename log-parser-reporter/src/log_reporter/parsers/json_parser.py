import json
from datetime import datetime
from typing import Any, Dict
from pydantic import ValidationError

from log_reporter.parsers.base import BaseParser, ParseResult
from log_reporter.models import LogEvent, LogLevel

class JsonLogParser(BaseParser):
    def parse_line(self, line: str) -> ParseResult:
        line = line.strip()
        if not line:
            return None, "Empty line"
            
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            return None, "Invalid JSON"
            
        # Map logical fields to standard model if keys differ.
        # Assuming sample format is close to model fields for this example,
        # but robust parser should handle alias mappings.
        
        # Normalize fields
        try:
            # Handle timestamp: can be string ISO or epoch or something else.
            # Assuming ISO 8601 string for now based on requirements sample.
            # If Pydantic is smart enough, passing the string to datetime field works.
            
            # Auto-mapping level
            if "level" in data:
                try:
                    data["level"] = LogLevel(data["level"].upper())
                except ValueError:
                    data["level"] = LogLevel.UNKNOWN
            else:
                 data["level"] = LogLevel.UNKNOWN
                 
            event = LogEvent(**data)
            return event, None
            
        except ValidationError as e:
            return None, f"Schema Error: {e}"
        except Exception as e:
             return None, f"Unexpected Error: {e}"
