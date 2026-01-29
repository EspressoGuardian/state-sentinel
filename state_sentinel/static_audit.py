
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

GODOT_BIN = os.environ.get("GODOT_BIN", "godot")

def check_file(file_info):
    """Runs godot --check-only on a single file."""
    file_path, project_path = file_info
    cmd = [GODOT_BIN, "--headless", "--path", project_path, "--check-only", file_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return file_path, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return file_path, "TIMEOUT"
    except Exception as e:
        return file_path, str(e)
    return file_path, None

def run_static_audit(project_path=".", max_workers=None):
    if not max_workers:
        max_workers = os.cpu_count() or 4
    
    # Locate project.godot to confirm root
    if not os.path.exists(os.path.join(project_path, "project.godot")):
        # If not in root, try looking in 'game' subdir as per standard structure
        if os.path.exists(os.path.join(project_path, "game", "project.godot")):
            project_path = os.path.join(project_path, "game")
        else:
            print(f"Error: No project.godot found in {project_path}")
            return 1

    print("=" * 60)
    print(f" STATIC AUDIT | Scanning {project_path}")
    print("=" * 60)

    scripts = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".gd"):
                full_path = os.path.join(root, file)
                # Godot expects relative path from project root usually, but absolute works for check-only
                scripts.append((full_path, project_path))

    print(f"Auditing {len(scripts)} scripts using {max_workers} workers...")
    
    start_time = time.time()
    failures = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(check_file, scripts))

    for path, err in results:
        if err:
            failures.append((path, err))

    duration = time.time() - start_time

    print("-" * 60)
    if not failures:
        print(f"✅ PASS: All scripts compiled successfully in {duration:.2f}s")
        return 0
    else:
        print(f"❌ FAIL: {len(failures)} scripts failed compilation")
        for path, err in failures:
            rel_path = os.path.relpath(path, project_path)
            print(f"\n[!] {rel_path}:")
            lines = err.strip().split("\n")
            for line in lines[:5]:
                print(f"    {line}")
            if len(lines) > 5:
                print("    ...")
        return 1
