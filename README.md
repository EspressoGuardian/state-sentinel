# state-sentinel 🔧

**Unified health & determinism auditor for Godot 4.x projects.**

`state-sentinel` is a CLI tool designed to enforce rigour in Godot projects. It combines parallel static analysis (compilation checks) with headless replay verification to ensure your game's state remains deterministic and error-free.

## Features

- **Static Audit**: Runs `godot --check-only` on all `.gd` files in parallel. Faster than the editor.
- **Replay Audit**: Verifies `.amber_replay.jsonl` files headlessly to confirm determinism.
- **CI-Ready**: Standard exit codes for pipeline integration.

## Installation

(Coming soon via pip)

For now, clone and run:

```bash
git clone https://github.com/EspressoGuardian/state-sentinel.git
cd state-sentinel
chmod +x bin/state-sentinel
```

## Usage

**Static Compilation Check:**

```bash
./bin/state-sentinel static --path /path/to/project --workers 8
```

**Replay Verification:**

```bash
./bin/state-sentinel replay ./debug/crash_log.jsonl --fastforward
```

## Safety & Support

This is a small tool I built for my own workflow and I’m sharing it in case it helps others.

- **Tested on**: Linux (TUXEDO OS)
- **Godot Version**: 4.x (Tested on 4.6)
- **Other platforms**: may work, but not regularly tested

Please review scripts before running, and try them on non-critical data first.

## License

MIT
