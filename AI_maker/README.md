# 智能编程导师 - CodeMentor AI

## 项目简介
CodeMentor AI 是一个基于人工智能的个性化编程学习智能体，旨在为编程学习者提供智能化的指导和支持。

## 核心功能
- 🤖 **智能代码分析** - 深度分析代码质量并提供改进建议
- 📚 **个性化学习路径** - 根据用户水平制定专属学习计划
- 💡 **实时编程助手** - 提供代码补全、错误修复等实时帮助
- 🎯 **项目实战指导** - 引导用户完成实际项目开发
- 📊 **学习进度跟踪** - 监控学习进度并提供激励反馈

## 技术栈
- **后端**: Python + FastAPI
- **前端**: React + TypeScript
- **AI模型**: OpenAI GPT-4 + 自定义微调模型
- **数据库**: PostgreSQL + Redis
- **部署**: Docker + Kubernetes

## 项目结构
```
AI_maker/
├── backend/                 # 后端服务
│   ├── app/                # 主应用
│   ├── models/             # 数据模型
│   ├── services/           # 业务逻辑
│   └── api/                # API接口
├── frontend/               # 前端应用
│   ├── src/                # 源代码
│   ├── components/         # React组件
│   └── pages/              # 页面组件
├── ai_engine/              # AI引擎
│   ├── models/             # AI模型
│   ├── processors/         # 代码处理器
│   └── trainers/           # 模型训练器
├── docs/                   # 文档
└── tests/                  # 测试文件
```

## 快速开始
1. 克隆项目
2. 安装依赖
3. 配置环境变量
4. 启动服务

详细安装和使用说明请参考 [安装指南](docs/installation.md) 