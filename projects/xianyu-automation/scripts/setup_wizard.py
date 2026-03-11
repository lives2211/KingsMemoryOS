#!/usr/bin/env python3
"""
闲鱼自动化 - 新手设置向导
一步步引导配置
"""

import json
import os
from pathlib import Path
from datetime import datetime

class SetupWizard:
    def __init__(self):
        self.base_dir = Path("/home/fengxueda/.openclaw/workspace/projects/xianyu-automation")
        self.config = {}
        self.items = []
        
    def welcome(self):
        print("""
╔════════════════════════════════════════╗
║     🦞 闲鱼自动化运营 - 新手向导       ║
╚════════════════════════════════════════╝

我会一步步帮你完成设置，大约需要 5-10 分钟。

请选择你的操作：
1. 全新设置（推荐新手）
2. 修改现有配置
3. 查看当前状态
4. 退出
        """)
        return input("请输入选项 [1-4]: ").strip()
    
    def step1_account_info(self):
        """步骤1：账号信息"""
        print("\n📱 步骤 1/5: 账号信息")
        print("-" * 40)
        
        print("\n你的闲鱼账号状态？")
        print("1. 已有账号，发布过商品")
        print("2. 已有账号，未发布过商品")
        print("3. 还没有账号")
        
        choice = input("请选择 [1-3]: ").strip()
        
        if choice == "3":
            print("\n⚠️ 请先下载闲鱼APP注册账号")
            print("注册完成后回来继续设置")
            return False
        
        self.config["account_status"] = choice
        self.config["account_created"] = choice == "1"
        
        # 询问商品数量
        print("\n你大概要卖多少件商品？")
        print("1. 1-5件（个人闲置）")
        print("2. 6-20件（小规模）")
        print("3. 20件以上（专业卖家）")
        
        item_count = input("请选择 [1-3]: ").strip()
        self.config["item_count_level"] = item_count
        
        return True
    
    def step2_product_category(self):
        """步骤2：商品类别"""
        print("\n📦 步骤 2/5: 商品类别")
        print("-" * 40)
        
        categories = {
            "1": "数码产品（手机、电脑、耳机等）",
            "2": "服装鞋包",
            "3": "家居用品",
            "4": "图书文具",
            "5": "美妆护肤",
            "6": "运动户外",
            "7": "其他"
        }
        
        print("你要卖什么类型的商品？（可多选，用逗号分隔）")
        for k, v in categories.items():
            print(f"{k}. {v}")
        
        selected = input("\n请选择 [1-7，多选用逗号分隔，如1,3]: ").strip()
        selected_cats = [categories.get(c.strip(), "其他") for c in selected.split(",") if c.strip()]
        
        self.config["categories"] = selected_cats
        print(f"\n✅ 已选择: {', '.join(selected_cats)}")
        
        return True
    
    def step3_operation_settings(self):
        """步骤3：运营设置"""
        print("\n⚙️ 步骤 3/5: 运营设置")
        print("-" * 40)
        
        # 擦亮时间设置
        print("\n你希望什么时候自动擦亮商品？")
        print("1. 早上 7:00-9:00（推荐，流量高峰）")
        print("2. 中午 12:00-13:00")
        print("3. 晚上 19:00-21:00（推荐，流量高峰）")
        print("4. 自定义时间")
        
        polish_time = input("请选择 [1-4]: ").strip()
        
        time_map = {
            "1": "07:00",
            "2": "12:00",
            "3": "19:00",
            "4": input("请输入时间（如08:30）: ").strip() or "08:00"
        }
        
        self.config["polish_time"] = time_map.get(polish_time, "08:00")
        
        # 每日擦亮数量
        print("\n每天最多擦亮多少个商品？")
        print("1. 10个（保守）")
        print("2. 30个（推荐）")
        print("3. 50个（闲鱼上限）")
        
        max_items = input("请选择 [1-3]: ").strip()
        self.config["max_polish_per_day"] = {"1": 10, "2": 30, "3": 50}.get(max_items, 30)
        
        # 是否开启价格调整建议
        print("\n是否开启智能调价建议？")
        print("当商品浏览高但想要少时，系统会建议降价")
        print("1. 开启（推荐）")
        print("2. 关闭")
        
        auto_price = input("请选择 [1-2]: ").strip()
        self.config["auto_price_suggest"] = auto_price == "1"
        
        return True
    
    def step4_generate_items(self):
        """步骤4：生成商品数据"""
        print("\n📝 步骤 4/5: 生成商品数据")
        print("-" * 40)
        
        print("\n现在我来帮你创建商品数据模板")
        print("你需要提供以下信息（可以跳过，稍后手动编辑）:\n")
        
        items = []
        
        # 根据选择的类别生成模板
        for i, cat in enumerate(self.config.get("categories", ["数码产品"]), 1):
            print(f"\n--- 商品 {i} ---")
            
            item = {
                "id": f"item_{i:03d}",
                "category": cat,
                "status": "draft"  # draft, active, sold
            }
            
            # 询问基本信息
            item["title"] = input(f"商品标题（或直接回车跳过）: ").strip()
            if not item["title"]:
                item["title"] = f"【待填写】{cat}商品"
            
            price_input = input("期望价格（元）: ").strip()
            item["price"] = int(price_input) if price_input.isdigit() else 0
            
            condition = input("成色（1.全新 2.99新 3.95新 4.9成新）: ").strip()
            condition_map = {"1": "全新", "2": "99新", "3": "95新", "4": "9成新"}
            item["condition"] = condition_map.get(condition, "95新")
            
            item["reason"] = input("出售原因（如：升级换代/搬家/闲置）: ").strip() or "闲置转让"
            
            items.append(item)
            
            if i >= 3:  # 最多先创建3个示例
                print(f"\n已创建 {i} 个商品模板，更多商品可以稍后手动添加")
                break
        
        self.items = items
        
        # 保存到文件
        items_file = self.base_dir / "data" / "my_items.json"
        with open(items_file, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 商品数据已保存到: {items_file}")
        
        return True
    
    def step5_cron_setup(self):
        """步骤5：设置定时任务"""
        print("\n⏰ 步骤 5/5: 设置定时任务")
        print("-" * 40)
        
        print("\n我将为你设置自动运行的定时任务：")
        print(f"• 每天 {self.config.get('polish_time', '08:00')} 自动擦亮商品")
        print("• 每周日晚上生成数据报告")
        
        confirm = input("\n是否设置？ [y/n]: ").strip().lower()
        
        if confirm == 'y':
            self._create_cron_jobs()
            print("\n✅ 定时任务已设置")
        else:
            print("\n⏸️ 已跳过定时任务设置")
            print("你可以稍后手动运行: ./run.sh")
        
        return True
    
    def _create_cron_jobs(self):
        """创建Cron任务"""
        polish_time = self.config.get("polish_time", "08:00")
        hour, minute = polish_time.split(":")
        
        # 构建cron表达式
        cron_polish = f"{minute} {hour} * * * cd {self.base_dir} && python3 scripts/xianyu_manage.py --items data/my_items.json >> logs/cron.log 2>&1"
        cron_report = f"0 21 * * 0 cd {self.base_dir} && python3 scripts/xianyu_metrics.py --items data/my_items.json --full-report >> logs/cron.log 2>&1"
        
        # 保存cron配置
        cron_file = self.base_dir / "config" / "cron.txt"
        with open(cron_file, 'w') as f:
            f.write(f"# 闲鱼自动化定时任务\n")
            f.write(f"# 每天自动擦亮\n")
            f.write(f"{cron_polish}\n")
            f.write(f"# 每周日晚上生成报告\n")
            f.write(f"{cron_report}\n")
        
        print(f"\n📄 Cron配置已保存到: {cron_file}")
        print("\n要启用定时任务，请运行以下命令：")
        print(f"  crontab {cron_file}")
        
        # 尝试自动设置
        try:
            os.system(f"crontab {cron_file}")
            print("\n✅ 已自动添加到系统定时任务")
        except:
            print("\n⚠️ 自动设置失败，请手动运行上述命令")
    
    def save_config(self):
        """保存配置"""
        config_file = self.base_dir / "config" / "user_config.json"
        
        full_config = {
            "created_at": datetime.now().isoformat(),
            "setup_complete": True,
            **self.config
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(full_config, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 配置已保存到: {config_file}")
    
    def show_summary(self):
        """显示配置摘要"""
        print("\n" + "=" * 50)
        print("📋 配置摘要")
        print("=" * 50)
        
        print(f"\n账号状态: {'已发布过商品' if self.config.get('account_created') else '新账号'}")
        print(f"商品类别: {', '.join(self.config.get('categories', []))}")
        print(f"自动擦亮时间: 每天 {self.config.get('polish_time', '08:00')}")
        print(f"每日擦亮上限: {self.config.get('max_polish_per_day', 30)} 个")
        print(f"智能调价建议: {'开启' if self.config.get('auto_price_suggest') else '关闭'}")
        print(f"商品数量: {len(self.items)} 个（可继续添加）")
        
        print("\n" + "=" * 50)
        print("🎉 设置完成！")
        print("=" * 50)
        
        print("\n下一步操作：")
        print("1. 编辑商品数据: nano data/my_items.json")
        print("2. 测试运行: ./run.sh")
        print("3. 查看帮助: cat README.md")
        
        print("\n💡 提示：首次运行建议先用 --dry-run 模式测试")
    
    def run(self):
        """运行向导"""
        choice = self.welcome()
        
        if choice == "4":
            print("👋 再见！")
            return
        
        if choice == "3":
            self.show_status()
            return
        
        # 执行设置步骤
        steps = [
            self.step1_account_info,
            self.step2_product_category,
            self.step3_operation_settings,
            self.step4_generate_items,
            self.step5_cron_setup
        ]
        
        for step in steps:
            if not step():
                print("\n❌ 设置中断，请完成后重新运行")
                return
        
        # 保存配置
        self.save_config()
        
        # 显示摘要
        self.show_summary()
    
    def show_status(self):
        """显示当前状态"""
        print("\n📊 当前状态")
        print("-" * 40)
        
        # 检查配置文件
        config_file = self.base_dir / "config" / "user_config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            print(f"✅ 配置已创建: {config.get('created_at', '未知')}")
            print(f"   擦亮时间: {config.get('polish_time', '未设置')}")
        else:
            print("❌ 尚未完成初始设置")
        
        # 检查商品数据
        items_file = self.base_dir / "data" / "my_items.json"
        if items_file.exists():
            with open(items_file, 'r') as f:
                items = json.load(f)
            print(f"✅ 商品数据: {len(items)} 个商品")
        else:
            print("❌ 暂无商品数据")
        
        # 检查定时任务
        cron_file = self.base_dir / "config" / "cron.txt"
        if cron_file.exists():
            print(f"✅ 定时任务配置已创建")
        else:
            print("❌ 定时任务未设置")


if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.run()
