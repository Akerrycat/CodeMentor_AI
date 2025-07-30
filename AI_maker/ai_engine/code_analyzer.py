import openai
import ast
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class AnalysisType(Enum):
    SYNTAX = "syntax"
    LOGIC = "logic"
    STYLE = "style"
    PERFORMANCE = "performance"
    SECURITY = "security"

@dataclass
class CodeIssue:
    line_number: int
    issue_type: AnalysisType
    description: str
    suggestion: str
    severity: str  # low, medium, high
    confidence: float

class CodeAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def analyze_code(self, code: str, language: str, user_level: str) -> Dict:
        """
        综合分析代码，返回详细的分析结果
        """
        # 基础语法检查
        syntax_issues = self._check_syntax(code, language)
        
        # AI深度分析
        ai_analysis = self._ai_analysis(code, language, user_level)
        
        # 性能分析
        performance_issues = self._analyze_performance(code, language)
        
        # 安全分析
        security_issues = self._analyze_security(code, language)
        
        return {
            "syntax_issues": syntax_issues,
            "ai_analysis": ai_analysis,
            "performance_issues": performance_issues,
            "security_issues": security_issues,
            "overall_score": self._calculate_score(syntax_issues, ai_analysis, performance_issues, security_issues)
        }
    
    def _check_syntax(self, code: str, language: str) -> List[CodeIssue]:
        """基础语法检查"""
        issues = []
        
        if language.lower() == "python":
            try:
                ast.parse(code)
            except SyntaxError as e:
                issues.append(CodeIssue(
                    line_number=e.lineno or 0,
                    issue_type=AnalysisType.SYNTAX,
                    description=f"语法错误: {e.msg}",
                    suggestion="请检查语法错误并修正",
                    severity="high",
                    confidence=1.0
                ))
        
        return issues
    
    def _ai_analysis(self, code: str, language: str, user_level: str) -> Dict:
        """使用AI进行深度代码分析"""
        prompt = f"""
        请分析以下{language}代码，用户水平为{user_level}。
        
        请从以下方面进行分析：
        1. 代码逻辑是否正确
        2. 代码风格是否良好
        3. 是否有改进空间
        4. 针对{user_level}水平的建议
        
        代码：
        {code}
        
        请以JSON格式返回分析结果，包含：
        - logic_issues: 逻辑问题列表
        - style_issues: 风格问题列表
        - suggestions: 改进建议
        - score: 总体评分(0-100)
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # 解析AI响应
            ai_response = response.choices[0].message.content
            # 这里需要解析JSON响应，简化处理
            return {
                "analysis": ai_response,
                "score": 85  # 示例分数
            }
        except Exception as e:
            return {
                "analysis": f"AI分析出错: {str(e)}",
                "score": 0
            }
    
    def _analyze_performance(self, code: str, language: str) -> List[CodeIssue]:
        """性能分析"""
        issues = []
        
        # 简单的性能检查规则
        if language.lower() == "python":
            # 检查是否有无限循环
            if "while True:" in code and "break" not in code:
                issues.append(CodeIssue(
                    line_number=0,
                    issue_type=AnalysisType.PERFORMANCE,
                    description="检测到可能的无限循环",
                    suggestion="请确保循环有正确的退出条件",
                    severity="high",
                    confidence=0.8
                ))
            
            # 检查列表推导式使用
            if "for" in code and "[" in code and "]" in code:
                # 这里可以添加更复杂的检查
                pass
        
        return issues
    
    def _analyze_security(self, code: str, language: str) -> List[CodeIssue]:
        """安全分析"""
        issues = []
        
        # 检查SQL注入风险
        if "sql" in code.lower() and "input(" in code.lower():
            issues.append(CodeIssue(
                line_number=0,
                issue_type=AnalysisType.SECURITY,
                description="可能存在SQL注入风险",
                suggestion="请使用参数化查询",
                severity="high",
                confidence=0.7
            ))
        
        # 检查eval使用
        if "eval(" in code:
            issues.append(CodeIssue(
                line_number=0,
                issue_type=AnalysisType.SECURITY,
                description="使用eval()函数存在安全风险",
                suggestion="请避免使用eval()，考虑使用ast.literal_eval()",
                severity="high",
                confidence=0.9
            ))
        
        return issues
    
    def _calculate_score(self, syntax_issues: List[CodeIssue], 
                        ai_analysis: Dict, 
                        performance_issues: List[CodeIssue],
                        security_issues: List[CodeIssue]) -> float:
        """计算总体评分"""
        base_score = 100
        
        # 语法错误扣分
        syntax_penalty = len([i for i in syntax_issues if i.severity == "high"]) * 20
        syntax_penalty += len([i for i in syntax_issues if i.severity == "medium"]) * 10
        syntax_penalty += len([i for i in syntax_issues if i.severity == "low"]) * 5
        
        # 性能问题扣分
        perf_penalty = len([i for i in performance_issues if i.severity == "high"]) * 15
        perf_penalty += len([i for i in performance_issues if i.severity == "medium"]) * 8
        perf_penalty += len([i for i in performance_issues if i.severity == "low"]) * 3
        
        # 安全问题扣分
        sec_penalty = len([i for i in security_issues if i.severity == "high"]) * 25
        sec_penalty += len([i for i in security_issues if i.severity == "medium"]) * 15
        sec_penalty += len([i for i in security_issues if i.severity == "low"]) * 8
        
        final_score = max(0, base_score - syntax_penalty - perf_penalty - sec_penalty)
        
        # 结合AI分析分数
        if "score" in ai_analysis:
            final_score = (final_score + ai_analysis["score"]) / 2
        
        return round(final_score, 1)
    
    def generate_feedback(self, analysis_result: Dict, user_level: str) -> str:
        """生成用户友好的反馈"""
        score = analysis_result.get("overall_score", 0)
        
        if score >= 90:
            feedback = "🎉 优秀！你的代码质量很高，继续保持！"
        elif score >= 80:
            feedback = "👍 很好！代码质量不错，有一些小问题可以改进。"
        elif score >= 70:
            feedback = "📝 不错！代码基本正确，但还有改进空间。"
        elif score >= 60:
            feedback = "⚠️ 需要改进。代码有一些问题，建议仔细检查。"
        else:
            feedback = "🔧 需要重点关注。代码存在较多问题，建议重新审视。"
        
        # 添加具体建议
        issues_count = len(analysis_result.get("syntax_issues", []))
        if issues_count > 0:
            feedback += f"\n发现 {issues_count} 个问题需要解决。"
        
        return feedback 