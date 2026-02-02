from abc import ABC, abstractmethod
from typing import Generator, Tuple, Optional
from log_reporter.models import LogEvent

# Tuple[Optional[LogEvent], Optional[str]]
# Yields: (Parsed Event OR None, Error Reason OR None)
ParseResult = Tuple[Optional[LogEvent], Optional[str]]

class BaseParser(ABC):
    @abstractmethod
    def parse_line(self, line: str) -> ParseResult:
        """Parse a single line into a LogEvent or return an error reason."""
        pass
    
    def parse(self, lines: Generator[str, None, None]) -> Generator[ParseResult, None, None]:
        """Stream processing of lines."""
        for line in lines:
            yield self.parse_line(line)
