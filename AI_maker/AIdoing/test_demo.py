#!/usr/bin/env python3
"""
CodeMentor AI 演示测试脚本
"""

import requests
import json
import time

def test_demo():
    """测试演示API"""
    base_url = "http://localhost:8000"
    
    print("🧪 开始测试 CodeMentor AI 演示...")
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(3)
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            print(f"   响应: {response.json()}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到API服务: {e}")
        return False
    
    # 测试根路径
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ 根路径访问成功")
            print(f"   响应: {response.json()}")
        else:
            print(f"❌ 根路径访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 根路径访问失败: {e}")
    
    # 测试代码分析
    test_codes = [
        {
            "name": "简单Hello World",
            "code": """
def hello_world():
    print("Hello, World!")
    return "success"

result = hello_world()
print(result)
""",
            "language": "python"
        },
        {
            "name": "循环示例",
            "code": """
for i in range(5):
    print(f"数字: {i}")
    if i % 2 == 0:
        print("这是偶数")
""",
            "language": "python"
        },
        {
            "name": "函数示例",
            "code": """
def calculate_sum(a, b):
    return a + b

def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

# 测试函数
result1 = calculate_sum(10, 20)
result2 = calculate_average([1, 2, 3, 4, 5])
print(f"和: {result1}")
print(f"平均值: {result2}")
""",
            "language": "python"
        }
    ]
    
    for i, test_case in enumerate(test_codes, 1):
        print(f"\n📝 测试代码 {i}: {test_case['name']}")
        try:
            response = requests.post(
                f"{base_url}/api/v1/code/analyze",
                json={
                    "code": test_case["code"],
                    "language": test_case["language"],
                    "topic": "demo"
                }
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 代码分析成功")
                print(f"   评分: {result['score']}")
                print(f"   反馈: {result['feedback']}")
                print(f"   建议数量: {len(result['suggestions'])}")
                if result['suggestions']:
                    print("   建议:")
                    for suggestion in result['suggestions']:
                        print(f"     - {suggestion}")
            else:
                print(f"❌ 代码分析失败: {response.status_code}")
                print(f"   错误: {response.text}")
        except Exception as e:
            print(f"❌ 代码分析请求失败: {e}")
    
    # 测试获取会话历史
    try:
        response = requests.get(f"{base_url}/api/v1/code/sessions")
        if response.status_code == 200:
            sessions = response.json()
            print(f"\n✅ 获取会话历史成功")
            print(f"   会话数量: {len(sessions)}")
            if sessions:
                print("   最近会话:")
                for session in sessions[-3:]:  # 显示最近3个
                    print(f"     - 会话 {session['id']}: {session['language']} (评分: {session['score']})")
        else:
            print(f"❌ 获取会话历史失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取会话历史失败: {e}")
    
    # 测试获取统计信息
    try:
        response = requests.get(f"{base_url}/api/v1/code/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"\n✅ 获取统计信息成功")
            print(f"   总会话数: {stats['total_sessions']}")
            print(f"   平均评分: {stats['average_score']}")
            print(f"   学习时间: {stats['total_learning_time']} 分钟")
            print(f"   用户水平: {stats['user_level']}")
        else:
            print(f"❌ 获取统计信息失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取统计信息失败: {e}")
    
    # 测试获取学习主题
    try:
        response = requests.get(f"{base_url}/api/v1/learning/topics")
        if response.status_code == 200:
            topics = response.json()
            print(f"\n✅ 获取学习主题成功")
            print(f"   主题数量: {len(topics['topics'])}")
            print("   可用主题:")
            for topic in topics['topics']:
                print(f"     - {topic['title']} ({topic['difficulty']}) - {topic['estimated_hours']}小时")
        else:
            print(f"❌ 获取学习主题失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取学习主题失败: {e}")
    
    print("\n🎉 演示测试完成！")
    print("🌐 您可以访问以下地址:")
    print(f"   - API文档: {base_url}/docs")
    print(f"   - 健康检查: {base_url}/health")
    print(f"   - 根路径: {base_url}/")
    print("\n💡 演示功能说明:")
    print("   - 代码分析: 支持Python代码的语法检查和建议")
    print("   - 会话历史: 记录所有代码分析会话")
    print("   - 统计信息: 显示学习进度和评分统计")
    print("   - 学习主题: 提供个性化的学习路径")

if __name__ == "__main__":
    test_demo() 