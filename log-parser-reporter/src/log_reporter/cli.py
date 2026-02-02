import typer
import sys
import glob
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from datetime import datetime

from log_reporter.parsers.json_parser import JsonLogParser
from log_reporter.parsers.text_parser import TextLogParser
from log_reporter.analyzer import LogAnalyzer
from log_reporter.reporter import Reporter

app = typer.Typer(help="High-performance log parsing CLI")
console = Console()

def get_files(input_path: Path) -> List[Path]:
    if input_path.is_file():
        return [input_path]
    elif input_path.is_dir():
        files = []
        files.extend(input_path.glob("*.log"))
        files.extend(input_path.glob("*.jsonl"))
        files.extend(input_path.glob("*.txt"))
        return files
    return []

# Common logic for parsing
def process_logs(
    input: Path, 
    strict: bool,
    analyzer: LogAnalyzer
) -> List[tuple]:
    failed_events = []
    files = get_files(input)
    
    if not files:
        console.print(f"[red]No files found in {input}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[green]Processing {len(files)} files...[/green]")
    
    parsers = [JsonLogParser(), TextLogParser()]
    
    for file in files:
        console.print(f"Reading {file.name}...")
        with open(file, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                parsed = False
                error = "No parser matched"
                
                # Plugin loop: first success wins
                for parser in parsers:
                    event, err = parser.parse_line(line)
                    if event:
                        analyzer.process_event(event)
                        parsed = True
                        break
                    else:
                        error = err # Keep last error? Or most specific?
                        
                if not parsed:
                    failed_events.append((line.strip(), error))
                    if strict:
                        console.print(f"[bold red]Strict mode: Failed at {file.name}:{line_no} -> {error}[/bold red]")
                        raise typer.Exit(code=1)
                        
    return failed_events

@app.command()
def parse(
    input: Path = typer.Option(..., exists=True, help="Input file or directory"),
    strict: bool = typer.Option(False, help="Fail on first error"),
    top: int = typer.Option(10, help="Number of slowest requests to show")
):
    """Parse logs and print summary to console."""
    analyzer = LogAnalyzer(top_n=top)
    
    start = datetime.now()
    failed = process_logs(input, strict, analyzer)
    duration = (datetime.now() - start).total_seconds()
    
    analyzer.detect_anomalies()
    summary = analyzer.get_summary()
    
    # Print rich tables
    console.print(f"\n[bold]Completed in {duration:.2f}s[/bold]")
    console.print(f"Total Requests: {summary['total_requests']}")
    console.print(f"Failed Lines: {len(failed)}")
    
    # Latency Table
    table = Table(title="Latency Stats")
    table.add_column("Metric")
    table.add_column("Value (ms)")
    stats = summary["duration_stats"]
    table.add_row("P50", f"{stats['p50']:.2f}")
    table.add_row("P95", f"{stats['p95']:.2f}")
    table.add_row("P99", f"{stats['p99']:.2f}")
    console.print(table)
    
    # Status Codes
    s_table = Table(title="Status Codes")
    s_table.add_column("Code")
    s_table.add_column("Count")
    for k, v in summary["status_codes"].items():
        s_table.add_row(str(k), str(v))
    console.print(s_table)
    
    if summary["anomalies"]:
        console.print("\n[bold red]⚠️ Anomalies Detected![/bold red]")
        for a in summary["anomalies"]:
            console.print(f"  {a['time']}: {a['error_rate']*100:.1f}% Error Rate (Total: {a['total']})")

@app.command()
def report(
    input: Path = typer.Option(..., exists=True, help="Input file or directory"),
    output: Path = typer.Option(Path("out"), help="Output directory"),
    strict: bool = typer.Option(False, help="Fail on first error"),
    top: int = typer.Option(10, help="Number of slowest requests to show"),
    format: str = typer.Option("both", help="Output format: html, csv, or both")
):
    """Parse logs and generate report files."""
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output / run_id
    reporter = Reporter(run_dir)
    
    analyzer = LogAnalyzer(top_n=top)
    failed = process_logs(input, strict, analyzer)
    analyzer.detect_anomalies()
    summary = analyzer.get_summary()

    # Always write core artifacts
    reporter.write_summary_json(summary)
    reporter.write_failed_events(failed)
    
    console.print(f"\n[green]Generating reports in {run_dir}...[/green]")
    
    if format in ("both", "html"):
        # Assuming templates are in package or working dir
        # For simplicity, look in cwd/templates
        template_dir = Path("templates").resolve()
        if not template_dir.exists():
            # Fallback for installed package? 
            # Ideally package data. For this repo, cwd is fine.
            console.print("[yellow]Template dir not found, skipping HTML[/yellow]")
        else:
            reporter.generate_html_report(summary, template_dir)
            console.print("  - HTML Report generated")

    console.print("[bold green]Done![/bold green]")

if __name__ == "__main__":
    app()
