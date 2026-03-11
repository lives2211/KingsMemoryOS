#!/usr/bin/env python3
"""
系统验证脚本
- 检查所有组件
- 验证配置
- 测试功能
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

class SystemVerifier:
    """系统验证器"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        self.base_path = Path(base_path)
        self.results = []
        self.warnings = []
        self.errors = []
        
    def check_directory(self, name, required=True):
        """检查目录"""
        path = self.base_path / name
        exists = path.exists() and path.is_dir()
        
        if exists:
            self.results.append(("✅", name, "目录存在"))
        elif required:
            self.errors.append(f"❌ 缺少必要目录: {name}")
        else:
            self.warnings.append(f"⚠️  缺少可选目录: {name}")
        
        return exists
    
    def check_file(self, name, required=True):
        """检查文件"""
        path = self.base_path / name
        exists = path.exists() and path.is_file()
        
        if exists:
            self.results.append(("✅", name, "文件存在"))
        elif required:
            self.errors.append(f"❌ 缺少必要文件: {name}")
        else:
            self.warnings.append(f"⚠️  缺少可选文件: {name}")
        
        return exists
    
    def check_python_module(self, module_name):
        """检查Python模块"""
        try:
            __import__(module_name)
            self.results.append(("✅", module_name, "Python模块已安装"))
            return True
        except ImportError:
            self.errors.append(f"❌ 缺少Python模块: {module_name}")
            return False
    
    def check_account_config(self):
        """检查账号配置"""
        accounts = ["tech-geek", "life-aesthetics", "career-growth", "foodie", "fashion"]
        configured = 0
        
        for account in accounts:
            env_file = self.base_path / f".env.{account}"
            if env_file.exists():
                content = env_file.read_text()
                if "XHS_COOKIE=" in content and len(content) > 50:
                    configured += 1
                    self.results.append(("✅", f"{account}", "已配置Cookie"))
                else:
                    self.warnings.append(f"⚠️  {account}: Cookie未配置")
            else:
                self.warnings.append(f"⚠️  {account}: 配置文件不存在")
        
        return configured
    
    def verify(self):
        """执行验证"""
        print("=" * 60)
        print("🦞 小红书矩阵运营系统 - 验证报告")
        print("=" * 60)
        print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 检查核心目录
        print("📁 核心目录检查")
        print("-" * 60)
        self.check_directory("content-gen", required=True)
        self.check_directory("ops-skill", required=True)
        self.check_directory("union-search", required=False)
        self.check_directory("aitu", required=False)
        self.check_directory("personas", required=True)
        self.check_directory("generated", required=True)
        self.check_directory("logs", required=True)
        self.check_directory("research", required=False)
        
        for status, name, msg in self.results[-7:]:
            print(f"{status} {name}: {msg}")
        print()
        
        # 检查核心文件
        print("📄 核心文件检查")
        print("-" * 60)
        self.check_file("scheduler.py", required=True)
        self.check_file("content_generator.py", required=True)
        self.check_file("auto_post.py", required=True)
        self.check_file("start.sh", required=True)
        self.check_file("analytics.py", required=False)
        self.check_file("setup_cron.py", required=False)
        
        for status, name, msg in self.results[-6:]:
            print(f"{status} {name}: {msg}")
        print()
        
        # 检查Python依赖
        print("🐍 Python依赖检查")
        print("-" * 60)
        modules = ["playwright", "markdown", "yaml", "requests", "lxml"]
        for module in modules:
            self.check_python_module(module)
        
        for status, name, msg in self.results[-6:]:
            print(f"{status} {name}: {msg}")
        print()
        
        # 检查账号配置
        print("👤 账号配置检查")
        print("-" * 60)
        configured = self.check_account_config()
        print(f"已配置: {configured}/5 个账号")
        print()
        
        # 检查Playwright
        print("🎭 Playwright检查")
        print("-" * 60)
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch()
                browser.close()
            self.results.append(("✅", "Playwright", "浏览器可正常启动"))
            print("✅ Playwright: 浏览器可正常启动")
        except Exception as e:
            self.warnings.append(f"⚠️  Playwright: {str(e)[:50]}")
            print(f"⚠️  Playwright: 需要安装浏览器")
            print("   运行: python3 -m playwright install chromium")
        print()
        
        # 显示警告
        if self.warnings:
            print("⚠️  警告")
            print("-" * 60)
            for warning in self.warnings:
                print(f"  {warning}")
            print()
        
        # 显示错误
        if self.errors:
            print("❌ 错误")
            print("-" * 60)
            for error in self.errors:
                print(f"  {error}")
            print()
        
        # 总结
        print("=" * 60)
        print("验证总结")
        print("=" * 60)
        
        total_checks = len(self.results)
        total_warnings = len(self.warnings)
        total_errors = len(self.errors)
        
        print(f"通过: {total_checks} 项")
        print(f"警告: {total_warnings} 项")
        print(f"错误: {total_errors} 项")
        print()
        
        if total_errors == 0:
            if total_warnings == 0:
                print("✅ 系统验证通过！所有组件就绪。")
            else:
                print("⚠️  系统基本可用，但有一些警告需要处理。")
        else:
            print("❌ 系统验证失败，请先修复错误。")
        
        print()
        print("=" * 60)
        
        return total_errors == 0
    
    def print_next_steps(self):
        """打印下一步操作"""
        print("\n🚀 下一步操作")
        print("=" * 60)
        print()
        print("1. 配置账号Cookie:")
        print("   - 编辑 .env.* 文件")
        print("   - 填入小红书Cookie")
        print()
        print("2. 生成发布计划:")
        print("   ./start.sh schedule")
        print()
        print("3. 测试内容生成:")
        print("   ./start.sh test")
        print()
        print("4. 查看数据报告:")
        print("   ./start.sh report")
        print()
        print("5. 启动自动运营:")
        print("   ./start.sh daemon")
        print()
        print("6. 设置定时任务:")
        print("   ./start.sh cron")
        print("   crontab cron.txt")
        print()
        print("=" * 60)

def main():
    """主函数"""
    verifier = SystemVerifier()
    success = verifier.verify()
    verifier.print_next_steps()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
