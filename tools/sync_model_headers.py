# tools/sync_model_headers.py
import yaml, re, pathlib, collections

HEADER_RE = re.compile(r"/\*---(.*?)---\*/", re.S)

def extract_header(sql):
    m = HEADER_RE.search(sql)
    if not m: return None
    return yaml.safe_load(m.group(1))

def main(root="models"):
    by_dir = collections.defaultdict(list)
    for p in pathlib.Path(root).rglob("*.sql"):
        meta = extract_header(p.read_text())
        if not meta: continue
        model = meta.get("model", {})
        cols  = meta.get("columns", [])
        entry = {
          "name": model["name"],
          "description": model.get("description",""),
          "columns": cols,
        }
        by_dir[str(p.parent)].append(entry)

    for d, models in by_dir.items():
        y = {"version": 2, "models": models}
        out = pathlib.Path(d) / "schema.generated.yml"
        # Only write when content changes to avoid unnecessary rebuilds
        new_content = yaml.dump(y, sort_keys=False)
        if out.exists():
            if out.read_text() != new_content:
                out.write_text(new_content)
        else:
            out.write_text(new_content)

if __name__ == "__main__":
    main()
