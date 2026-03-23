# VS Code Auto Setup

Script này giúp bạn **tự động cài các công cụ/ngôn ngữ phổ biến** để code trên VS Code.

## File chính

- `dev_setup.sh`: script chạy cài đặt.
- `vscode-dev-manifest.sh`: danh sách packages/extensions có thể tùy chỉnh.

## Cách dùng

```bash
chmod +x dev_setup.sh vscode-dev-manifest.sh
./dev_setup.sh
```

## Hệ điều hành hỗ trợ

- Ubuntu/Debian: dùng `apt`.
- macOS: dùng `brew`.
- Windows: ưu tiên `winget`, fallback `choco`.

## Lưu ý

- Trên Linux/macOS script có thể cần `sudo` để cài package hệ thống.
- Để cài extension VS Code, cần có lệnh `code` trong PATH.
- Bạn có thể chỉnh danh sách package tại `vscode-dev-manifest.sh` theo stack của bạn.
