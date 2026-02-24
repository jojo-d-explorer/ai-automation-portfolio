#!/usr/bin/env python3
"""Local web server for the job search dashboard.

Usage:
  python3 JC3/serve.py
  Then open http://localhost:8765 in your browser.
"""

import csv
import json
import os
import re
import webbrowser
from collections import Counter
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.html")
PORT = 8765


# ---------------------------------------------------------------------------
# Database discovery (mirrors dashboard.py)
# ---------------------------------------------------------------------------

def find_databases():
    users = {}

    joey_path = os.path.join(_REPO, "results", "master_job_database.csv")
    if os.path.exists(joey_path):
        users["joey"] = ("Joey Clark", joey_path)

    for_others = os.path.join(_REPO, "results", "For_Others")
    if os.path.isdir(for_others):
        for name in sorted(os.listdir(for_others)):
            folder = os.path.join(for_others, name)
            if not os.path.isdir(folder):
                continue
            candidate = os.path.join(folder, f"Master_Job_Database_{name}.csv")
            if os.path.exists(candidate):
                slug = name.lower().replace("_", " ").split()[0]
                if slug in users:
                    slug = name.lower().replace("_", "-")
                users[slug] = (name.replace("_", " "), candidate)

    return users


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

SECTOR_MAP = {
    "Fintech": ["fintech", "crypto", "blockchain", "banking", "payments", "tax tech",
                "alternative investments", "market intelligence", "identity", "fraud",
                "insurtech", "web3"],
    "Health Tech": ["health", "wellness", "fitness", "biotech"],
    "AI / ML": ["ai/", "ai ", "/ai", " ai", "speech tech", "ml"],
    "SaaS / Software": ["saas", "developer tools", "devtools", "cloud", "automation",
                        "martech", "adtech", "analytics"],
    "E-commerce / Consumer": ["e-commerce", "commerce", "consumer tech", "marketplace",
                               "restaurant tech", "social media", "media/sports"],
}


def normalize_sector(raw):
    if not raw:
        return "Other"
    low = raw.lower()
    for parent, keywords in SECTOR_MAP.items():
        if any(kw in low for kw in keywords):
            return parent
    return raw


def parse_score(row):
    try:
        return float(row["Score"])
    except (ValueError, KeyError):
        return None


def build_data(display_name, db_path):
    with open(db_path, newline="", encoding="utf-8") as f:
        jobs = list(csv.DictReader(f))

    scored = [(j, parse_score(j)) for j in jobs if parse_score(j) is not None]

    avg = round(sum(s for _, s in scored) / len(scored), 1) if scored else 0
    top_score = int(max((s for _, s in scored), default=0))
    low_score = int(min((s for _, s in scored), default=0))

    top10 = [
        {
            "score": int(s),
            "company": j["Company"],
            "title": j["Job_Title"],
            "sector": normalize_sector(j.get("Sector", "")),
            "url": j.get("URL", ""),
        }
        for j, s in sorted(scored, key=lambda x: x[1], reverse=True)[:10]
    ]

    sector_data: dict[str, list[float]] = {}
    for j, s in scored:
        sec = normalize_sector(j.get("Sector", ""))
        sector_data.setdefault(sec, []).append(s)

    sectors = sorted(
        [{"name": k, "count": len(v), "avg": round(sum(v) / len(v), 1)}
         for k, v in sector_data.items()],
        key=lambda x: x["count"], reverse=True
    )

    apply_next = [
        {
            "score": int(s),
            "company": j["Company"],
            "title": j["Job_Title"],
            "sector": normalize_sector(j.get("Sector", "")),
            "url": j.get("URL", ""),
        }
        for j, s in sorted(scored, key=lambda x: x[1], reverse=True)
        if s >= 85 and not j.get("Applied_Date", "").strip()
    ]

    status_counts = dict(Counter(j.get("Status", "Unknown") for j in jobs))

    return {
        "display_name": display_name,
        "total_jobs": len(jobs),
        "scored_jobs": len(scored),
        "avg_score": avg,
        "max_score": top_score,
        "min_score": low_score,
        "apply_next_count": len(apply_next),
        "top10": top10,
        "sectors": sectors,
        "apply_next": apply_next,
        "status_counts": status_counts,
    }


# ---------------------------------------------------------------------------
# HTTP server
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress request noise

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path in ("/", "/dashboard.html"):
            self._serve_file(_HTML, "text/html; charset=utf-8")

        elif parsed.path == "/api/users":
            users = find_databases()
            payload = [{"slug": k, "name": v[0]} for k, v in users.items()]
            self._serve_json(payload)

        elif parsed.path == "/api/data":
            qs = parse_qs(parsed.query)
            slug = qs.get("user", [None])[0]
            users = find_databases()
            if slug and slug in users:
                display_name, db_path = users[slug]
                self._serve_json(build_data(display_name, db_path))
            else:
                self.send_error(404, "User not found")

        else:
            self.send_error(404)

    def _serve_file(self, path, content_type):
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"  Job Search Dashboard")
    print(f"  Running at {url}")
    print(f"  Press Ctrl+C to stop\n")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
