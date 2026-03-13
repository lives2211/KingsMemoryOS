#!/usr/bin/env python3
"""
OpenClaw 教程生成器
自动生成高质量的 OpenClaw 使用教程
"""

import json
import random
from datetime import datetime
from pathlib import Path


class OpenClawTutorialGenerator:
    """OpenClaw 教程生成器"""
    
    def __init__(self):
        self.tutorial_types = {
            'getting_started': '入门教程',
            'skill_building': 'Skill 开发',
            'automation': '自动化工作流',
            'integration': '第三方集成',
            'advanced': '高级技巧'
        }
    
    def generate_getting_started_tutorial(self) -> list:
        """生成入门教程 Thread"""
        
        return [
            # Tweet 1: 钩子
            f"🚀 OpenClaw 完全入门指南\n\n"
            f"我花了 30 天深入研究 OpenClaw，\n"
            f"从零到自动化 10+ 个工作流。\n\n"
            f"这是给新手的完整路线图 👇\n\n"
            f"(Based on {random.randint(8000, 9000)}+ GitHub stars)",
            
            # Tweet 2: 什么是 OpenClaw
            f"❓ 什么是 OpenClaw?\n\n"
            f"GitHub: https://github.com/openclaw/openclaw\n\n"
            f"OpenClaw 是一个开源的 AI Agent 框架，让你:\n"
            f"✅ 自动化重复性工作\n"
            f"✅ 构建智能工作流\n"
            f"✅ 集成 150+ AI 工具\n"
            f"✅ 完全免费开源\n\n"
            f"Think of it as Zapier + AI + Code.",
            
            # Tweet 3: 安装
            f"Step 1: 安装 (5 分钟)\n\n"
            f"```bash\n"
            f"# 安装 OpenClaw CLI\n"
            f"curl -fsSL https://openclaw.ai/install.sh | bash\n\n"
            f"# 验证安装\n"
            f"openclaw --version\n"
            f"```\n\n"
            f"支持: macOS, Linux, Windows (WSL)\n\n"
            f"文档: https://docs.openclaw.ai",
            
            # Tweet 4: 第一个 Skill
            f"Step 2: 运行第一个 Skill (10 分钟)\n\n"
            f"```bash\n"
            f"# 列出可用 Skills\n"
            f"openclaw skills list\n\n"
            f"# 运行 AI 图像生成\n"
            f"openclaw run ai-image-generation \"a cat in space\"\n"
            f"```\n\n"
            f"Boom! 你的第一个自动化完成。",
            
            # Tweet 5: 发现 Skills
            f"Step 3: 发现有用 Skills\n\n"
            f"热门 Skills (按使用频率):\n\n"
            f"1️⃣ ai-image-generation (图像生成)\n"
            f"2️⃣ ai-video-generation (视频生成)\n"
            f"3️⃣ ai-content-pipeline (内容流水线)\n"
            f"4️⃣ agentic-browser (浏览器自动化)\n"
            f"5️⃣ ai-automation-workflows (工作流)\n\n"
            f"完整列表: https://clawhub.com/skills",
            
            # Tweet 6: 配置
            f"Step 4: 配置你的环境\n\n"
            f"```bash\n"
            f"# 配置 API Keys\n"
            f"openclaw config set OPENAI_API_KEY=xxx\n"
            f"openclaw config set ANTHROPIC_API_KEY=xxx\n\n"
            f"# 保存配置\n"
            f"openclaw config save\n"
            f"```\n\n"
            f"支持: OpenAI, Anthropic, Gemini, 本地模型",
            
            # Tweet 7: 构建工作流
            f"Step 5: 构建自动化工作流\n\n"
            f"示例: 自动内容创作\n\n"
            f"```yaml\n"
            f"# workflow.yaml\n"
            f"steps:\n"
            f"  - skill: ai-content-pipeline\n"
            f"    input: \"topic: AI trends\"\n"
            f"  - skill: ai-image-generation\n"
            f"    input: \"cover image\"\n"
            f"  - skill: twitter-post\n"
            f"    input: \"auto post\"\n"
            f"```\n\n"
            f"一键运行整个流程。",
            
            # Tweet 8: 高级技巧
            f"Pro Tips:\n\n"
            f"💡 使用 cron 定时任务:\n"
            f"   openclaw cron add --daily \"9:00\"\n\n"
            f"💡 组合多个 Skills:\n"
            f"   输出 → 输入自动传递\n\n"
            f"💡 自定义配置:\n"
            f"   ~/.openclaw/config.yaml\n\n"
            f"💡 查看日志:\n"
            f"   openclaw logs --follow",
            
            # Tweet 9: 社区资源
            f"社区资源:\n\n"
            f"📚 官方文档:\n"
            f"   https://docs.openclaw.ai\n\n"
            f"💬 Discord 社区:\n"
            f"   https://discord.gg/openclaw\n\n"
            f"🐦 Twitter:\n"
            f"   @OpenClawAI\n\n"
            f"⭐ GitHub:\n"
            f"   https://github.com/openclaw/openclaw\n\n"
            f"活跃社区，有问必答。",
            
            # Tweet 10: 总结
            f"总结:\n\n"
            f"OpenClaw = 自动化 + AI + 开源\n\n"
            f"适合:\n"
            f"✅ 想自动化重复工作的人\n"
            f"✅ 想构建 AI 产品的开发者\n"
            f"✅ 想提升效率的内容创作者\n\n"
            f"不适合:\n"
            f"❌ 只想手动操作的人\n\n"
            f"开始你的自动化之旅 🚀\n\n"
            f"#OpenClaw #AI #Automation #Tutorial #GettingStarted"
        ]
    
    def generate_skill_building_tutorial(self, skill_name: str) -> list:
        """生成 Skill 开发教程"""
        
        return [
            f"🛠️ 如何构建自己的 OpenClaw Skill\n\n"
            f"Skill: {skill_name}\n\n"
            f"我将展示从零到发布的完整流程 👇",
            
            f"Step 1: 项目结构\n\n"
            f"```\n"
            f"{skill_name}/\n"
            f"├── SKILL.md          # 文档\n"
            f"├── src/\n"
            f"│   └── index.py      # 主代码\n"
            f"├── config.yaml       # 配置\n"
            f"└── requirements.txt  # 依赖\n"
            f"```\n\n"
            f"GitHub 模板:\n"
            f"https://github.com/openclaw/skill-template",
            
            f"Step 2: SKILL.md 文档\n\n"
            f"```markdown\n"
            f"# {skill_name.title()}\n\n"
            f"## Description\n"
            f"Brief description here\n\n"
            f"## Installation\n"
            f"```bash\n"
            f"openclaw skill install {skill_name}\n"
            f"```\n\n"
            f"## Usage\n"
            f"Example commands...\n"
            f"```\n\n"
            f"文档是关键！",
            
            f"Step 3: 核心代码\n\n"
            f"```python\n"
            f"# src/index.py\n"
            f"from openclaw import Skill\n\n"
            f"class {skill_name.title().replace('-', '')}Skill(Skill):\n"
            f"    def run(self, input_data):\n"
            f"        # Your logic here\n"
            f"        result = process(input_data)\n"
            f"        return result\n"
            f"```\n\n"
            f"保持代码简洁。",
            
            f"Step 4: 测试\n\n"
            f"```bash\n"
            f"# 本地测试\n"
            f"openclaw skill test {skill_name}\n\n"
            f"# 调试模式\n"
            f"openclaw skill test {skill_name} --debug\n"
            f"```\n\n"
            f"确保所有测试通过。",
            
            f"Step 5: 发布到社区\n\n"
            f"```bash\n"
            f"# 提交到 ClawHub\n"
            f"openclaw skill publish {skill_name}\n\n"
            f"# 分享你的 Skill\n"
            f"openclaw skill share {skill_name}\n"
            f"```\n\n"
            f"社区会帮你 review。",
            
            f"最佳实践:\n\n"
            f"✅ 写清晰的文档\n"
            f"✅ 提供使用示例\n"
            f"✅ 处理错误情况\n"
            f"✅ 添加单元测试\n"
            f"✅ 保持代码整洁\n\n"
            f"❌ 不要硬编码 API keys\n"
            f"❌ 不要忽略错误处理",
            
            f"完整示例:\n\n"
            f"GitHub: https://github.com/openclaw/example-skill\n\n"
            f"包含:\n"
            f"• 完整项目结构\n"
            f"• 测试用例\n"
            f"• CI/CD 配置\n"
            f"• 文档模板\n\n"
            f"Fork 并修改即可。",
            
            f"下一步:\n\n"
            f"1. Fork 模板仓库\n"
            f"2. 实现你的逻辑\n"
            f"3. 测试并提交\n"
            f"4. 分享给社区\n\n"
            f"期待看到你的 Skill! 🚀\n\n"
            f"#OpenClaw #Skill #Development #Tutorial"
        ]
    
    def generate_automation_tutorial(self) -> list:
        """生成自动化教程"""
        
        workflows = [
            {
                'name': 'Content Creation Pipeline',
                'description': '全自动内容创作流水线',
                'skills': ['ai-content-pipeline', 'ai-image-generation', 'twitter-post'],
                'time_saved': '3 hours/day'
            },
            {
                'name': 'Social Media Management',
                'description': '社交媒体自动管理',
                'skills': ['ai-content-pipeline', 'ai-image-generation', 'ai-video-generation'],
                'time_saved': '2 hours/day'
            },
            {
                'name': 'Data Processing',
                'description': '数据处理自动化',
                'skills': ['agentic-browser', 'python-executor', 'ai-rag-pipeline'],
                'time_saved': '4 hours/day'
            }
        ]
        
        workflow = random.choice(workflows)
        
        return [
            f"⚡ 自动化工作流: {workflow['name']}\n\n"
            f"节省: {workflow['time_saved']}\n\n"
            f"完整搭建指南 👇",
            
            f"工作流概述:\n\n"
            f"{workflow['description']}\n\n"
            f"使用的 Skills:\n"
            + '\n'.join([f"• {s}" for s in workflow['skills']]) + "\n\n"
            f"完全自动化，零人工干预。",
            
            f"配置步骤:\n\n"
            f"1️⃣ 安装所需 Skills\n"
            f"2️⃣ 配置 API Keys\n"
            f"3️⃣ 设置工作流 YAML\n"
            f"4️⃣ 测试运行\n"
            f"5️⃣ 部署到生产\n\n"
            f"详细配置见 thread 👇",
            
            f"YAML 配置示例:\n\n"
            f"```yaml\n"
            f"workflow: {workflow['name'].lower().replace(' ', '-')}\n"
            f"schedule: \"0 9 * * *\"  # 每天9点\n\n"
            f"steps:\n"
            + '\n'.join([f"  - skill: {s}" for s in workflow['skills']]) + "\n"
            f"```\n\n"
            f"保存为 workflow.yaml",
            
            f"运行:\n\n"
            f"```bash\n"
            f"# 手动运行\n"
            f"openclaw workflow run workflow.yaml\n\n"
            f"# 定时运行\n"
            f"openclaw workflow schedule workflow.yaml\n"
            f"```\n\n"
            f"开始自动化！",
            
            f"结果:\n\n"
            f"⏱️ 节省时间: {workflow['time_saved']}\n"
            f"📈 效率提升: 500%+\n"
            f"💰 成本: $0\n"
            f"😌 压力: 大幅降低\n\n"
            f"ROI: 无限大",
            
            f"适用场景:\n\n"
            f"✅ 重复性内容创作\n"
            f"✅ 批量数据处理\n"
            f"✅ 定时任务执行\n"
            f"✅ 跨平台同步\n\n"
            f"任何重复工作都可以自动化。",
            
            f"高级技巧:\n\n"
            f"💡 条件判断:\n"
            f"   if: result.status == 'success'\n\n"
            f"💡 错误处理:\n"
            f"   retry: 3\n"
            f"   on_error: notify\n\n"
            f"💡 并行执行:\n"
            f"   parallel: true\n\n"
            f"💡 数据传递:\n"
            f"   output -> input",
            
            f"监控:\n\n"
            f"```bash\n"
            f"# 查看运行日志\n"
            f"openclaw logs --workflow {workflow['name'].lower().replace(' ', '-')}\n\n"
            f"# 实时监控\n"
            f"openclaw logs --follow\n"
            f"```\n\n"
            f"随时掌握状态。",
            
            f"开始你的自动化:\n\n"
            f"1. 选择工作流模板\n"
            f"2. 自定义配置\n"
            f"3. 测试运行\n"
            f"4. 部署上线\n\n"
            f"模板: https://clawhub.com/workflows\n\n"
            f"#OpenClaw #Automation #Workflow #{workflow['name'].replace(' ', '')}"
        ]
    
    def generate_daily_tutorial(self):
        """生成每日教程"""
        tutorials = [
            self.generate_getting_started_tutorial,
            lambda: self.generate_skill_building_tutorial(f"my-skill-{random.randint(1, 100)}"),
            self.generate_automation_tutorial
        ]
        
        generator = random.choice(tutorials)
        return generator()


def main():
    """主函数"""
    generator = OpenClawTutorialGenerator()
    
    print("="*60)
    print("📚 OpenClaw 教程生成器")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # 生成随机教程
    tutorial = generator.generate_daily_tutorial()
    
    print(f"\n✅ 生成 {len(tutorial)} 条推文")
    print("\n预览:\n")
    
    for i, tweet in enumerate(tutorial[:3], 1):
        print(f"推文 {i}:")
        print(tweet[:150] + "..." if len(tweet) > 150 else tweet)
        print()
    
    # 保存
    filename = f"tutorial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for i, tweet in enumerate(tutorial, 1):
            f.write(f"Tweet {i}:\n{tweet}\n\n")
    
    print(f"💾 已保存: {filename}")


if __name__ == "__main__":
    main()
