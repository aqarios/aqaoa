#!/usr/bin/env python3

import os
import subprocess
import json
import requests
import base64
import tomli
import tempfile
import importlib.metadata as metadata
from pathlib import Path
from urllib.parse import urlparse

# ========== CONFIGURATION ==========
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LICENSES_DIR = PROJECT_ROOT / "licenses"
OUTPUT_FILE = PROJECT_ROOT / "THIRD_PARTY_LICENSES.txt"

EXCLUDE_PACKAGES = {
    "aqaoa",
    "custatevec"
}

MANUAL_ENTRIES = [
    {
        "name": "miniforge",
        "version": "latest",
        "authors": "conda-forge",
        "repository": "https://github.com/conda-forge/miniforge",
        "license": "BSD-3-Clause",
        "license_file": None,
        "description": "Minimal Conda installer",
        "license_mode": "copy"
    },
    {
        "name": "uv",
        "version": "latest",
        "authors": "Astral",
        "repository": "https://github.com/astral-sh/uv",
        "license": "MIT",
        "license_file": None,
        "description": "Ultra-fast Python package manager",
        "license_mode": "copy"
    },
    {
        "name": "custatevec",
        "version": "latest",
        "authors": "NVIDIA Corporation",
        "repository": "https://developer.nvidia.com/cuquantum-sdk",
        "license": "NVIDIA cuQuantum SDK License",
        "license_file": None,
        "description": "GPU-accelerated quantum state vector simulator (conda package)",
        "license_source": "https://docs.nvidia.com/cuda/cuquantum/latest/license.html#nvidia-cuquantum-sdk",
        "license_mode": "link"
    }
]

GITHUB_API_BASE = "https://api.github.com/repos"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Accept": "application/vnd.github.v3+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

# ========== HELPERS ==========

def run(cmd, capture=True):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=capture)
    if result.returncode != 0:
        print(f"❌ Error running: {cmd}")
        print(result.stderr)
        exit(1)
    return result.stdout.strip() if capture else None

def ensure_output_dirs():
    LICENSES_DIR.mkdir(parents=True, exist_ok=True)

def extract_repo_path(url):
    try:
        parsed = urlparse(url)
        if "github.com" not in parsed.netloc:
            return None
        parts = parsed.path.strip("/").split("/")
        return f"{parts[0]}/{parts[1]}"
    except:
        return None

def fetch_license_from_github(repo_url):
    repo_path = extract_repo_path(repo_url)
    if not repo_path:
        return None, None, None
    url = f"{GITHUB_API_BASE}/{repo_path}/license"
    try:
        res = requests.get(url, headers=HEADERS)
        if res.status_code == 200:
            data = res.json()
            spdx = data.get("license", {}).get("spdx_id", "UNKNOWN")
            content = base64.b64decode(data.get("content", "")).decode("utf-8")
            source_url = data.get("html_url")
            return spdx, content, source_url
    except Exception as e:
        print(f"⚠️ Failed to fetch license for {repo_url}: {e}")
    return None, None, None

def save_license_file(entry, text):
    name = entry["name"]
    version = entry.get("version", "unknown")
    repo_path = entry.get("repository", "unknown_repo")
    safe_repo = extract_repo_path(repo_path) or "unknown_repo"
    filename = LICENSES_DIR / f"{name}-{version}_{safe_repo.replace('/', '_')}.txt"

    if not filename.exists():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{name} v{version}\n")
            f.write(f"Author: {entry.get('authors', '')}\n")
            f.write(f"Repository: {entry.get('repository', '')}\n")
            f.write(f"License: {entry.get('license', '')}\n")
            f.write(f"Source: {entry.get('license_source', '')}\n\n")
            f.write(text)
    return filename

# ========== COLLECTORS ==========

def collect_rust(data_dir):
    print("🦀 Collecting Rust licenses...")
    run(f"cargo license --json > {data_dir}/all_licenses.json")
    run(f"cargo metadata --format-version 1 --no-deps | jq -r '.packages[].dependencies[] | select(.kind == null or .kind == \"normal\") | .name' > {data_dir}/direct_deps.txt")
    run(f"jq -sR 'split(\"\\n\") | map(select(. != \"\"))' {data_dir}/direct_deps.txt > {data_dir}/direct_names.json")
    run(f"jq --argjson names \"$(cat {data_dir}/direct_names.json)\" 'map(select(.name as $n | $names | index($n)))' {data_dir}/all_licenses.json > {data_dir}/rust_licenses.json")

def collect_conda(data_dir):
    print("🧪 Collecting Conda licenses...")
    run(f"conda list --json > {data_dir}/conda_packages.json")
    run(f"conda env export --from-history > {data_dir}/conda_history.yml")

    with open(data_dir / "conda_history.yml") as f:
        history = [line.strip("- \n") for line in f if line.strip().startswith("-")]

    with open(data_dir / "conda_packages.json") as f:
        full = json.load(f)

    out = []
    for pkg in full:
        if pkg["name"] in history and pkg["name"] not in EXCLUDE_PACKAGES:
            out.append({
                "name": pkg["name"],
                "version": pkg["version"],
                "authors": "",
                "repository": f"https://github.com/conda-forge/{pkg['name']}-feedstock",
                "license": "UNKNOWN",
                "license_file": None,
                "description": ""
            })

    with open(data_dir / "conda_licenses.json", "w") as f:
        json.dump(out, f, indent=2)

def collect_python(data_dir):
    print("🐍 Collecting Python licenses...")
    with open(PROJECT_ROOT / "pyproject.toml", "rb") as f:
        toml_data = tomli.load(f)

    deps = toml_data.get("project", {}).get("dependencies", [])
    direct_names = [d.split()[0].split("=")[0].lower() for d in deps]

    out = []
    for dist in metadata.distributions():
        name = dist.metadata["Name"].lower()
        if name not in direct_names or name in EXCLUDE_PACKAGES:
            continue
        meta = dist.metadata
        urls = meta.get_all("Project-URL") or []
        homepage = meta.get("Home-page", "")
        repo = next((u.split(",")[-1].strip() for u in urls if "github.com" in u.lower()), homepage)
        out.append({
            "name": meta["Name"],
            "version": dist.version,
            "authors": meta.get("Author", ""),
            "repository": repo,
            "license": meta.get("License", "UNKNOWN"),
            "license_file": None,
            "description": meta.get("Summary", "")
        })

    with open(data_dir / "python_licenses.json", "w") as f:
        json.dump(out, f, indent=2)

# ========== LICENSE FETCHER ==========

def fetch_all_licenses(data_dir):
    print("📦 Fetching licenses from GitHub...")
    auto_discovered = []
    for fpath in ["rust_licenses.json", "conda_licenses.json", "python_licenses.json"]:
        full_path = data_dir / fpath
        if full_path.exists():
            with open(full_path) as f:
                auto_discovered.extend(json.load(f))

    auto_discovered = [entry for entry in auto_discovered if entry["name"] not in EXCLUDE_PACKAGES]
    combined = auto_discovered + MANUAL_ENTRIES

    for entry in combined:
        name = entry["name"]
        repo = entry.get("repository", "")
        license_mode = entry.get("license_mode", "fetch")

        if license_mode == "link":
            print(f"🔗 Linking license for: {name}")
            text = f"See license: {entry.get('license_source') or '(no URL provided)'}"
            entry["license_source"] = entry.get("license_source") or "(no URL provided)"
            save_license_file(entry, text)
            continue

        if license_mode == "copy":
            spdx, text, url = fetch_license_from_github(repo)
            if text:
                entry["license"] = spdx
                entry["license_source"] = url
                save_license_file(entry, text)
            else:
                print(f"⚠️ Failed to fetch license for {name}")
            continue

        spdx, text, url = fetch_license_from_github(repo)
        if text:
            entry["license"] = spdx
            entry["license_source"] = url
            save_license_file(entry, text)
        else:
            print(f"⚠️ Could not fetch license for {name} ({repo})")

    with open(data_dir / "licenses.json", "w") as f:
        json.dump(combined, f, indent=2)

# ========== MERGE ==========

def merge_license_files():
    print("📜 Generating THIRD_PARTY_LICENSES.txt...")
    entries = []
    for file in sorted(LICENSES_DIR.glob("*.txt")):
        with open(file, encoding="utf-8") as f:
            content = f.read().strip()
            entries.append("-" * 80 + "\n" + content)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(entries))
    print(f"✅ Written: {OUTPUT_FILE}")

# ========== MAIN ==========

def main():
    ensure_output_dirs()
    with tempfile.TemporaryDirectory() as tmp:
        data_dir = Path(tmp)
        print(f"📁 Using temporary directory: {data_dir}")
        collect_rust(data_dir)
        collect_conda(data_dir)
        collect_python(data_dir)
        fetch_all_licenses(data_dir)
        merge_license_files()
    print("\n🎉 All licenses saved in ./licenses and ./THIRD_PARTY_LICENSES.txt")

if __name__ == "__main__":
    main()

