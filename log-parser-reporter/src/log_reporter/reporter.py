import csv
import json
from pathlib import Path
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader

class Reporter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def write_failed_events(self, failed_events: List[tuple]):
        # failed_events = [(line, error), ...]
        filepath = self.output_dir / "events_failed.csv"
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["original_line", "error_reason"])
            for line, error in failed_events:
                # Truncate line if too long?
                writer.writerow([line[:1000], error])
                
    def write_summary_json(self, summary: Dict):
        filepath = self.output_dir / "summary.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

    def generate_html_report(self, summary: Dict, template_dir: Path):
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("report.html.j2")
        
        # Add simpler variables for template if needed
        html_content = template.render(
            summary=summary, 
            generated_at=summary.get("end_time") # Just using end_time as ref
        )
        
        filepath = self.output_dir / "report.html"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
