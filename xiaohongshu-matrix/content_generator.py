#!/usr/bin/env python3
"""
小红书内容生成器
- 根据人设生成文案
- 调用render_xhs生成图片
- 集成人工化处理（去AI化）
"""

import os
import sys
import random
import subprocess
from pathlib import Path
from datetime import datetime

# 导入人工化模块
from humanize_content import ContentHumanizer

# 内容模板库
CONTENT_TEMPLATES = {
    "tech-geek": {
        "titles": [
            "实测{X}天，这{Y}个缺点不吐不快",
            "先说结论：{product}值得买吗？",
            "对比了{X}款，这款是智商税",
            "{price}元档位，这{Y}款怎么选？",
            "用了{X}个月，说说真实体验"
        ],
        "topics": [
            "手机评测", "笔记本推荐", "耳机对比", "智能家居", "数码配件",
            "性价比之选", "避坑指南", "新品开箱", "长期使用报告"
        ]
    },
    "life-aesthetics": {
        "titles": [
            "不到{price}元，get同款氛围感",
            "这个角落，是我每天最治愈的地方",
            "租房改造｜{X}平米也能拥有的{style}",
            "{X}件提升幸福感的小物",
            "回到家，开灯的那一刻..."
        ],
        "topics": [
            "家居布置", "氛围感打造", "平价好物", "租房改造", "生活仪式感",
            "收纳整理", "绿植养护", "灯光设计"
        ]
    },
    "career-growth": {
        "titles": [
            "我面过{X}人，这{Y}种简历直接pass",
            "先说结论：这样做没用",
            "从{level}到{target}，我只做了这{X}件事",
            "别卷了，用这个方法效率翻倍",
            "工作{X}年，这{Y}个真相没人告诉你"
        ],
        "topics": [
            "面试技巧", "简历优化", "职场沟通", "效率提升", "升职加薪",
            "副业探索", "时间管理", "向上管理"
        ]
    },
    "foodie": {
        "titles": [
            "先说结论：值得排队/快跑",
            "网红店实测，这{Y}道是智商税",
            "人均{price}，吃到扶墙出",
            "隐藏小店｜第{X}次来了",
            "在家复刻｜{dish}原来这么简单"
        ],
        "topics": [
            "探店测评", "隐藏小店", "网红店实测", "在家复刻", "美食避坑",
            "性价比之选", "本地美食", "异国料理"
        ]
    },
    "fashion": {
        "titles": [
            "{price}元的平替，效果不输大牌",
            "一件单品搭出{X}种风格",
            "小个子/高个子都能穿的{style}",
            "{season}穿搭｜这{Y}套look请收好",
            "平价也能穿出高级感"
        ],
        "topics": [
            "一衣多穿", "平价替代", "季节穿搭", "职场穿搭", "学生党穿搭",
            "显高显瘦", "色彩搭配", "基础款改造"
        ]
    }
}

class ContentGenerator:
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        self.base_path = Path(base_path)
        self.content_gen_path = self.base_path / "content-gen"
        
    def generate_title(self, account_type):
        """生成标题"""
        templates = CONTENT_TEMPLATES[account_type]["titles"]
        template = random.choice(templates)
        
        # 替换变量
        variables = {
            "{X}": str(random.randint(2, 10)),
            "{Y}": str(random.randint(2, 5)),
            "{price}": str(random.choice([29, 49, 99, 199, 299, 499])),
            "{product}": random.choice(["iPhone", "AirPods", "机械键盘", "显示器"]),
            "{style}": random.choice(["ins风", "原木风", "极简风", "复古风"]),
            "{level}": random.choice(["专员", "主管", "经理"]),
            "{target}": random.choice(["总监", "VP", "专家"]),
            "{dish}": random.choice(["红烧肉", "提拉米苏", "韩式拌饭", "奶茶"]),
            "{season}": random.choice(["春日", "夏日", "秋日", "冬日"])
        }
        
        title = template
        for var, value in variables.items():
            title = title.replace(var, value)
        
        return title
    
    def generate_content(self, account_type, title):
        """生成正文内容"""
        topics = CONTENT_TEMPLATES[account_type]["topics"]
        topic = random.choice(topics)
        
        # 根据账号类型生成不同风格的内容
        if account_type == "tech-geek":
            content = f"""# {title}

先说结论，再展开说。

## 核心参数
- 测试周期：{random.randint(3, 30)}天
- 使用场景：日常主力/备用
- 购买价格：¥{random.randint(100, 5000)}

## 优点
1. 续航实测：{random.randint(5, 12)}小时，比官方数据{random.choice(["高", "低"])}{random.randint(5, 20)}%
2. 性能表现：{random.choice(["流畅", "够用", "略有卡顿"])}
3. 做工质感：{random.choice(["超预期", "符合价位", "一般"])}

## 缺点（不吐不快）
1. {random.choice(["发热控制一般", "充电速度偏慢", "系统偶有bug", "配件生态不完善"])}
2. {random.choice(["性价比一般", "同价位有更好的选择", "降价后再考虑"])}

## 适合谁？
{random.choice(["预算有限的学生党", "追求实用的上班族", "数码爱好者", "备用机需求"])}

## 不适合谁？
{random.choice(["重度游戏玩家", "专业创作者", "追求极致体验的用户"])}

有问题评论区见，看到都会回。
"""
        elif account_type == "life-aesthetics":
            content = f"""# {title}

每天回到家，最期待的就是这一刻。

## 改造思路
不需要大动干戈，{random.choice(["一盏灯", "一块地毯", "几株绿植", "一幅画"])}就能改变氛围。

## 清单分享
- {random.choice(["台灯", "香薰", "抱枕", "挂画"])}：¥{random.randint(20, 200)}
- {random.choice(["绿植", "花瓶", "收纳盒", "桌布"])}：¥{random.randint(15, 150)}
- {random.choice(["地毯", "窗帘", "置物架", "镜子"])}：¥{random.randint(50, 300)}

## 小tips
{random.choice([
    "灯光色温选3000K，最治愈",
    "绿植选耐阴的，好养活",
    "小物件统一色调，不乱",
    "留白很重要，别塞太满"
])}

你的治愈角落是什么样的？评论区聊聊～
"""
        elif account_type == "career-growth":
            content = f"""# {title}

直接上干货，不废话。

## 核心认知
{random.choice([
    "努力是最不值钱的东西，方向才对",
    "职场不是学校，没人有义务教你",
    "会哭的孩子有奶吃，要会争取",
    "你的价值=解决问题的能力"
])}

## 具体方法
1. **{random.choice(["主动汇报", "建立人脉", "提升能见度", "打造代表作"])}**
   - 具体做法：...
   - 预期效果：...

2. **{random.choice(["向上管理", "横向协作", "时间管理", "情绪管理"])}**
   - 核心技巧：...
   - 避坑指南：...

3. **{random.choice(["持续学习", "建立个人品牌", "积累资源", "规划路径"])}**
   - 行动清单：...
   - 时间节点：...

## 最后说两句
{random.choice([
    "别等准备好了再开始，先动起来",
    "职场没有标准答案，只有适合你的解法",
    "你的职业生涯很长，别急于一时的得失"
])}

有问题评论区，看到都会回。
"""
        elif account_type == "foodie":
            content = f"""# {title}

嘴刁认证，真实测评。

## 基本信息
- 店名：{random.choice(["某某小馆", "隐藏食堂", "街边老店", "新晋网红"])}
- 地址：{random.choice(["老城区", "商圈附近", "巷子深处", "地铁口"])}
- 人均：¥{random.randint(30, 200)}

## 菜品实测
**{random.choice(["招牌菜", "必点菜", "特色菜", "隐藏菜单"])}**
- 口味：{random.choice(["超预期", "正常水平", "略失望", "踩雷"])}
- 分量：{random.choice(["扎实", "适中", "偏少"])}
- 性价比：{random.choice(["高", "一般", "偏低"])}

**{random.choice(["主食", "配菜", "饮品", "甜品"])}**
- 评价：...

## 排队建议
- 最佳时间：{random.choice(["工作日中午", "下午3点", "晚上8点后"])}
- 等位时长：{random.randint(10, 60)}分钟

## 总结
{random.choice(["值得专程去", "路过可以试试", "期待值别太高", "快跑"])}

还有哪家想让我测的？评论区告诉我。
"""
        else:  # fashion
            content = f"""# {title}

平价穿搭，高级感拿捏。

## 单品信息
- {random.choice(["上衣", "外套", "裤子", "裙子"])}：¥{random.randint(50, 300)}
- {random.choice(["鞋子", "包包", "配饰", "帽子"])}：¥{random.randint(30, 200)}

## 搭配思路
**Look 1：{random.choice(["通勤风", "休闲风", "约会风", "街头风"])}**
- 要点：{random.choice(["同色系", "撞色", "层次感", "简约"])}

**Look 2：{random.choice(["正式场合", "周末出游", "日常上课", "聚会"])}**
- 要点：...

**Look 3：{random.choice(["换季穿搭", "小个子专属", "显高技巧", "遮肉秘诀"])}**
- 要点：...

## 购买建议
- 尺码：{random.choice(["正码", "偏大", "偏小", "建议试穿"])}
- 质量：{random.choice(["超预期", "符合价位", "一般"])}
- 推荐指数：{'⭐' * random.randint(3, 5)}

还想看什么搭配？评论区告诉我。
"""
        
        return content
    
    def create_markdown_file(self, account_type, title, content):
        """创建markdown文件"""
        output_dir = self.base_path / "generated" / account_type
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{account_type}.md"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def render_images(self, markdown_file, theme, mode="auto-split"):
        """调用render_xhs生成图片"""
        script_path = self.content_gen_path / "scripts" / "render_xhs.py"
        
        cmd = [
            "python3", str(script_path),
            str(markdown_file),
            "-t", theme,
            "-m", mode
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.content_gen_path)
            if result.returncode == 0:
                print(f"✅ 渲染成功: {markdown_file}")
                return True
            else:
                print(f"❌ 渲染失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 渲染异常: {e}")
            return False
    
    def generate_post(self, account_type, humanize=True):
        """生成完整帖子（文案+图片）"""
        # 生成标题
        title = self.generate_title(account_type)
        
        # 生成内容
        content = self.generate_content(account_type, title)
        
        # 人工化处理（去AI化）
        if humanize:
            humanizer = ContentHumanizer()
            content = humanizer.humanize(content, intensity=0.7)
            print("🎭 内容已人工化处理")
        
        # 创建markdown文件
        md_file = self.create_markdown_file(account_type, title, content)
        
        # 获取主题配置
        from scheduler import ACCOUNTS
        theme = ACCOUNTS[account_type]["theme"]
        mode = ACCOUNTS[account_type]["mode"]
        
        # 渲染图片
        success = self.render_images(md_file, theme, mode)
        
        return {
            "title": title,
            "content": content,
            "markdown_file": str(md_file),
            "rendered": success,
            "humanized": humanize
        }

if __name__ == "__main__":
    generator = ContentGenerator()
    
    # 测试生成
    for account in ["tech-geek", "life-aesthetics", "career-growth", "foodie", "fashion"]:
        print(f"\n🦞 测试生成: {account}")
        result = generator.generate_post(account)
        print(f"标题: {result['title'][:30]}...")
        print(f"渲染: {'✅' if result['rendered'] else '❌'}")
