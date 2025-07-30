#!/usr/bin/env python3
"""
CodeMentor AI 简单演示
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn

app = FastAPI(
    title="CodeMentor AI Demo",
    description="智能编程导师演示版本",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟数据
demo_sessions = []

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str
    topic: str = "general"

class CodeAnalysisResponse(BaseModel):
    session_id: int
    analysis: Dict[str, Any]
    feedback: str
    score: float
    suggestions: List[str]
    issues_count: int

def analyze_code_demo(code: str, language: str) -> Dict:
    issues = []
    suggestions = []
    score = 85.0

    if language.lower() == "python":
        if "print(" in code:
            suggestions.append("✅ 使用了print函数，很好！")
        if "def " in code:
            suggestions.append("✅ 定义了函数，结构清晰！")
        if "for " in code or "while " in code:
            suggestions.append("✅ 使用了循环结构！")
        if "if " in code:
            suggestions.append("✅ 使用了条件判断！")
    if "eval(" in code:
        issues.append("⚠️ 检测到eval函数，可能存在安全风险")
        score -= 10
    if len(code.split('\n')) < 3:
        suggestions.append("💡 建议添加更多注释和文档")

    return {
        "syntax_issues": issues,
        "ai_analysis": {
            "analysis": "这是一个演示版本的代码分析。在实际版本中，这里会包含AI驱动的深度分析。",
            "suggestions": suggestions
        },
        "performance_issues": [],
        "security_issues": [],
        "overall_score": max(0, score)
    }

@app.get("/")
async def root():
    return {
        "message": "欢迎使用 CodeMentor AI - 演示版本",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "CodeMentor AI Demo"}

@app.post("/api/v1/code/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    try:
        analysis_result = analyze_code_demo(
            code=request.code,
            language=request.language
        )
        feedback = "🎉 代码分析完成！这是一个演示版本的分析结果。"
        if analysis_result["overall_score"] >= 80:
            feedback = "🎉 优秀！您的代码质量很高！"
        elif analysis_result["overall_score"] >= 60:
            feedback = "👍 不错！代码基本正确，但还有改进空间。"
        else:
            feedback = "📚 需要改进。建议查看分析结果中的建议。"
        session_id = len(demo_sessions) + 1
        demo_sessions.append({
            "id": session_id,
            "code": request.code,
            "language": request.language,
            "topic": request.topic,
            "score": analysis_result["overall_score"],
            "feedback": feedback
        })
        return CodeAnalysisResponse(
            session_id=session_id,
            analysis=analysis_result,
            feedback=feedback,
            score=analysis_result["overall_score"],
            suggestions=analysis_result["ai_analysis"]["suggestions"],
            issues_count=len(analysis_result["syntax_issues"])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"代码分析失败: {str(e)}")

@app.get("/api/v1/code/sessions")
async def get_user_sessions():
    return demo_sessions

@app.get("/api/v1/code/stats")
async def get_user_stats():
    if not demo_sessions:
        return {
            "total_sessions": 0,
            "average_score": 0.0,
            "total_learning_time": 0,
            "user_level": "beginner"
        }
    total_sessions = len(demo_sessions)
    avg_score = sum(session["score"] for session in demo_sessions) / total_sessions
    return {
        "total_sessions": total_sessions,
        "average_score": round(avg_score, 2),
        "total_learning_time": total_sessions * 5,
        "user_level": "beginner"
    }

@app.get("/api/v1/learning/topics")
async def get_available_topics():
    topics = [
        {
            "id": "python_basics",
            "title": "Python基础语法",
            "description": "学习Python的基本语法、变量、数据类型和控制结构",
            "difficulty": "beginner",
            "estimated_hours": 10,
            "prerequisites": [],
            "tags": ["python", "基础", "语法"]
        },
        {
            "id": "functions",
            "title": "函数和模块",
            "description": "学习如何定义和使用函数，以及模块化编程",
            "difficulty": "beginner",
            "estimated_hours": 8,
            "prerequisites": ["python_basics"],
            "tags": ["python", "函数", "模块"]
        },
        {
            "id": "data_structures",
            "title": "数据结构基础",
            "description": "学习列表、字典、集合等基本数据结构",
            "difficulty": "beginner",
            "estimated_hours": 12,
            "prerequisites": ["python_basics"],
            "tags": ["python", "数据结构"]
        }
    ]
    return {"topics": topics}

if __name__ == "__main__":
    print("🚀 启动 CodeMentor AI 演示服务...")
    print("🌐 访问地址:")
    print("   - API服务: http://localhost:8000")
    print("   - API文档: http://localhost:8000/docs")
    print("   - 健康检查: http://localhost:8000/health")
    print("   - 根路径: http://localhost:8000/")
    print("\n📝 演示功能:")
    print("   - 代码分析: POST /api/v1/code/analyze")
    print("   - 会话历史: GET /api/v1/code/sessions")
    print("   - 统计信息: GET /api/v1/code/stats")
    print("   - 学习主题: GET /api/v1/learning/topics")
    uvicorn.run(
        "simple_demo:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 