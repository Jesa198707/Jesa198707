"""Descarga las estadísticas de GitHub (incluidos repos privados) y las guarda en JSON.

Requiere la variable de entorno GH_TOKEN con un token personal del dueño de la cuenta
(scopes: repo, read:user). Uso:
    python fetch_stats.py <salida.json>
"""
import datetime as dt
import json
import os
import sys
import urllib.request

API = "https://api.github.com/graphql"
TOKEN = os.environ["GH_TOKEN"]


def gql(query, **variables):
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        sys.exit(f"GraphQL error: {body['errors']}")
    return body["data"]


viewer = gql("""{ viewer { createdAt
  repositories(ownerAffiliations: OWNER, isFork: false, first: 100) { totalCount nodes { isPrivate } } } }""")["viewer"]

created = dt.datetime.fromisoformat(viewer["createdAt"].replace("Z", "+00:00"))
now = dt.datetime.now(dt.timezone.utc)

CAL = """query($from: DateTime!, $to: DateTime!) { viewer { contributionsCollection(from: $from, to: $to) {
  totalCommitContributions restrictedContributionsCount
  contributionCalendar { weeks { contributionDays { date contributionCount } } } } } }"""

days, commits = {}, 0
start = created
while start < now:  # la API admite como máximo un año por consulta
    end = min(start + dt.timedelta(days=365) - dt.timedelta(seconds=1), now)
    c = gql(CAL, **{"from": start.isoformat(), "to": end.isoformat()})["viewer"]["contributionsCollection"]
    commits += c["totalCommitContributions"]
    for w in c["contributionCalendar"]["weeks"]:
        for d in w["contributionDays"]:
            days[d["date"]] = d["contributionCount"]
    start = end + dt.timedelta(seconds=1)

first = created.date().isoformat()
ds = sorted(k for k in days if first <= k <= now.date().isoformat())

longest, cur, run_start = (0, ds[0], ds[0]), 0, None
for k in ds:
    if days[k] > 0:
        if cur == 0:
            run_start = k
        cur += 1
        if cur > longest[0]:
            longest = (cur, run_start, k)
    else:
        cur = 0

# racha actual: si hoy aún no hay contribuciones, cuenta desde ayer
i = len(ds) - 1
if days[ds[i]] == 0:
    i -= 1
cs, cend = 0, ds[i] if i >= 0 else None
while i >= 0 and days[ds[i]] > 0:
    cs += 1
    i -= 1
current = (cs, ds[i + 1] if cs else None, cend if cs else None)

repos = viewer["repositories"]
out = {
    "total": sum(days[k] for k in ds),
    "commits": commits,
    "active": sum(1 for k in ds if days[k] > 0),
    "first": first,
    "last": ds[-1],
    "longest": longest,
    "current": current,
    "repos": repos["totalCount"],
    "private": sum(1 for r in repos["nodes"] if r["isPrivate"]),
}
with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False))
