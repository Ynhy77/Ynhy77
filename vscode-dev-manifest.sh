#!/usr/bin/env bash

# Danh sách package tối thiểu, có thể chỉnh theo nhu cầu dự án.
APT_PACKAGES=(
  git
  curl
  build-essential
  python3
  python3-pip
  nodejs
  npm
  openjdk-17-jdk
  golang
  rustc
  cargo
)

BREW_PACKAGES=(
  git
  curl
  python
  node
  openjdk@17
  go
  rust
)

# IDs cho winget (tham khảo kho winget)
WINGET_PACKAGES=(
  Git.Git
  Python.Python.3.12
  OpenJS.NodeJS.LTS
  Microsoft.OpenJDK.17
  GoLang.Go
  Rustlang.Rustup
)

CHOCO_PACKAGES=(
  git
  python
  nodejs-lts
  openjdk17
  golang
  rust
)

VSCODE_EXTENSIONS=(
  ms-python.python
  ms-python.vscode-pylance
  dbaeumer.vscode-eslint
  esbenp.prettier-vscode
  golang.go
  rust-lang.rust-analyzer
  redhat.java
  ms-vscode.cpptools
  eamodio.gitlens
)
