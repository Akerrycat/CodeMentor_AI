from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import sys
import os

# 添加AI引擎路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../ai_engine'))
from code_analyzer import CodeAnalyzer
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.learning_session import LearningSession, LearningSessionCreate, LearningSessionResponse
from app.core.auth import get_current_user

router = APIRouter()

# 初始化代码分析器
code_analyzer = CodeAnalyzer(settings.OPENAI_API_KEY, settings.OPENAI_MODEL)

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_code(
    code: str,
    language: str,
    topic: str = "general",
    session_type: str = "code_review",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    分析用户提交的代码
    """
    try:
        # 使用AI分析代码
        analysis_result = code_analyzer.analyze_code(
            code=code,
            language=language,
            user_level=current_user.skill_level
        )
        
        # 生成用户友好的反馈
        feedback = code_analyzer.generate_feedback(analysis_result, current_user.skill_level)
        
        # 创建学习会话记录
        session_data = LearningSessionCreate(
            session_type=session_type,
            language=language,
            topic=topic,
            code_content=code
        )
        
        # 保存到数据库
        db_session = LearningSession(
            user_id=current_user.id,
            session_type=session_data.session_type,
            language=session_data.language,
            topic=session_data.topic,
            code_content=session_data.code_content,
            ai_feedback=feedback,
            score=analysis_result.get("overall_score", 0.0)
        )
        
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        
        return {
            "session_id": db_session.id,
            "analysis": analysis_result,
            "feedback": feedback,
            "score": analysis_result.get("overall_score", 0.0),
            "suggestions": analysis_result.get("ai_analysis", {}).get("suggestions", []),
            "issues_count": len(analysis_result.get("syntax_issues", []))
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"代码分析失败: {str(e)}"
        )

@router.get("/sessions", response_model=list[LearningSessionResponse])
async def get_user_sessions(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户的学习会话历史
    """
    sessions = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return sessions

@router.get("/sessions/{session_id}", response_model=LearningSessionResponse)
async def get_session_detail(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取特定会话的详细信息
    """
    session = db.query(LearningSession).filter(
        LearningSession.id == session_id,
        LearningSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    return session

@router.get("/stats")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户的学习统计信息
    """
    # 获取总会话数
    total_sessions = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id
    ).count()
    
    # 获取平均分数
    avg_score = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id,
        LearningSession.score > 0
    ).with_entities(
        db.func.avg(LearningSession.score)
    ).scalar() or 0.0
    
    # 获取最佳分数
    best_score = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id
    ).with_entities(
        db.func.max(LearningSession.score)
    ).scalar() or 0.0
    
    # 获取学习时长
    total_duration = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id
    ).with_entities(
        db.func.sum(LearningSession.duration_minutes)
    ).scalar() or 0
    
    return {
        "total_sessions": total_sessions,
        "average_score": round(avg_score, 2),
        "best_score": round(best_score, 2),
        "total_duration_minutes": total_duration,
        "total_duration_hours": round(total_duration / 60, 1)
    } 