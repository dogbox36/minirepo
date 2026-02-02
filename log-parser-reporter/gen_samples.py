import json
from datetime import datetime
import random
import sys

def generate_samples():
    services = ["auth-service", "payment-api", "user-service"]
    levels = ["INFO", "INFO", "INFO", "WARN", "ERROR"]
    
    # 1. Generate JSONL
    with open("samples/app.jsonl", "w") as f:
        for i in range(100):
            event = {
                "timestamp": datetime.now().isoformat(),
                "level": random.choice(levels),
                "service": random.choice(services),
                "request_id": f"req-{i}",
                "msg": "Processed request",
                "status_code": random.choice([200, 200, 200, 500, 404]),
                "duration_ms": random.randint(10, 500)
            }
            # Add anomaly
            if 80 < i < 90:
                event["level"] = "ERROR"
                event["status_code"] = 503
            
            f.write(json.dumps(event) + "\n")
            
    # 2. Generate Text Logs
    with open("samples/access.log", "w") as f:
        for i in range(100):
            ts = datetime.now().isoformat()
            lvl = random.choice(levels)
            svc = random.choice(services)
            dur = random.randint(5, 300)
            line = f'{ts} {lvl} service={svc} request_id=tx-{i} status=200 duration_ms={dur} msg="GET /api/v1/resource"'
            f.write(line + "\n")
            
    # 3. Bad file
    with open("samples/bad.log", "w") as f:
        f.write("This is not a log line\n")
        f.write("{broken json\n")

if __name__ == "__main__":
    generate_samples()
