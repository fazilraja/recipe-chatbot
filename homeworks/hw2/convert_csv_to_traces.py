"""Convert CSV results to trace JSON format for annotation tool."""

import csv
import json
from pathlib import Path
from datetime import datetime

# Input CSV file
csv_path = Path(__file__).parent.parent.parent / "results" / "results_20251005_222121.csv"

# Output directory (where annotation.py looks for traces)
traces_dir = Path(__file__).parent.parent.parent / "annotation" / "traces"
traces_dir.mkdir(parents=True, exist_ok=True)

# Read CSV and convert to trace format
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        query_id = row['id']
        query = row['query']
        response = row['response']

        # Create trace in the exact same format as backend/main.py saves them
        # (matching the format shown in hw2_solution_walkthrough.ipynb)
        trace = {
            "request": {
                "messages": [
                    {"role": "user", "content": query}
                ]
            },
            "response": {
                "messages": [
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": response}
                ]
            },
            # Pre-initialize fields for annotation tool
            "open_coding": "",
            "axial_coding_code": ""
        }

        # Save with a filename based on the query ID
        # Using a timestamp-like format to match existing trace naming
        trace_filename = f"trace_hw2_{query_id}.json"
        trace_path = traces_dir / trace_filename

        with open(trace_path, 'w', encoding='utf-8') as f:
            json.dump(trace, f, indent=2)

print(f"✅ Converted CSV to trace files in {traces_dir}")
print(f"Run the annotation tool with: python annotation/annotation.py")
