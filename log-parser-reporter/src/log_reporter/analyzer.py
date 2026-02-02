from typing import Dict, List, Counter, Tuple
from collections import defaultdict
import statistics
import heapq
from log_reporter.models import LogEvent, LogLevel

class LogAnalyzer:
    def __init__(self, top_n: int = 10):
        self.total_requests = 0
        self.level_counts = Counter()
        self.service_counts = Counter()
        self.status_codes = Counter()
        self.durations: List[float] = [] # Storing all durations for p50/p95/p99 (optimize if memory constraint)
        self.start_time = None
        self.end_time = None
        
        # Slowest requests: MinHeap of (duration, request_id, msg) -> keep largest N
        self.top_n = top_n
        self.slowest_requests = [] # Heap
        
        # Time buckets for error rate (per minute)
        # Format: "YYYY-MM-DD HH:MM" -> {"total": int, "error": int}
        self.time_buckets = defaultdict(lambda: {"total": 0, "error": 0})
        
        # Anomaly detection
        self.anomalies = [] 

    def process_event(self, event: LogEvent):
        if not event:
            return

        self.total_requests += 1
        self.level_counts[event.level] += 1
        self.service_counts[event.service] += 1
        
        if event.status_code:
            self.status_codes[event.status_code] += 1
            
        if event.duration_ms is not None:
             self.durations.append(event.duration_ms)
             # Update slowest requests heap
             # We want to keep Top N LARGEST.
             # Heapq is min-heap. So we push, and if size > N, we pop smallest.
             item = (event.duration_ms, event.request_id, event.message)
             if len(self.slowest_requests) < self.top_n:
                 heapq.heappush(self.slowest_requests, item)
             else:
                 heapq.heappushpop(self.slowest_requests, item)

        # Time range
        if self.start_time is None or event.timestamp < self.start_time:
            self.start_time = event.timestamp
        if self.end_time is None or event.timestamp > self.end_time:
            self.end_time = event.timestamp
            
        # Bucketing
        bucket_key = event.timestamp.strftime("%Y-%m-%d %H:%M")
        self.time_buckets[bucket_key]["total"] += 1
        if event.level in (LogLevel.ERROR, LogLevel.FATAL):
            self.time_buckets[bucket_key]["error"] += 1

    def compute_percentiles(self) -> Dict[str, float]:
        if not self.durations:
            return {"p50": 0, "p95": 0, "p99": 0}
        
        # Sorting is O(N log N) - acceptable for reasonably large N
        sorted_durs = sorted(self.durations)
        n = len(sorted_durs)
        
        def get_p(p):
            k = int(p * n)
            return sorted_durs[min(k, n-1)]
            
        return {
            "p50": get_p(0.50),
            "p95": get_p(0.95),
            "p99": get_p(0.99)
        }
        
    def detect_anomalies(self, threshold_ratio: float = 0.1, min_reqs: int = 10):
        # Simple rule: if error rate > threshold in a bucket
        for time_key, counts in self.time_buckets.items():
            total = counts["total"]
            if total < min_reqs: 
                continue
            error_rate = counts["error"] / total
            if error_rate > threshold_ratio:
                self.anomalies.append({
                    "time": time_key,
                    "error_rate": round(error_rate, 2),
                    "total": total,
                    "errors": counts["error"]
                })
        
        # Sort anomalies by time
        self.anomalies.sort(key=lambda x: x["time"])

    def get_summary(self) -> Dict:
        percentiles = self.compute_percentiles()
        # Slowest requests: sort desc
        sorted_slowest = sorted(self.slowest_requests, key=lambda x: x[0], reverse=True)
        
        return {
            "total_requests": self.total_requests,
            "duration_stats": percentiles,
            "level_counts": dict(self.level_counts),
            "service_counts": dict(self.service_counts),
            "status_codes": dict(self.status_codes),
            "slowest_requests": [
                {"duration": d, "request_id": r, "msg": m} for d, r, m in sorted_slowest
            ],
            "anomalies": self.anomalies,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None
        }
