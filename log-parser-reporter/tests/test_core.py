import pytest
from log_reporter.parsers.json_parser import JsonLogParser
from log_reporter.parsers.text_parser import TextLogParser
from log_reporter.analyzer import LogAnalyzer
from log_reporter.models import LogEvent, LogLevel
from datetime import datetime

class TestParsers:
    def test_json_parser_valid(self):
        parser = JsonLogParser()
        line = '{"timestamp": "2023-01-01T12:00:00", "level": "INFO", "message": "hello", "duration_ms": 100}'
        event, err = parser.parse_line(line)
        assert event is not None
        assert event.level == LogLevel.INFO
        assert event.duration_ms == 100.0

    def test_json_parser_invalid(self):
        parser = JsonLogParser()
        event, err = parser.parse_line("{bad json")
        assert event is None
        assert "Invalid JSON" in err

    def test_text_parser_valid(self):
        parser = TextLogParser()
        line = '2023-01-01T12:00:00 INFO service=api duration_ms=50 msg="hello world"'
        event, err = parser.parse_line(line)
        assert event is not None
        assert event.service == "api"
        assert event.duration_ms == 50.0
        assert event.message == "hello world"

class TestAnalyzer:
    def test_percentiles(self):
        analyzer = LogAnalyzer()
        for i in range(1, 101):
            event = LogEvent(
                timestamp=datetime.now(),
                level=LogLevel.INFO,
                message="test",
                duration_ms=float(i)
            )
            analyzer.process_event(event)
            
        stats = analyzer.compute_percentiles()
        assert stats["p50"] == 51.0
        assert stats["p95"] == 96.0
        assert stats["p99"] == 100.0

    def test_slowest_requests(self):
        analyzer = LogAnalyzer(top_n=2)
        durations = [10, 50, 20, 100, 5]
        for d in durations:
            analyzer.process_event(LogEvent(
                timestamp=datetime.now(),
                level=LogLevel.INFO, # Required field
                message="msg",
                duration_ms= float(d) # Required field type
            ))
            
        summary = analyzer.get_summary()
        slowest = summary["slowest_requests"]
        assert len(slowest) == 2
        assert slowest[0]["duration"] == 100.0
        assert slowest[1]["duration"] == 50.0
