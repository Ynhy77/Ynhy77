#!/usr/bin/env bash
set -euo pipefail

# Tự động cài tool/ngôn ngữ phổ biến cho môi trường code với VS Code.
# Hỗ trợ: macOS (brew), Ubuntu/Debian (apt), Windows (winget/choco nếu chạy trong Git Bash/WSL).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST_PATH="${SCRIPT_DIR}/vscode-dev-manifest.sh"

if [[ ! -f "$MANIFEST_PATH" ]]; then
  echo "Không tìm thấy manifest: $MANIFEST_PATH"
  exit 1
fi

# shellcheck source=/dev/null
source "$MANIFEST_PATH"

log() { printf "\n[setup] %s\n" "$1"; }
warn() { printf "\n[warn] %s\n" "$1"; }

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

install_with_apt() {
  local pkg="$1"
  if dpkg -s "$pkg" >/dev/null 2>&1; then
    echo "  - $pkg đã có"
  else
    sudo apt-get install -y "$pkg"
  fi
}

install_with_brew() {
  local pkg="$1"
  if brew list "$pkg" >/dev/null 2>&1; then
    echo "  - $pkg đã có"
  else
    brew install "$pkg"
  fi
}

install_with_winget() {
  local id="$1"
  winget install --id "$id" -e --accept-package-agreements --accept-source-agreements || true
}

install_with_choco() {
  local pkg="$1"
  choco install -y "$pkg"
}

install_system_packages() {
  log "Cài system packages"

  if has_cmd apt-get; then
    sudo apt-get update -y
    for pkg in "${APT_PACKAGES[@]}"; do
      install_with_apt "$pkg"
    done
    return
  fi

  if has_cmd brew; then
    for pkg in "${BREW_PACKAGES[@]}"; do
      install_with_brew "$pkg"
    done
    return
  fi

  if has_cmd winget; then
    for id in "${WINGET_PACKAGES[@]}"; do
      install_with_winget "$id"
    done
    return
  fi

  if has_cmd choco; then
    for pkg in "${CHOCO_PACKAGES[@]}"; do
      install_with_choco "$pkg"
    done
    return
  fi

  warn "Không tìm thấy apt/brew/winget/choco. Bỏ qua cài system packages."
}

install_vscode_extensions() {
  if ! has_cmd code; then
    warn "Không tìm thấy lệnh 'code'. Hãy bật 'Shell Command: Install \"code\" command in PATH' trong VS Code."
    return
  fi

  log "Cài VS Code extensions"
  mapfile -t installed < <(code --list-extensions)

  for ext in "${VSCODE_EXTENSIONS[@]}"; do
    if printf '%s\n' "${installed[@]}" | grep -qx "$ext"; then
      echo "  - $ext đã có"
    else
      code --install-extension "$ext"
    fi
  done
}

show_post_steps() {
  log "Hoàn tất"
  cat <<EOF
Gợi ý tiếp theo:
1) Mở VS Code tại thư mục project.
2) Chọn Python interpreter / Node version theo dự án.
3) Chạy formatters & linters của dự án.
EOF
}

main() {
  install_system_packages
  install_vscode_extensions
  show_post_steps
}

main "$@"
