# Modbus Monitor Frontend - Vue 3 + Vite

現代化的 Vue 3 前端應用程式,使用 Vite 建置工具和 Single File Components (SFC)。

## 技術棧

- **Vue 3** - 使用 Composition API
- **Vite** - 快速的開發伺服器和建置工具
- **Axios** - HTTP 客戶端
- **Font Awesome** - 圖示庫

## 專案結構

```
frontend-vite/
├── src/
│   ├── components/          # Vue SFC 元件
│   │   ├── AlertContainer.vue
│   │   ├── Configuration.vue
│   │   ├── DataDisplay.vue
│   │   ├── ManualRead.vue
│   │   └── WriteRegister.vue
│   ├── composables/         # Vue 組合式函數
│   │   └── useAlerts.js
│   ├── services/            # API 服務層
│   │   └── api.js
│   ├── assets/              # 靜態資源
│   │   ├── styles.css       # 基礎樣式
│   │   └── page-styles.css  # 頁面專屬樣式
│   ├── App.vue              # 主應用元件
│   └── main.js              # 應用程式入口
├── dist/                    # 建置輸出目錄
├── index.html               # HTML 模板
├── vite.config.js           # Vite 配置
└── package.json             # 專案依賴
```

## 開發

### 安裝依賴

```bash
cd frontend-vite
npm install
```

### 開發伺服器

啟動 Vite 開發伺服器 (熱重載):

```bash
npm run dev
```

開發伺服器會在 `http://localhost:5173` 啟動,並自動將 API 請求代理到 `http://localhost:8000`。

### 生產建置

建置生產版本:

```bash
npm run build
```

建置輸出會在 `dist/` 目錄中。

或使用專案根目錄的建置腳本:

```bash
./build-frontend.sh
```

## 元件架構

### 主要元件

1. **App.vue** - 主應用元件,管理全域狀態和業務邏輯
2. **Configuration.vue** - Modbus 配置表單
3. **ManualRead.vue** - 手動讀取暫存器
4. **WriteRegister.vue** - 寫入暫存器
5. **DataDisplay.vue** - 顯示 Modbus 資料表格
6. **AlertContainer.vue** - 通知訊息系統

### 組合式函數

- **useAlerts.js** - 提供 alert 管理功能 (showAlert, removeAlert)

### 服務層

- **api.js** - 統一的 API 請求服務,自動偵測環境並設定 API base URL

## 與舊版前端 (frontend/) 的差異

| 特性 | 舊版 (CDN) | 新版 (Vite) |
|------|-----------|------------|
| 建置工具 | 無 | Vite |
| 元件格式 | 單一 HTML + JS | Single File Components (.vue) |
| 開發體驗 | 無熱重載 | 快速熱重載 |
| 生產優化 | 無優化 | Tree-shaking, code splitting |
| TypeScript 支援 | 無 | 完整支援 |
| 程式碼組織 | 單一檔案 | 模組化元件 |

## 部署

建置完成後,`dist/` 目錄包含所有靜態檔案。Docker Compose 會自動掛載這個目錄到 nginx 容器。

```bash
# 建置前端
./build-frontend.sh

# 啟動 Docker
docker-compose up -d
```

前端會在 `http://localhost:8081` 提供服務。

## 環境變數

API base URL 會自動根據環境偵測:

- **開發模式** (localhost:5173): `http://localhost:8000/api`
- **Docker/生產**: `/api` (透過 nginx proxy)
- **Nginx proxy** (port 8081): `${protocol}//${hostname}:8081/api`

## 樣式系統

應用程式使用現代化的漸層玻璃擬態設計系統:

- CSS 變數定義在 `assets/styles.css`
- 頁面專屬樣式在 `assets/page-styles.css`
- 響應式設計,支援移動裝置
- 動畫效果和漸層背景

## 故障排除

### 建置失敗

```bash
# 清除快取並重新安裝
rm -rf node_modules package-lock.json
npm install
npm run build
```

### API 連線問題

確保後端在 `localhost:8000` 運行,或在 Vite 配置中修改 proxy target。

### Docker 無法顯示前端

確保已建置前端:

```bash
./build-frontend.sh
docker-compose restart frontend
```
