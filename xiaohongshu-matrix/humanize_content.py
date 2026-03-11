#!/usr/bin/env python3
"""
内容人工化处理模块
- 添加人为痕迹
- 去AI化
- 模拟真人表达
"""

import random
import re
from datetime import datetime

class ContentHumanizer:
    """内容人工化处理器"""
    
    def __init__(self):
        # 口语化开头
        self.openings = [
            "姐妹们，",
            "忍不住来分享一下",
            "刚用完，赶紧来发",
            "真的服了",
            "不得不说",
            "最近发现",
            "",
        ]
        
        # 情绪词
        self.emotions = ["😂", "🤔", "💢", "❗", "✨", "💡", "🔥"]
        
        # 口头禅
        self.fillers = ["真的", "居然", "绝了", "说实话", "讲真", "其实"]
        
        # 个人化表达
        self.personal = [
            "（仅代表个人观点）",
            "（可能是我运气不好）",
            "（你们呢？）",
            "（欢迎补充）",
            "",
        ]
        
        # 结尾互动
        self.engagements = [
            "有问题评论区见",
            "觉得有用就点个赞吧",
            "你们有什么建议吗？",
            "欢迎交流",
            "",
        ]
    
    def humanize(self, content, intensity=0.7):
        """
        人工化处理内容
        intensity: 人工化强度 (0-1)
        """
        if random.random() > intensity:
            return content
        
        # 1. 添加口语化开头 (50%概率)
        if random.random() < 0.5:
            content = self._add_opening(content)
        
        # 2. 插入情绪词和emoji (每篇1-3个)
        content = self._add_emotions(content)
        
        # 3. 添加口头禅
        content = self._add_fillers(content)
        
        # 4. 添加个人化表达 (30%概率)
        if random.random() < 0.3:
            content = self._add_personal(content)
        
        # 5. 添加结尾互动 (50%概率)
        if random.random() < 0.5:
            content = self._add_engagement(content)
        
        # 6. 故意小错误 (20%概率)
        if random.random() < 0.2:
            content = self._add_typos(content)
        
        # 7. 标点符号随机化
        content = self._randomize_punctuation(content)
        
        return content
    
    def _add_opening(self, content):
        """添加口语化开头"""
        opening = random.choice(self.openings)
        if opening and not content.startswith(opening):
            # 如果内容以"#"开头（标题），在标题后添加
            if content.startswith('#'):
                lines = content.split('\n', 1)
                if len(lines) > 1:
                    return lines[0] + '\n\n' + opening + lines[1]
            else:
                return opening + content
        return content
    
    def _add_emotions(self, content):
        """插入情绪词和emoji"""
        count = random.randint(1, 3)
        
        for _ in range(count):
            # 找到合适的位置插入（不在代码块、链接中）
            emotion = random.choice(self.emotions)
            
            # 在句子中间随机位置插入
            sentences = re.split(r'([。！？.\n])', content)
            if len(sentences) > 2:
                pos = random.randint(0, len(sentences) - 2)
                if pos % 2 == 0:  # 确保插在句子中
                    sentences[pos] = sentences[pos] + emotion
                    content = ''.join(sentences)
        
        return content
    
    def _add_fillers(self, content):
        """添加口头禅"""
        filler = random.choice(self.fillers)
        
        # 在第二句开头添加
        sentences = re.split(r'([。！？.\n])', content)
        if len(sentences) >= 3:
            # 找到第二个完整句子
            for i in range(2, len(sentences), 2):
                if sentences[i].strip():
                    sentences[i] = filler + "，" + sentences[i]
                    break
            content = ''.join(sentences)
        
        return content
    
    def _add_personal(self, content):
        """添加个人化表达"""
        personal = random.choice(self.personal)
        if personal:
            # 在段落中间插入
            paragraphs = content.split('\n\n')
            if len(paragraphs) >= 2:
                pos = random.randint(1, len(paragraphs) - 1)
                paragraphs[pos] = paragraphs[pos] + '\n' + personal
                content = '\n\n'.join(paragraphs)
        return content
    
    def _add_engagement(self, content):
        """添加结尾互动"""
        engagement = random.choice(self.engagements)
        if engagement and not content.rstrip().endswith('？'):
            content = content.rstrip() + '\n\n' + engagement
        return content
    
    def _add_typos(self, content):
        """添加故意的小错误"""
        # 随机替换一个"的"为"得"或"地"
        if "的" in content:
            positions = [m.start() for m in re.finditer(r'的', content)]
            if positions:
                pos = random.choice(positions)
                replacement = random.choice(["得", "地"])
                content = content[:pos] + replacement + content[pos+1:]
        
        # 偶尔添加错别字
        typos = {
            "吧": "巴",
            "呢": "呐",
            "啊": "阿",
        }
        for correct, wrong in typos.items():
            if correct in content and random.random() < 0.3:
                content = content.replace(correct, wrong, 1)
                break
        
        return content
    
    def _randomize_punctuation(self, content):
        """随机化标点符号"""
        # 偶尔把句号换成省略号或感叹号
        if random.random() < 0.3:
            content = content.replace("。", "...", 1)
        
        if random.random() < 0.2:
            content = content.replace("。", "！", 1)
        
        # 偶尔添加多个感叹号
        if random.random() < 0.2:
            content = content.replace("！", "！！", 1)
        
        return content
    
    def generate_human_time(self, base_hour, window=2):
        """
        生成符合人类习惯的时间
        base_hour: 基础小时
        window: 时间窗口（小时）
        """
        # 在基础时间前后随机偏移
        hour_offset = random.randint(-window//2, window//2)
        minute = random.randint(0, 59)
        
        # 避免整点和半点（太规律）
        if minute in [0, 30]:
            minute += random.choice([-1, 1]) * random.randint(1, 5)
            minute = max(0, min(59, minute))
        
        final_hour = base_hour + hour_offset
        final_hour = max(6, min(23, final_hour))  # 限制在6-23点
        
        return f"{final_hour:02d}:{minute:02d}"
    
    def randomize_posting_schedule(self, num_posts=3):
        """
        生成随机的发布计划
        """
        time_windows = [
            (7, 30, 9, 30),    # 早上
            (11, 30, 13, 30),  # 中午
            (18, 0, 21, 0),    # 晚上
        ]
        
        schedule = []
        
        for i in range(num_posts):
            if i < len(time_windows):
                window = time_windows[i]
                start_h, start_m, end_h, end_m = window
                
                # 70%概率在这个时间段发布
                if random.random() < 0.7:
                    hour = random.randint(start_h, end_h)
                    minute = random.randint(0, 59)
                    
                    # 避免整点
                    if minute == 0:
                        minute = random.randint(1, 59)
                    
                    schedule.append(f"{hour:02d}:{minute:02d}")
        
        # 随机打乱
        random.shuffle(schedule)
        
        return schedule

# 便捷函数
def humanize_content(content, intensity=0.7):
    """快速人工化内容"""
    humanizer = ContentHumanizer()
    return humanizer.humanize(content, intensity)

if __name__ == "__main__":
    # 测试
    test_content = """# 先说结论：值得买

实测3天，发现3个问题。

## 优点
1. 续航好
2. 性能强
3. 做工好

## 缺点
1. 发热
2. 价格贵

适合预算充足的用户。"""
    
    print("原始内容:")
    print(test_content)
    print("\n" + "="*50 + "\n")
    
    humanizer = ContentHumanizer()
    
    for i in range(3):
        print(f"人工化版本 {i+1}:")
        result = humanizer.humanize(test_content)
        print(result)
        print("\n" + "-"*50 + "\n")
