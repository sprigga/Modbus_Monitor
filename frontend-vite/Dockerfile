# 建構階段
FROM node:20-alpine AS builder

WORKDIR /app

# 複製 package 檔案
COPY package*.json ./

# 安裝依賴
RUN npm ci

# 複製原始碼
COPY . .

# 建構應用
RUN npm run build

# 生產階段 - 使用 nginx 提供靜態檔案
FROM nginx:alpine

# 複製自訂 nginx 設定 (若有需要)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# 從建構階段複製建構產物
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 啟動 nginx
CMD ["nginx", "-g", "daemon off;"]
