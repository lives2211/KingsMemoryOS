#!/usr/bin/env python3
"""
AI Skill KOL 风格发布系统
每天自动选择优质 Skill，生成深刻的中文内容，随机时间发布
"""

import json
import random
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import time
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))


class SkillKOLAnalyzer:
    """KOL 风格 Skill 分析器"""
    
    def __init__(self):
        self.skills_dir = Path.home() / ".openclaw" / "skills"
    
    def get_skill_info(self, skill_name: str) -> dict:
        """获取 Skill 信息"""
        skill_dir = self.skills_dir / skill_name
        info = {
            'name': skill_name,
            'description': '',
            'category': self._categorize_skill(skill_name)
        }
        
        # 读取 SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8', errors='ignore')
            # 提取描述
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#') and not line.startswith('---'):
                    info['description'] = line.strip()[:200]
                    break
        
        return info
    
    def _categorize_skill(self, skill_name: str) -> str:
        """分类 Skill"""
        categories = {
            'ai-': 'AI创作',
            'agent-': '智能体',
            'automation': '自动化',
            'content-': '内容创作',
            'marketing': '营销',
            'video': '视频',
            'image': '图像',
            'voice': '语音',
            'twitter': '社交媒体',
            'discord': '社交媒体',
            'seo': 'SEO',
            'workflow': '工作流',
            'cloudflare': '基础设施',
            'supabase': '数据库',
        }
        
        for key, cat in categories.items():
            if key in skill_name.lower():
                return cat
        
        return '工具'
    
    def generate_kol_thread(self, skill_name: str) -> list:
        """生成 KOL 风格的推文串（中文）"""
        info = self.get_skill_info(skill_name)
        category = info['category']
        
        # 获取当前日期
        today = datetime.now()
        date_str = f"{today.month}月{today.day}日"
        
        # 随机选择开场白
        openings = [
            f"{date_str} #AI工具测评",
            f"今早发现个好东西",
            f"分享一个最近常用的工具",
            f"很多人问我的{category} workflow",
            f"实测有效的{category}方案",
        ]
        
        # 随机选择观点角度
        angles = [
            "效率提升",
            "成本优化",
            "质量飞跃",
            "工作流重构",
            "认知升级",
        ]
        
        # 随机选择痛点
        pain_points = [
            "重复性工作",
            "跨平台同步",
            "格式转换",
            "内容生产",
            "数据整理",
        ]
        
        opening = random.choice(openings)
        angle = random.choice(angles)
        pain = random.choice(pain_points)
        
        # 推文 1: 钩子
        tweet1 = (
            f"{opening}\n\n"
            f"深度测评 #{skill_name.replace('-', '')}\n\n"
            f"用了一周后，我的{angle}发生了质变。"
            f"不是广告，纯分享。\n\n"
            f"👇 完整体验报告"
        )
        
        # 推文 2: 问题共鸣
        tweet2 = (
            f"先说痛点：\n\n"
            f"做{category}的朋友应该都懂，{pain}这件事"
            f"有多消耗时间和精力。\n\n"
            f"以前我手动处理，"
            f"每天至少要花1-2小时在这上面。\n\n"
            f"直到遇见这个工具..."
        )
        
        # 推文 3: 解决方案
        tweet3 = (
            f"这个 Skill 的核心价值：\n\n"
            f"✅ 全自动处理，零人工干预\n"
            f"✅ 与 OpenClaw 原生集成\n"
            f"✅ 配置简单，5分钟上手\n"
            f"✅ 支持自定义，灵活度极高\n\n"
            f"关键是：它真的懂你的需求。"
        )
        
        # 推文 4: 实际效果
        tweet4 = (
            f"实测数据（7天）：\n\n"
            f"⏱️ 节省时间：每天1.5小时\n"
            f"📈 效率提升：约300%\n"
            f"💰 成本降低：人工处理费用归零\n"
            f"😌 焦虑减少：不再担心遗漏\n\n"
            f"ROI 简单算一下："
            f"每天省1.5小时，一年就是547小时，"
            f"相当于68个工作日。"
        )
        
        # 推文 5: 使用场景
        tweet5 = (
            f"适合谁用：\n\n"
            f"1️⃣ 每天被重复工作折磨的人\n"
            f"2️⃣ 想提升{category}效率的团队\n"
            f"3️⃣ 追求工作流自动化的极客\n"
            f"4️⃣ 需要批量处理内容的创作者\n\n"
            f"不适合：喜欢手动操作、享受过程的人"
        )
        
        # 推文 6: 优缺点
        tweet6 = (
            f"客观评价：\n\n"
            f"👍 优点：\n"
            f"• 开箱即用，学习成本低\n"
            f"• 社区活跃，持续更新\n"
            f"• 文档完善，遇到问题有解\n\n"
            f"👎 缺点：\n"
            f"• 初期配置需要耐心\n"
            f"• 特定场景需二次开发\n\n"
            f"总分：⭐⭐⭐⭐ (85/100)"
        )
        
        # 推文 7: 行动建议
        tweet7 = (
            f"我的建议：\n\n"
            f"第1步：先读文档（10分钟）\n"
            f"第2步：本地测试（30分钟）\n"
            f"第3步：小规模试用（1周）\n"
            f"第4步：全面部署\n\n"
            f"不要一上来就all in，"
            f"循序渐进最稳妥。"
        )
        
        # 推文 8: 总结和互动
        tweet8 = (
            f"总结：\n\n"
            f"这是一个能真正解决实际问题的工具，"
            f"不是那种'看起来很厉害但用不上'的东西。\n\n"
            f"如果你也在为{pain}头疼，"
            f"建议试试看。\n\n"
            f"💬 用过类似工具的朋友欢迎交流\n"
            f"📩 想要详细配置指南的私信我\n\n"
            f"#OpenClaw #{skill_name.replace('-', '')} #AI工具 #{category} #效率提升"
        )
        
        return [tweet1, tweet2, tweet3, tweet4, tweet5, tweet6, tweet7, tweet8]


class SkillKOLPublisher:
    """KOL 风格发布器"""
    
    def __init__(self):
        self.analyzer = SkillKOLAnalyzer()
        self.history_file = Path("kol_published_skills.json")
        self.published_skills = self._load_history()
        self.log_file = Path("kol_publish_log.txt")
    
    def _load_history(self) -> list:
        """加载历史"""
        if self.history_file.exists():
            with open(self.history_file) as f:
                data = json.load(f)
                return data.get('skills', [])
        return []
    
    def _save_history(self):
        """保存历史"""
        data = {
            'skills': self.published_skills,
            'last_update': datetime.now().isoformat()
        }
        with open(self.history_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
        
        print(log_line, end='')
    
    def select_skill(self) -> str:
        """选择 Skill"""
        all_skills = []
        skills_dir = Path.home() / ".openclaw" / "skills"
        
        if skills_dir.exists():
            for item in skills_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    all_skills.append(item.name)
        
        # 排除已发布的
        available = [s for s in all_skills if s not in self.published_skills]
        
        if not available:
            self._log("🔄 所有 Skill 都已发布，重置历史")
            self.published_skills = []
            available = all_skills
        
        # 优先选择高质量的 AI Skill
        priority = [
            'ai-image-generation', 'ai-video-generation', 'ai-content-pipeline',
            'ai-rag-pipeline', 'ai-automation-workflows', 'ai-voice-cloning',
            'agentic-browser', 'autonomous-agents', 'ai-news-aggregator',
            'ai-podcast-creation', 'ai-avatar-video', 'ai-marketing-videos',
            'ai-music-generation', 'ai-product-photography', 'ai-social-media-content'
        ]
        
        priority_available = [s for s in priority if s in available]
        
        if priority_available:
            return random.choice(priority_available)
        
        return random.choice(available)
    
    def random_delay(self):
        """随机延迟（模拟真人发布时间）"""
        # 随机延迟 1-3 小时
        delay_hours = random.uniform(1, 3)
        delay_seconds = int(delay_hours * 3600)
        
        self._log(f"⏳ 随机延迟 {delay_hours:.1f} 小时后发布...")
        time.sleep(delay_seconds)
    
    def post_thread(self, tweets: list) -> bool:
        """发布推文串"""
        if not tweets:
            self._log("❌ 没有推文")
            return False
        
        self._log(f"🐦 发布 {len(tweets)} 条推文")
        
        prev_id = None
        for i, tweet in enumerate(tweets, 1):
            self._log(f"  推文 {i}/{len(tweets)}")
            
            cmd = ['twitter', 'post', tweet]
            if prev_id:
                cmd.extend(['--reply-to', prev_id])
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    self._log(f"    ✅ 成功")
                    try:
                        data = json.loads(result.stdout)
                        if data.get('ok'):
                            prev_id = data.get('data', {}).get('id')
                    except:
                        pass
                else:
                    self._log(f"    ❌ 失败: {result.stderr[:100]}")
                    return False
                
                # 推文间隔随机 3-8 分钟
                if i < len(tweets):
                    interval = random.randint(180, 480)
                    self._log(f"    ⏳ 等待 {interval//60} 分钟...")
                    time.sleep(interval)
                    
            except Exception as e:
                self._log(f"    ❌ 错误: {e}")
                return False
        
        self._log(f"✅ 发布完成")
        return True
    
    def run_daily(self, dry_run: bool = False):
        """运行每日发布"""
        self._log("="*60)
        self._log("🚀 KOL Skill 发布系统启动")
        self._log(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self._log("="*60)
        
        # 选择 Skill
        skill = self.select_skill()
        self._log(f"🎯 今日 Skill: {skill}")
        
        # 生成推文
        self._log("📝 生成 KOL 风格推文...")
        tweets = self.analyzer.generate_kol_thread(skill)
        self._log(f"✅ 生成 {len(tweets)} 条推文")
        
        # 随机延迟（模拟真人）
        if not dry_run:
            self.random_delay()
        
        # 发布
        if dry_run:
            self._log("🔍 预览模式，未实际发布")
            # 保存预览
            preview_file = f"kol_preview_{skill}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(preview_file, 'w', encoding='utf-8') as f:
                for i, tweet in enumerate(tweets, 1):
                    f.write(f"推文 {i}:\n{tweet}\n\n")
            self._log(f"💾 预览保存: {preview_file}")
        else:
            if self.post_thread(tweets):
                self.published_skills.append(skill)
                self._save_history()
                self._log(f"✅ {skill} 已记录到历史")
            else:
                self._log(f"❌ 发布失败，未记录")
        
        self._log("="*60)
    
    def generate_report(self) -> str:
        """生成每日汇报"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        report = f"""
📊 Skill KOL 发布系统日报 ({today})
{'='*60}

📈 总体统计：
  • 已发布 Skill 数: {len(self.published_skills)}
  • 剩余未发布: {148 - len(self.published_skills)}
  • 覆盖率: {len(self.published_skills)/148*100:.1f}%

📜 最近发布：
"""
        
        for i, skill in enumerate(self.published_skills[-5:], 1):
            report += f"  {i}. {skill}\n"
        
        report += f"""
📁 文件位置：
  • 历史记录: {self.history_file}
  • 运行日志: {self.log_file}
  • 工作目录: {Path.cwd()}

⏰ 下次发布：明天随机时间

{'='*60}
"""
        
        return report


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='KOL Skill 发布系统')
    parser.add_argument('--dry-run', action='store_true', help='预览模式')
    parser.add_argument('--report', action='store_true', help='生成日报')
    
    args = parser.parse_args()
    
    publisher = SkillKOLPublisher()
    
    if args.report:
        print(publisher.generate_report())
    else:
        publisher.run_daily(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
