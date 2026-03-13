"""
Discord 总指挥频道自动派发器
基于 Paperclip 架构：智能识别 → 自动解析 → 即时派发
"""

import re
import json
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

API_URL = "http://localhost:3100"

@dataclass
class ParsedTask:
    """解析后的任务"""
    title: str
    description: str
    budget: float
    priority: str
    skills_required: List[str]
    confidence: float

class TaskParser:
    """
    任务解析器 - 借鉴 Paperclip 的意图识别
    
    从自然语言中提取:
    - 任务类型/技能需求
    - 预算
    - 优先级
    - 时间要求
    """
    
    # 技能关键词映射 (9 Agents - agency-agents 优化版)
    SKILL_PATTERNS = {
        # === Engineering Division ===
        "yitai": {
            "keywords": ["编程", "写程序", "脚本", "开发", "调试", "爬取", "修复bug", "bug修复",
                        "python", "javascript", "实现功能", "功能开发", "写代码", "接口实现",
                        "爬虫", "抓取", "spider", "crawl"],
            "weight": 1.0
        },
        "architect": {
            "keywords": ["架构", "设计", "方案", "技术选型", "重构", "微服务", "ddd", 
                        "系统", "模块", "接口设计", "数据库设计", "api设计", "架构图", 
                        "技术栈", "性能优化", "扩展性", "高并发", "分布式", "系统设计"],
            "weight": 1.2  # 架构任务权重更高
        },
        "devops": {
            "keywords": ["部署", "ci/cd", "docker", "kubernetes", "k8s", "自动化", 
                        "pipeline", "github actions", "jenkins", "监控", "日志", "nginx", 
                        "服务器", "运维", "域名", "cdn", "负载均衡", "容器", "配置环境",
                        "持续集成", "持续部署", "devops"],
            "weight": 1.2
        },
        
        # === Design Division ===
        "bingbing": {
            "keywords": ["设计", "创意", "封面", "内容", "文案", "写作", "图像", "视频",
                      "logo", "海报", "banner", "ui", "ux", "插画", "配图", "视觉", "品牌"],
            "weight": 1.0
        },
        
        # === Data Division ===
        "daping": {
            "keywords": ["分析", "数据", "检测", "监控", "竞品", "调研", "报表", "可视化", "统计"],
            "weight": 1.0
        },
        
        # === Quality Division ===
        "spikey": {
            "keywords": ["审计", "复盘", "质量", "审查", "检查", "代码审查", "代码质量", "审计代码"],
            "weight": 1.2
        },
        "security": {
            "keywords": ["安全", "漏洞", "渗透", "防护", "xss", "sql注入", "csrf", 
                        "加密", "https", "安全扫描", "owasp", "鉴权", "认证", "授权", "token", "jwt",
                        "ssl证书", "安全审计", "安全检查", "安全加固"],
            "weight": 1.3  # 安全任务权重更高
        },
        
        # === Growth Division ===
        "xiaohongcai": {
            "keywords": ["社媒", "运营", "发布", "小红书", "公众号", "内容运营"],
            "weight": 1.0
        },
        
        # === Product Division ===
        "pm": {
            "keywords": ["产品", "需求", "prd", "用户故事", "功能设计", "原型", "流程图", 
                        "竞品分析", "用户调研", "优先级", "路线图", "mvp", "迭代", "版本规划",
                        "产品功能", "产品设计", "产品需求", "产品文档"],
            "weight": 1.2  # 产品任务权重更高
        }
    }
    
    # 预算模式
    BUDGET_PATTERNS = [
        r'(\d+)\s*刀',
        r'(\d+)\s*美元',
        r'(\d+)\s*元',
        r'预算\s*(\d+)',
        r'(\d+)\s*usd',
        r'\$(\d+)',
    ]
    
    # 优先级关键词
    PRIORITY_PATTERNS = {
        "urgent": ["紧急", "urgent", "急", "马上", "立即", "asap", "今天"],
        "high": ["高优先级", "high", "重要", "优先", "尽快"],
        "low": ["低优先级", "low", "不急", "有空再说"]
    }
    
    def parse(self, message: str) -> ParsedTask:
        """解析消息为结构化任务"""
        msg_lower = message.lower()
        
        # 1. 提取预算
        budget = self._extract_budget(message)
        
        # 2. 提取优先级
        priority = self._extract_priority(msg_lower)
        
        # 3. 匹配技能
        agent_id, confidence, skills = self._match_skills(msg_lower)
        
        # 4. 生成标题
        title = self._generate_title(message)
        
        return ParsedTask(
            title=title,
            description=message,
            budget=budget,
            priority=priority,
            skills_required=skills,
            confidence=confidence
        )
    
    def _extract_budget(self, message: str) -> float:
        """提取预算"""
        for pattern in self.BUDGET_PATTERNS:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return float(match.group(1))
        return 0.0
    
    def _extract_priority(self, message: str) -> str:
        """提取优先级"""
        for priority, keywords in self.PRIORITY_PATTERNS.items():
            for kw in keywords:
                if kw in message:
                    return priority
        return "normal"
    
    def _match_skills(self, message: str) -> Tuple[str, float, List[str]]:
        """匹配技能，返回最佳 Agent"""
        scores = {}
        matched_skills = {}
        
        for agent_id, config in self.SKILL_PATTERNS.items():
            score = 0
            skills = []
            for keyword in config["keywords"]:
                if keyword in message:
                    score += config["weight"]
                    skills.append(keyword)
            scores[agent_id] = score
            matched_skills[agent_id] = skills
        
        # 找出最佳匹配
        best_agent = max(scores, key=scores.get)
        best_score = scores[best_agent]
        
        # 计算置信度
        total_keywords = sum(len(matched_skills[a]) for a in matched_skills)
        confidence = best_score / total_keywords if total_keywords > 0 else 0.0
        
        return best_agent, confidence, matched_skills[best_agent]
    
    def _generate_title(self, message: str) -> str:
        """生成任务标题"""
        # 取前 30 个字符作为标题
        title = message.strip()
        if len(title) > 30:
            title = title[:30] + "..."
        return title


class DiscordDispatcher:
    """
    Discord 自动派发器
    
    Paperclip 风格的工作流:
    1. 监听消息
    2. 解析意图
    3. 匹配 Agent
    4. 创建任务
    5. 通知结果
    """
    
    def __init__(self):
        self.parser = TaskParser()
        
    def dispatch(self, message: str, user: str = "unknown") -> Dict:
        """
        派发任务主流程
        
        Args:
            message: 用户消息
            user: 用户名
            
        Returns:
            派发结果
        """
        # 1. 解析任务
        task = self.parser.parse(message)
        
        # 2. 创建任务
        result = self._create_task(task, user)
        
        # 3. 生成回复
        reply = self._generate_reply(result, task)
        
        return {
            "success": result.get("id") is not None,
            "task": result,
            "parsed": task,
            "reply": reply
        }
    
    def _create_task(self, task: ParsedTask, user: str) -> Dict:
        """调用 API 创建任务"""
        try:
            resp = requests.post(
                f"{API_URL}/api/tasks",
                json={
                    "title": task.title,
                    "description": task.description,
                    "budget": task.budget,
                    "priority": task.priority,
                    "requester": user
                },
                timeout=10
            )
            return resp.json() if resp.status_code == 201 else {}
        except Exception as e:
            print(f"[Dispatcher] 创建任务失败: {e}")
            return {}
    
    def _generate_reply(self, result: Dict, parsed: ParsedTask) -> str:
        """生成 Discord 回复"""
        if not result.get("id"):
            return "❌ 任务派发失败，请稍后重试"
        
        agent_name = result.get("agent_name", "unknown")
        agent_role = result.get("agent_role", "未知")
        
        # Emoji 映射
        emoji_map = {
            "yitai": "💻",
            "bingbing": "🎨",
            "daping": "📊",
            "spikey": "🔍",
            "xiaohongcai": "📱"
        }
        emoji = emoji_map.get(agent_name, "🤖")
        
        reply = f"""🤖 任务已派发

📋 **{result['title']}**
👤 指派给: {emoji} @{agent_name} ({agent_role})
🆔 任务ID: `{result['id']}`
💰 预算: ${result['budget']['total']}
✅ 状态: {result['status']}
"""
        
        if parsed.confidence < 0.5:
            reply += "\n⚠️ 置信度较低，可能需要人工确认"
        
        reply += "\n💡 查看详情: http://localhost:3100/dashboard_v2.html"
        
        return reply
    
    def should_dispatch(self, message: str) -> bool:
        """判断是否应该派发任务"""
        import re
        
        # 任务触发关键词
        triggers = [
            "帮我", "我要", "我想", "需要", "请",
            "做一个", "写个", "设计", "分析", "爬取",
            "生成", "创建", "制作", "开发", "修复",
            "审计", "检查", "测试", "优化", "部署",
            "写", "画", "做", "整"
        ]
        
        msg_lower = message.lower()
        
        # 检查是否包含触发词
        has_trigger = any(t in msg_lower for t in triggers)
        
        # 检查是否包含预算（可选）
        has_budget = self.parser._extract_budget(message) > 0
        
        # 检查是否 @ 了特定 Agent
        mentioned_agent = re.search(r'@(\w+)', message)
        
        result = has_trigger or has_budget or bool(mentioned_agent)
        return result



# 全局派发器实例
dispatcher = DiscordDispatcher()


def handle_discord_message(message: str, user: str = "unknown") -> Optional[str]:
    """
    处理 Discord 消息
    
    这是主入口函数，在总指挥频道收到消息时调用
    """
    # 检查是否应该派发
    if not dispatcher.should_dispatch(message):
        return None
    
    # 执行派发
    result = dispatcher.dispatch(message, user)
    
    return result.get("reply")


# 测试
if __name__ == "__main__":
    # 测试用例
    test_messages = [
        "帮我爬取 Twitter 数据，预算10美元",
        "设计一个小红书封面，5刀",
        "分析一下竞品数据",
        "帮我修复登录bug，紧急",
        "写一篇公众号文章"
    ]
    
    print("🦞 Discord Dispatcher 测试\n")
    
    for msg in test_messages:
        print(f"输入: {msg}")
        reply = handle_discord_message(msg, "candycion")
        if reply:
            print(f"回复:\n{reply}\n")
        else:
            print("未触发派发\n")
