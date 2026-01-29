
import os
import shutil
import subprocess
from pathlib import Path

def _find_godot(bin_override: str | None = None) -> str | None:
    if bin_override:
        return bin_override
    env_bin = os.environ.get("GODOT_BIN")
    if env_bin:
        return env_bin
    for name in ("godot4", "godot"):
        path = shutil.which(name)
        if path:
            return path
    return None

def _find_repo_root(start: Path) -> Path:
    # Look for game/project.godot
    current = start.resolve()
    for parent in [current] + list(current.parents):
        if (parent / "game" / "project.godot").exists():
            return parent
        if (parent / "project.godot").exists():
            return parent
    return start # Fallback

def run_replay_audit(replay_file, fastforward=False, timeout=120):
    godot_bin = _find_godot()
    if not godot_bin:
        print("Error: Godot binary not found. Set GODOT_BIN environment variable.")
        return 1

    replay_path = Path(replay_file).resolve()
    if not replay_path.exists():
        print(f"Error: Replay file not found: {replay_path}")
        return 1

    # Heuristic: Assume running from repo root
    repo_root = Path.cwd()
    project_path = repo_root / "game"
    
    if not (project_path / "project.godot").exists():
         if (repo_root / "project.godot").exists():
             project_path = repo_root
         else:
             print("Error: Could not locate project.godot")
             return 1

    print("=" * 60)
    print(f" REPLAY AUDIT | {replay_path.name}")
    print("=" * 60)

    # Note: Requires ReplayRunner.gd to be present in the target project
    # We assume standard Amber State structure: scripts/tools/ReplayRunner.gd
    script_path = "scripts/tools/ReplayRunner.gd"
    
    cmd = [
        godot_bin,
        "--headless",
        "--path",
        str(project_path),
        "--script",
        script_path,
        "--",
        f"--file={replay_path}",
        f"--timeout={timeout}",
    ]
    if fastforward:
        cmd.append("--fastforward")

    try:
        result = subprocess.run(cmd, cwd=str(repo_root))
        return result.returncode
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1
