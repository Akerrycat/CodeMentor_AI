#!/bin/bash

echo "🚀 启动 CodeMentor AI 项目..."

# 检查环境变量
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  警告: 未设置 OPENAI_API_KEY 环境变量"
    echo "请在 .env 文件中设置您的 OpenAI API 密钥"
fi

if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  警告: 未设置 SECRET_KEY 环境变量"
    echo "正在生成随机密钥..."
    export SECRET_KEY=$(openssl rand -hex 32)
fi

# 创建必要的目录
mkdir -p logs
mkdir -p data

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未找到 Docker，请先安装 Docker"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: 未找到 Docker Compose，请先安装 Docker Compose"
    exit 1
fi

# 构建并启动服务
echo "📦 构建 Docker 镜像..."
docker-compose build

echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 服务状态:"
docker-compose ps

echo ""
echo "✅ CodeMentor AI 已启动!"
echo ""
echo "🌐 访问地址:"
echo "   前端应用: http://localhost:3000"
echo "   后端API:  http://localhost:8000"
echo "   API文档:  http://localhost:8000/docs"
echo ""
echo "📝 日志查看:"
echo "   docker-compose logs -f backend"
echo "   docker-compose logs -f frontend"
echo ""
echo "🛑 停止服务:"
echo "   docker-compose down" 