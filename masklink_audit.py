"""Audit consistency/collisions of row-aligned pseudonymized CSV exports."""
import argparse
import csv
import io
import json
from pathlib import Path


def table(text):
    rows = list(csv.reader(io.StringIO(text), strict=True))
    if not rows or not rows[0] or any(not x for x in rows[0]) or len(set(rows[0])) != len(rows[0]):
        raise ValueError("CSV requires unique nonempty column names")
    if any(len(r) != len(rows[0]) for r in rows[1:]):
        raise ValueError("ragged CSV row")
    return rows[0], rows[1:]


def audit(pairs):
    if not isinstance(pairs, list) or not pairs:
        raise ValueError("nonempty export pair list required")
    forward, reverse, findings, count = {}, {}, [], 0
    for pair_index, p in enumerate(pairs):
        if not isinstance(p, dict) or set(p) != {"source", "masked", "domains"} or not isinstance(p["domains"], dict) or not p["domains"]:
            raise ValueError("pair requires source CSV text, masked CSV text, and nonempty column-to-domain map")
        if not all(isinstance(k, str) and isinstance(v, str) and k and v for k, v in p["domains"].items()):
            raise ValueError("domain names must be nonempty strings")
        sh, sr = table(p["source"]); mh, mr = table(p["masked"])
        if sh != mh:
            raise ValueError("pair %d: schema or column order differs" % pair_index)
        if len(sr) != len(mr):
            raise ValueError("pair %d: row count differs; row alignment is required" % pair_index)
        if set(p["domains"]) - set(sh):
            raise ValueError("pair %d: declared column missing" % pair_index)
        columns = {sh.index(k): v for k, v in p["domains"].items()}
        for row_index, (s, m) in enumerate(zip(sr, mr), 1):
            count += 1
            for ci, domain in columns.items():
                original, token = s[ci], m[ci]
                loc = {"pair": pair_index, "row": row_index, "column": ci, "domain": domain}
                def flag(code):
                    findings.append({**loc, "code": code})
                if not original:
                    if token:
                        flag("empty_identifier_changed")
                    continue
                if not token:
                    flag("identifier_erased"); continue
                if original == token:
                    flag("identifier_unchanged")
                key, back = (domain, original), (domain, token)
                if key in forward and forward[key] != token:
                    flag("inconsistent_token")
                if back in reverse and reverse[back] != original:
                    flag("token_collision")
                forward.setdefault(key, token); reverse.setdefault(back, original)
            # Non-ID columns must remain exact: makes row alignment observable when an anchor exists.
            for ci in range(len(sh)):
                if ci not in columns and s[ci] != m[ci]:
                    findings.append({"pair": pair_index, "row": row_index, "column": ci, "code": "unmapped_column_changed"})
    return {"ok": not findings, "pairs": len(pairs), "rows": count, "distinct_domain_identifiers": len(forward), "findings": findings,
            "limitations": "Row order must be preserved. No anonymity or transformation-security guarantee. Reports omit cell values."}


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("manifest"); a = p.parse_args()
    try:
        manifest_path = Path(a.manifest); configs = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(configs, list) or not configs:
            raise ValueError("manifest must be a nonempty list")
        pairs = []
        for c in configs:
            if not isinstance(c, dict) or set(c) != {"source", "masked", "domains"}:
                raise ValueError("manifest pair requires source, masked, domains only")
            pairs.append({"source": (manifest_path.parent / c["source"]).read_text(encoding="utf-8-sig"),
                          "masked": (manifest_path.parent / c["masked"]).read_text(encoding="utf-8-sig"), "domains": c["domains"]})
        r = audit(pairs); print(json.dumps(r, sort_keys=True)); return 0 if r["ok"] else 1
    except (ValueError, OSError, TypeError, csv.Error) as e:
        print(json.dumps({"error": str(e)})); return 2


if __name__ == "__main__":
    raise SystemExit(main())
