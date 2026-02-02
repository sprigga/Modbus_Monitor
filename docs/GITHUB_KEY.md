# GitHub SSH 金鑰設置

## 問題描述

執行 `git pull origin main` 時出現 SSH 權限錯誤：

```bash
git@github.com: Permission denied (publickey).
fatal: 無法讀取遠端版本庫。
```

## 診斷步驟

### 1. 檢查遠端倉庫 URL

```bash
git remote -v
```

如果顯示 `git@github.com:...` 表示使用 SSH 方式。

### 2. 檢查 SSH 目錄

```bash
ls -la ~/.ssh/
```

確認是否有 SSH 金鑰檔案（如 `id_ed25519`、`id_rsa` 等）。

### 3. 檢查 SSH 配置

```bash
cat ~/.ssh/config
```

查看 SSH 配置是否正確指向金鑰檔案。

### 4. 測試 SSH 連線

```bash
ssh -T git@github.com
```

成功的話會顯示：
```
Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.
```

## 解決方案

### 方案一：使用 GitHub CLI 設置 SSH 金鑰

#### 1. 檢查 gh 登入狀態

```bash
gh auth status
```

#### 2. 刷新 gh 權限（如需要）

```bash
gh auth refresh -h github.com -s admin:public_key,admin:ssh_signing_key
```

按照提示在瀏覽器中完成驗證。

#### 3. 生成新的 SSH 金鑰

```bash
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519_new -N ""
```

#### 4. 添加金鑰到 GitHub

```bash
gh ssh-key add ~/.ssh/id_ed25519_new.pub --title "my_ssh_key"
```

#### 5. 更新 SSH 配置

編輯 `~/.ssh/config`：

```bash
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_new
    IdentitiesOnly yes
```

#### 6. 測試連線

```bash
ssh -T git@github.com
```

### 方案二：改用 HTTPS 方式

如果 SSH 設置有困難，可以改用 HTTPS：

```bash
git remote set-url origin https://github.com/username/repository.git
```

## 驗證設置成功

執行以下指令驗證：

```bash
# 測試 SSH 連線
ssh -T git@github.com

# 拉取最新程式碼
git pull origin main
```

## 常見問題

### 私鑰與公鑰不匹配

如果出現 `Permission denied`，可能的原因：
- 私鑰需要密碼保護
- 本地公鑰與私鑰不匹配
- GitHub 上的金鑰已過期

解決方法：重新生成金鑰對並添加到 GitHub。

### 權限不足

確保 gh 有足夠的權限：
```bash
gh auth refresh -h github.com -s admin:public_key
```

## 參考資料

- [GitHub SSH 金鑰官方文檔](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh)
- [GitHub CLI 認證](https://docs.github.com/zh/github-cli/github-cli/about-github-cli)
