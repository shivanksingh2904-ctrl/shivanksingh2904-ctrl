#!/usr/bin/env python3
"""Create an SVG chart from GitHub's recent public events feed."""
import json, os, urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone

user = os.environ.get("GITHUB_USERNAME", "shivanksingh2904-ctrl")
url = f"https://api.github.com/users/{user}/events/public?per_page=100"
req = urllib.request.Request(url, headers={
    "Accept": "application/vnd.github+json",
    "User-Agent": "github-profile-readme-activity-chart"
})
token = os.environ.get("GITHUB_TOKEN")
if token:
    req.add_header("Authorization", f"Bearer {token}")

with urllib.request.urlopen(req, timeout=25) as resp:
    events = json.load(resp)

today = datetime.now(timezone.utc).date()
dates = [today - timedelta(days=n) for n in range(13, -1, -1)]
counts = Counter()
for event in events:
    stamp = event.get("created_at")
    if stamp:
        try:
            day = datetime.fromisoformat(stamp.replace("Z", "+00:00")).date()
            if day in dates:
                counts[day] += 1
        except ValueError:
            continue

values = [counts[d] for d in dates]
maximum = max(values, default=0) or 1
W, H, L, R, T, B = 1100, 300, 56, 28, 52, 48
plot_h = H - T - B
plot_w = W - L - R
gap = 12
bar_w = (plot_w - gap * 13) / 14
svg = [
 f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
 '<title id="title">Recent public GitHub events</title>',
 '<desc id="desc">Daily public event counts for the last 14 days based on the GitHub events API.</desc>',
 '<defs><linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#67E8F9"/><stop offset="1" stop-color="#8B5CF6"/></linearGradient></defs>',
 '<rect width="100%" height="100%" rx="18" fill="#0B1220"/>',
 '<text x="30" y="30" font-family="Arial,sans-serif" font-size="17" font-weight="700" fill="#E2E8F0">PUBLIC GITHUB EVENTS · LAST 14 DAYS</text>'
]
for tick in range(4):
    val = round(maximum * tick / 3)
    y = T + plot_h - plot_h * tick / 3
    svg.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W-R}" y2="{y:.1f}" stroke="#334155" stroke-dasharray="4 6"/>')
    svg.append(f'<text x="{L-12}" y="{y+4:.1f}" text-anchor="end" font-family="Arial,sans-serif" font-size="11" fill="#94A3B8">{val}</text>')
for i, (day, value) in enumerate(zip(dates, values)):
    x = L + i * (bar_w + gap)
    bh = plot_h * value / maximum
    y = T + plot_h - bh
    svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{max(2,bh):.1f}" rx="5" fill="url(#bar)"><title>{day.isoformat()}: {value} public events</title></rect>')
    if value:
        svg.append(f'<text x="{x+bar_w/2:.1f}" y="{max(T+12,y-7):.1f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#F8FAFC">{value}</text>')
    svg.append(f'<text x="{x+bar_w/2:.1f}" y="{H-24}" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#CBD5E1">{day.strftime("%d %b")}</text>')
svg.append(f'<text x="{W-R}" y="{H-7}" text-anchor="end" font-family="Arial,sans-serif" font-size="10" fill="#64748B">Generated {today.isoformat()} UTC · Public events only</text>')
svg.append('</svg>')
os.makedirs("assets", exist_ok=True)
with open("assets/activity-graph.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print(f"Updated activity graph for {user}; events counted: {sum(values)}")
