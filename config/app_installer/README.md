## Deustaller

A small, preset-driven package installer with clean logging and predictable behavior.

- Auto-detects package manager: apt, pacman, or dnf
- Scans local presets in directories named `di-*`
- Reads packages from each preset’s `pkg` file
- Streams live output, writes a full audit log, and records errors separately
- Clears the screen between major steps for operator focus

### Header and Versioning
- Application name and version are controlled by `APP_NAME` and `APP_VERSION` in `deustaller.sh`.
- At runtime the header prints as two lines:
  - `<APP_NAME> v<APP_VERSION>`
  - `OS: <PRETTY_NAME>` (from `/etc/os-release` when available)

### Requirements
- Linux: Debian/Ubuntu (apt), Arch/Manjaro (pacman), Fedora/RHEL family (dnf)
- Bash 4+
- Privileges: may use `sudo` automatically when not root

### Layout
- `deustaller.sh` — main executable
- `di-<name>/pkg` — preset directories with a `pkg` file
- `log-deustaller-full.log` — append-only full session log
- `log-deustaller-error.log` — error log (created only on failures)
- `script*.sh` — optional post-install scripts inside a preset, executed after package installation
  - Each script writes its own logs next to the script:
    - `<script>-full.log` — full output
    - `<script>-error.log` — errors only

Example:
```
./deustaller.sh
./di-work/pkg
./di-main/pkg
```

### Preset `pkg` Format
- Package names separated by spaces and/or newlines
- `#` begins a comment to end of line

Example:
```
# Core
curl git

# Editor
vim
```

### Usage
```bash
chmod +x ./deustaller.sh
./deustaller.sh
```
- Choose a preset from the menu (numbers correspond to names without the `di-` prefix).
- Enter `0` to exit at any time.
- Before installation, two summary lines are shown:
  - `To install (N): ...`
  - `Already installed (M): ...`

#### Post-install scripts (script*.sh)
- Place one or more `script*.sh` files inside the selected preset (e.g., `di-work`).
- They run automatically after package installation, in alphabetical order.
- Example: `di-work/script-snap-install.sh` installs `snapd` from AUR non-interactively.
- It is recommended to make commands non-interactive inside such scripts (e.g., add `--noconfirm`).

### Logging
- Console output is mirrored to `log-deustaller-full.log`.
- On any non-zero exit, `log-deustaller-error.log` receives a timestamp, command, exit code, and stderr snapshot.
- Log rotation is out of scope; manage externally if needed.
- Each `script*.sh` also writes its own logs next to the script: `<script>-full.log` and `<script>-error.log`.

### Exit Codes
- `0` success (including when nothing needed to be installed)
- `1` configuration/input error (unsupported package manager, invalid menu, missing `pkg`)
- Underlying tool errors are surfaced live and recorded in logs

### Configuration and Extensibility
- Change `APP_NAME`, `APP_VERSION`, and log filenames at the top of `deustaller.sh`.
- Extend `detect_os()` to support other package managers if required.

### Notes and Limitations
- No rollback of partial installs.
- Assumes package names are valid for the detected package manager.

