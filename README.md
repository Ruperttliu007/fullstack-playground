# fullstack-playground

一个最小全栈示例：**React + FastAPI + Postgres**。

## 目录结构
- apps/web —— React + TS (Vite)
- apps/api —— FastAPI
- infra/docker —— Docker Compose（Postgres、pgAdmin）

## 快速开始
### 1) 启动数据库
cd infra/docker
docker compose up -d

### 2) 启动后端（FastAPI）
cd ../../apps/api
source ~/.venvs/fs/bin/activate
export PYTHONPATH=$PWD
uvicorn src.main:app --reload --port 8000

### 3) 启动前端（Vite）
cd ../../apps/web
pnpm install
pnpm dev
