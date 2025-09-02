#!/usr/bin/env bash

# Deustaller: minimal preset-based package installer with logging
# - Detects OS package manager (apt/pacman/dnf)
# - Scans local di-* preset directories and lets user choose
# - Reads packages from preset's pkg file
# - Prints two lines: missing to install, already installed
# - Streams all output to console and full log, errors to separate error log

APP_VERSION="0.0.1"
ERRORLOG=log-deustaller-error.log
FULLOG=log-deustaller-full.log

# Print a simple header with version
logo() {
    clear
    message=$1
    echo "DEUSTALLER v$APP_VERSION"
    echo "OS: ${OS_PRETTY:-Unknown}"
    if [ -n "$message" ]; then
        echo "$message"
    fi
}

# Clear screen and show step title
step() {
    local title="$1"
    clear
    logo "$title"
}

# Format timestamp for logs
ts() {
    date +"%Y-%m-%d %H:%M:%S"
}

# Initialize the full log with a session header
init_logs() {
    {
        echo "==== $(ts) :: start deustaller v$APP_VERSION on ${OS_PRETTY:-Unknown} ===="
    } >> "$FULLOG"
}

# Print informational message to stdout and append to full log
log_info() {
    local message="$1"
    echo "$message" | tee -a "$FULLOG"
}

# Run a command with live output; append stdout to full log and capture stderr to error log
run_cmd() {
    local cmd_str="$*"
    log_info "$ $cmd_str"
    local tmp_err
    tmp_err=$(mktemp)
    {
        bash -c "$cmd_str"
    } > >(tee -a "$FULLOG") 2> >(tee -a "$FULLOG" | tee -a "$tmp_err" >&2)
    local ec=$?
    if [ $ec -ne 0 ]; then
        touch "$ERRORLOG"
        {
            echo "[$(ts)] Command failed: $cmd_str"
            echo "Exit code: $ec"
            echo "Stderr:"
            cat "$tmp_err"
            echo "----"
        } >> "$ERRORLOG"
    fi
    rm -f "$tmp_err"
    return $ec
}

# Package manager related globals
PKG_MGR_NAME=""
INSTALL_CMD=""
CHECK_CMD=""
SUDO=""
OS_PRETTY="Unknown"

# Detect OS pretty name for header/logging (does not decide package manager)
detect_os_info() {
    if [ -r /etc/os-release ]; then
        . /etc/os-release
        OS_PRETTY="${PRETTY_NAME:-${NAME:-Unknown}}"
    else
        OS_PRETTY="$(uname -s) $(uname -r)"
    fi
}

# Detect OS/package manager and prepare install/check commands
detect_os() {
    if [ "$(id -u)" -ne 0 ]; then
        SUDO="sudo"
    else
        SUDO=""
    fi

    local id like
    if [ -r /etc/os-release ]; then
        . /etc/os-release
        id="$ID"
        like="$ID_LIKE"
    fi

    case "$id $like" in
        *debian*|*ubuntu*|*Debian*|*Ubuntu*)
            PKG_MGR_NAME="apt"
            INSTALL_CMD="$SUDO apt-get install -y"
            CHECK_CMD="dpkg -s"
            ;;
        *arch*|*manjaro*|*Artix*|*Arch*)
            PKG_MGR_NAME="pacman"
            INSTALL_CMD="$SUDO pacman -S --noconfirm"
            CHECK_CMD="pacman -Qi"
            ;;
        *fedora*|*rhel*|*centos*|*rocky*|*alma*)
            PKG_MGR_NAME="dnf"
            INSTALL_CMD="$SUDO dnf install -y"
            CHECK_CMD="rpm -q"
            ;;
        *)
            ;;
    esac

    if [ -z "$PKG_MGR_NAME" ]; then
        log_info "Failed to detect a supported package manager."
        exit 1
    fi

    log_info "Detected package manager: $PKG_MGR_NAME"
    if [ "$PKG_MGR_NAME" = "apt" ]; then
        run_cmd $SUDO apt-get update
    elif [ "$PKG_MGR_NAME" = "pacman" ]; then
        run_cmd $SUDO pacman -Sy --noconfirm
    fi
}

# Return 0 if package is installed, non-zero otherwise
is_installed() {
    local pkg="$1"
    case "$PKG_MGR_NAME" in
        apt)
            $CHECK_CMD "$pkg" >/dev/null 2>&1 ;;
        pacman)
            $CHECK_CMD "$pkg" >/dev/null 2>&1 ;;
        dnf)
            $CHECK_CMD "$pkg" >/dev/null 2>&1 ;;
        *)
            return 1 ;;
    esac
}

# Install a list of packages using the detected package manager
install_packages() {
    local -a pkgs=("$@")
    [ ${#pkgs[@]} -eq 0 ] && return 0
    case "$PKG_MGR_NAME" in
        apt)
            run_cmd $INSTALL_CMD "${pkgs[*]}" ;;
        pacman)
            run_cmd $INSTALL_CMD "${pkgs[*]}" ;;
        dnf)
            run_cmd $INSTALL_CMD "${pkgs[*]}" ;;
        *)
            return 1 ;;
    esac
}

# Read package names from a file, ignoring comments and blank lines
read_packages_from_file() {
    local file="$1"
    local -n _out_arr="$2"
    _out_arr=()
    while IFS= read -r line || [ -n "$line" ]; do
        line="${line%%#*}"
        line="$(echo "$line" | xargs)"
        [ -z "$line" ] && continue
        for token in $line; do
            _out_arr+=("$token")
        done
    done < "$file"
}

# Execute additional preset scripts: any files matching script*.sh in the preset directory
run_preset_scripts() {
    # PRESET_DIR must be set by select_preset_dir
    [ -z "$PRESET_DIR" ] && return 0

    shopt -s nullglob
    local scripts=("$PRESET_DIR"/script*.sh)
    shopt -u nullglob

    if [ ${#scripts[@]} -eq 0 ]; then
        # Nothing to run
        return 0
    fi

    step "Running preset scripts"
    for sc in "${scripts[@]}"; do
        local bn
        bn="${sc##*/}"

        # Per-script logs inside the preset directory
        local s_full s_err
        s_full="$PRESET_DIR/${bn%.sh}-full.log"
        s_err="$PRESET_DIR/${bn%.sh}-error.log"

        log_info "Executing $bn"

        chmod +x "$sc" 2>/dev/null

        # Run and pipe stdout/stderr to dedicated logs, while also mirroring to global FULLOG
        {
            echo "==== $(ts) :: start $bn ===="
            bash -c "$sc"
            echo "==== $(ts) :: end $bn ===="
        } >> "$s_full" 2>> "$s_err"

        # Also append short status to the main logs
        if [ ${PIPESTATUS[1]:-0} -eq 0 ]; then
            log_info "$bn finished successfully"
        else
            log_info "$bn finished with errors (see $(realpath --relative-to="$PWD" "$s_err" 2>/dev/null || echo "$s_err"))"
        fi
    done
}

# Scan for di-* directories, display a menu without the di- prefix, and set PRESET_DIR/NAME
select_preset_dir() {
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local -a dirs=()
    local -a names=()
    shopt -s nullglob
    for d in "$script_dir"/di-*; do
        [ -d "$d" ] || continue
        dirs+=("$d")
        local bn
        bn="${d##*/}"
        names+=("${bn#di-}")
    done
    shopt -u nullglob

    if [ ${#dirs[@]} -eq 0 ]; then
        log_info "No presets found. Press 0 to exit."
        echo -n "Your choice: "
        read -r choice
        [ "$choice" = "0" ] && exit 0 || exit 0
    fi

    log_info "Available presets:"
    local i=1
    while [ $i -le ${#names[@]} ]; do
        echo "$i. ${names[$((i-1))]}"
        i=$((i+1))
    done | tee -a "$FULLOG"
    echo "0. exit" | tee -a "$FULLOG"

    echo -n "Your choice: "
    read -r choice
    if [ "$choice" = "0" ]; then
        exit 0
    fi
    if ! [[ "$choice" =~ ^[0-9]+$ ]]; then
        log_info "Invalid input"
        exit 1
    fi
    local idx=$((choice-1))
    if [ $idx -lt 0 ] || [ $idx -ge ${#dirs[@]} ]; then
        log_info "No such menu item"
        exit 1
    fi
    PRESET_DIR="${dirs[$idx]}"
    PRESET_NAME="${names[$idx]}"
}

# Main entry: detect OS, select preset, read packages, show summary, install missing
main() {
    detect_os_info
    init_logs

    step "Detecting system"
    detect_os

    step "Select preset"
    select_preset_dir

    local pkg_file="$PRESET_DIR/pkg"
    if [ ! -f "$pkg_file" ]; then
        log_info "No pkg file found in preset '$PRESET_NAME'"
        exit 1
    fi

    local -a all_pkgs
    read_packages_from_file "$pkg_file" all_pkgs
    if [ ${#all_pkgs[@]} -eq 0 ]; then
        log_info "pkg file is empty."
        exit 0
    fi

    step "Analyzing packages"
    local -a to_install=()
    local -a installed=()
    for p in "${all_pkgs[@]}"; do
        if is_installed "$p"; then
            installed+=("$p")
        else
            to_install+=("$p")
        fi
    done

    local ni=${#to_install[@]}
    local mi=${#installed[@]}
    if [ $ni -gt 0 ]; then
        log_info "To install ($ni): ${to_install[*]}"
    else
        log_info "To install (0): -"
    fi
    if [ $mi -gt 0 ]; then
        log_info "Already installed ($mi): ${installed[*]}"
    else
        log_info "Already installed (0): -"
    fi

    if [ $ni -gt 0 ]; then
        step "Installing packages"
        log_info "Starting installation..."
        install_packages "${to_install[@]}"
    fi

    # Execute preset scripts after package installation
    run_preset_scripts

    step "Done"
}

main "$@"