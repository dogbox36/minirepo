import re
from datetime import datetime
from typing import Optional, Pattern
from pydantic import ValidationError

from log_reporter.parsers.base import BaseParser, ParseResult
from log_reporter.models import LogEvent, LogLevel

# Sample Regex based on: 2026-02-02T12:34:56.789Z INFO service=api request_id=abc123 status=200 duration_ms=42 msg="GET /users"
# We need to capture: timestamp, level, key-value pairs?
# Or just strict regex for the example?
# Let's make it robust:
# 1. Start with Timestamp (ISO)
# 2. Level
# 3. Rest of line key=value pairs or msg="..."

DEFAULT_PATTERN = re.compile(
    r'^(?P<timestamp>\S+)\s+(?P<level>\w+)\s+(?P<rest>.*)$'
)

KV_PATTERN = re.compile(r'(?P<key>\w+)=(?:"(?P<quoted_val>[^"]*)"|(?P<val>\S+))')

class TextLogParser(BaseParser):
    def __init__(self, main_pattern: Pattern = DEFAULT_PATTERN):
        self.main_pattern = main_pattern

    def parse_line(self, line: str) -> ParseResult:
        line = line.strip()
        if not line:
             return None, "Empty line"

        match = self.main_pattern.match(line)
        if not match:
            return None, "Regex no match"

        groups = match.groupdict()
        
        raw_level = groups.get("level", "UNKNOWN").upper()
        try:
            level = LogLevel(raw_level)
        except ValueError:
            level = LogLevel.UNKNOWN
            
        # Parse KV pairs from 'rest'
        rest = groups.get("rest", "")
        data = {
            "timestamp": groups.get("timestamp"),
            "level": level,
            "message": "" # Will fill later
        }

        # Extract structured data
        for kv_match in KV_PATTERN.finditer(rest):
            k = kv_match.group("key")
            v = kv_match.group("quoted_val") if kv_match.group("quoted_val") is not None else kv_match.group("val")
            
            # Map known keys
            if k == "msg" or k == "message":
                data["message"] = v
            elif k == "duration_ms":
                try:
                    data["duration_ms"] = float(v)
                except ValueError:
                    pass
            elif k == "status":
                try:
                    data["status_code"] = int(v)
                except ValueError:
                    pass
            elif k in ["service", "request_id"]:
                data[k] = v
        
        # Fallback if message not in KV
        if not data.get("message"):
            data["message"] = rest # If parsing failed partial, just dump rest? Or maybe not.
            # Requirement says "msg" field exists.
        
        try:
            event = LogEvent(**data)
            return event, None
        except ValidationError as e:
            return None, f"Schema Error: {e}"
