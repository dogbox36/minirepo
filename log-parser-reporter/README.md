# Log Parser & Reporter

High-performance, streaming log analysis tool designed for large-scale log processing.
Generates comprehensive HTML reports and CSV summaries from JSONL and Text logs.

## Features

- **Streaming Architecture**: Processes large files without loading them entirely into memory.
- **Multi-Format Support**:
  - `JSON Lines`: Structured logs with automatic schema validation.
  - `Text Logs`: Regex-based parsing for legacy formats (e.g., access logs).
- **Robustness**: Handles malformed lines gracefully, reporting them separately.
- **Analytics**:
  - Latency distribution (P50, P95, P99).
  - Slowest request tracking.
  - Anomaly detection (sudden error rate spikes).
- **Reporting**:
  - Interactive HTML dashboard.
  - Machine-readable JSON/CSV exports.
- **Plugin System**: extensible `BaseParser` interface.

## Quickstart

### Installation
Requires Python 3.9+.

```bash
git clone <repo-url>
cd log-parser-reporter
pip install -e .
```

### Usage

**1. Parse logs and see summary in CLI:**
```bash
# Parse a single file
log-reporter parse --input /var/log/app.jsonl

# Parse entire directory (merges all supported files)
log-reporter parse --input logs/ --top 5
```

**2. Generate HTML Report:**
```bash
log-reporter report --input logs/ --output out/run_01
```

This will create:
- `out/run_01/<timestamp>/report.html`
- `out/run_01/<timestamp>/summary.json`
- `out/run_01/<timestamp>/events_failed.csv`

## Project Structure
```text
log-parser-reporter/
├── src/log_reporter/
│   ├── analyzer.py        # Streaming statistics & anomaly detection
│   ├── models.py          # Pydantic data models
│   ├── reporter.py        # Report generation logic
│   ├── cli.py             # Typer CLI application
│   └── parsers/           # Parser implementations
├── templates/             # Jinja2 HTML templates
├── tests/                 # Unit & Integration tests
├── samples/               # Sample log generator
└── Makefile               # Development tasks
```

## Design Decisions

### Why Streaming?
To handle gigabyte-scale logs typically found in production, we avoid `pandas` or loading lists into memory. 
- **Memory**: O(1) mostly, except for `slowest_requests` (heap O(K)) and `durations` list for exact percentiles (O(N)). 
- **Optimization**: For true "infinite" streams, we would use `t-digest` or reservoir sampling for percentiles to keep memory bounded.

### Why Pydantic?
Ensures strict type validation at the edge. Invalid logs are rejected early, preventing runtime errors in the analyzer.

### Why Typer & Rich?
Provides a top-tier Developer Experience (DX) with auto-completion, help generation, and beautiful terminal output out-of-the-box.

## Development

Run tests:
```bash
make test
```

Lint code:
```bash
make lint
```

Generate sample data:
```bash
python gen_samples.py
```

## Roadmap
1. [ ] **Streaming Percentiles**: Replace list-based P95 with `t-digest` for constant memory usage.
2. [ ] **Parallel Processing**: Use `multiprocessing` to parse multiple files concurrently.
3. [ ] **OpenTelemetry**: Export metrics to OTLP collector.
4. [ ] **Database Sink**: Option to write parsed events to SQLite/Postgres.
5. [ ] **Interactive Charts**: Use `Plotly` or `Apache ECharts` in HTML report.
6. [ ] **Live Tailing**: `tail -f` support for real-time monitoring.
