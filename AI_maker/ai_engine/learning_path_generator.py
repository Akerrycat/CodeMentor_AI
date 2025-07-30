import openai
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class LearningTopic:
    id: str
    title: str
    description: str
    difficulty: SkillLevel
    estimated_hours: int
    prerequisites: List[str]
    tags: List[str]

@dataclass
class LearningPath:
    user_id: str
    current_level: SkillLevel
    target_level: SkillLevel
    topics: List[LearningTopic]
    estimated_completion_time: int  # 小时
    progress: float = 0.0

class LearningPathGenerator:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        
        # 预定义的学习主题
        self.topics_database = self._initialize_topics()
    
    def _initialize_topics(self) -> Dict[str, LearningTopic]:
        """初始化学习主题数据库"""
        topics = {
            # Python 基础主题
            "python_basics": LearningTopic(
                id="python_basics",
                title="Python基础语法",
                description="学习Python的基本语法、变量、数据类型、控制流等",
                difficulty=SkillLevel.BEGINNER,
                estimated_hours=10,
                prerequisites=[],
                tags=["python", "基础", "语法"]
            ),
            "python_functions": LearningTopic(
                id="python_functions",
                title="函数和模块",
                description="学习函数定义、参数传递、模块导入等",
                difficulty=SkillLevel.BEGINNER,
                estimated_hours=8,
                prerequisites=["python_basics"],
                tags=["python", "函数", "模块"]
            ),
            "python_oop": LearningTopic(
                id="python_oop",
                title="面向对象编程",
                description="学习类、对象、继承、多态等OOP概念",
                difficulty=SkillLevel.INTERMEDIATE,
                estimated_hours=12,
                prerequisites=["python_functions"],
                tags=["python", "OOP", "类"]
            ),
            "python_data_structures": LearningTopic(
                id="python_data_structures",
                title="数据结构",
                description="学习列表、字典、集合、元组等数据结构",
                difficulty=SkillLevel.BEGINNER,
                estimated_hours=6,
                prerequisites=["python_basics"],
                tags=["python", "数据结构"]
            ),
            "python_algorithms": LearningTopic(
                id="python_algorithms",
                title="算法基础",
                description="学习排序、搜索、递归等基础算法",
                difficulty=SkillLevel.INTERMEDIATE,
                estimated_hours=15,
                prerequisites=["python_data_structures"],
                tags=["python", "算法"]
            ),
            "python_web": LearningTopic(
                id="python_web",
                title="Web开发基础",
                description="学习Flask/Django框架进行Web开发",
                difficulty=SkillLevel.INTERMEDIATE,
                estimated_hours=20,
                prerequisites=["python_oop"],
                tags=["python", "web", "框架"]
            ),
            "python_ai": LearningTopic(
                id="python_ai",
                title="人工智能入门",
                description="学习机器学习基础，使用scikit-learn等库",
                difficulty=SkillLevel.ADVANCED,
                estimated_hours=25,
                prerequisites=["python_algorithms"],
                tags=["python", "AI", "机器学习"]
            )
        }
        return topics
    
    def generate_personalized_path(self, user_profile: Dict) -> LearningPath:
        """生成个性化学习路径"""
        current_level = SkillLevel(user_profile.get("skill_level", "beginner"))
        target_level = self._determine_target_level(current_level)
        programming_languages = user_profile.get("programming_languages", [])
        
        # 根据用户水平选择合适的话题
        selected_topics = self._select_topics_for_level(current_level, programming_languages)
        
        # 使用AI优化学习路径
        optimized_topics = self._optimize_path_with_ai(selected_topics, user_profile)
        
        # 计算预计完成时间
        total_hours = sum(topic.estimated_hours for topic in optimized_topics)
        
        return LearningPath(
            user_id=user_profile.get("user_id", ""),
            current_level=current_level,
            target_level=target_level,
            topics=optimized_topics,
            estimated_completion_time=total_hours
        )
    
    def _determine_target_level(self, current_level: SkillLevel) -> SkillLevel:
        """确定目标水平"""
        if current_level == SkillLevel.BEGINNER:
            return SkillLevel.INTERMEDIATE
        elif current_level == SkillLevel.INTERMEDIATE:
            return SkillLevel.ADVANCED
        else:
            return SkillLevel.ADVANCED  # 已经是高级水平
    
    def _select_topics_for_level(self, level: SkillLevel, languages: List[str]) -> List[LearningTopic]:
        """根据水平选择话题"""
        selected_topics = []
        
        if level == SkillLevel.BEGINNER:
            # 初学者：基础语法 + 数据结构
            selected_topics = [
                self.topics_database["python_basics"],
                self.topics_database["python_data_structures"],
                self.topics_database["python_functions"]
            ]
        elif level == SkillLevel.INTERMEDIATE:
            # 中级：OOP + 算法 + Web开发
            selected_topics = [
                self.topics_database["python_oop"],
                self.topics_database["python_algorithms"],
                self.topics_database["python_web"]
            ]
        else:
            # 高级：AI/ML + 高级主题
            selected_topics = [
                self.topics_database["python_ai"]
            ]
        
        return selected_topics
    
    def _optimize_path_with_ai(self, topics: List[LearningTopic], user_profile: Dict) -> List[LearningTopic]:
        """使用AI优化学习路径"""
        topic_names = [topic.title for topic in topics]
        
        prompt = f"""
        用户信息：
        - 当前水平：{user_profile.get('skill_level', 'beginner')}
        - 编程语言：{user_profile.get('programming_languages', [])}
        - 学习目标：{user_profile.get('learning_goals', '提高编程技能')}
        
        建议的学习主题：{topic_names}
        
        请根据用户情况，优化学习顺序和内容，并给出具体的学习建议。
        返回JSON格式：
        {{
            "optimized_order": ["topic1", "topic2", ...],
            "learning_tips": ["建议1", "建议2", ...],
            "estimated_weeks": 数字
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # 这里应该解析AI响应并重新排序topics
            # 简化处理，直接返回原顺序
            return topics
            
        except Exception as e:
            print(f"AI优化失败: {e}")
            return topics
    
    def get_next_topic(self, learning_path: LearningPath, completed_topics: List[str]) -> Optional[LearningTopic]:
        """获取下一个学习主题"""
        for topic in learning_path.topics:
            if topic.id not in completed_topics:
                # 检查前置条件是否满足
                if self._check_prerequisites(topic, completed_topics):
                    return topic
        return None
    
    def _check_prerequisites(self, topic: LearningTopic, completed_topics: List[str]) -> bool:
        """检查前置条件是否满足"""
        for prereq in topic.prerequisites:
            if prereq not in completed_topics:
                return False
        return True
    
    def update_progress(self, learning_path: LearningPath, completed_topics: List[str]) -> float:
        """更新学习进度"""
        total_topics = len(learning_path.topics)
        completed_count = len([t for t in learning_path.topics if t.id in completed_topics])
        
        progress = (completed_count / total_topics) * 100
        learning_path.progress = progress
        
        return progress
    
    def generate_encouragement(self, progress: float, user_level: str) -> str:
        """生成鼓励信息"""
        if progress >= 90:
            return "🎉 太棒了！你已经接近完成学习路径，继续保持这个势头！"
        elif progress >= 70:
            return "👍 做得很好！你已经完成了大部分内容，继续加油！"
        elif progress >= 50:
            return "📚 进度不错！你已经完成了一半，坚持就是胜利！"
        elif progress >= 30:
            return "💪 好的开始！学习是一个渐进的过程，保持耐心！"
        else:
            return "🚀 学习之旅刚刚开始！每一步都是进步，相信自己！" 