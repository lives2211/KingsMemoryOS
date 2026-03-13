#!/usr/bin/env python3
"""
小红书自动发布主程序
- 检查调度计划
- 生成内容
- 渲染图片
- 发布到小红书
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

from scheduler import PostingScheduler, ACCOUNTS
from content_generator import ContentGenerator

class AutoPoster:
    def __init__(self):
        self.scheduler = PostingScheduler()
        self.generator = ContentGenerator()
        self.base_path = Path("/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix")
        
    def check_and_post(self):
        """检查并执行发布任务"""
        next_post = self.scheduler.get_next_post()
        
        if not next_post:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 暂无待发布任务")
            return False
        
        account = next_post["account"]
        account_name = next_post["account_name"]
        post_time = next_post["time"]
        
        print(f"\n🦞 执行发布任务")
        print(f"账号: {account_name} ({account})")
        print(f"计划时间: {post_time}")
        
        # 1. 生成内容（带人工化处理）
        print("\n1️⃣ 生成内容...")
        result = self.generator.generate_post(account, humanize=True)
        
        if not result["rendered"]:
            print("❌ 图片渲染失败，跳过本次发布")
            return False
        
        print(f"✅ 标题: {result['title'][:40]}...")
        
        # 2. 获取生成的图片
        md_file = Path(result["markdown_file"])
        output_dir = md_file.parent
        
        # 查找生成的图片
        images = sorted(output_dir.glob("*.png"))
        if not images:
            print("❌ 未找到生成的图片")
            return False
        
        print(f"✅ 生成图片: {len(images)} 张")
        for img in images:
            print(f"   - {img.name}")
        
        # 3. 发布到小红书（需要配置Cookie）
        print("\n3️⃣ 发布到小红书...")
        
        # 3. 发布到小红书
        print("\n3️⃣ 发布到小红书...")
        
        # 使用 xhs CLI 工具发布
        import subprocess
        
        # 检查并限制内容长度
        title = result["title"]
        content = result["content"]
        
        # 小红书限制：标题 + 正文 + 其他数据 < 260096 bytes
        # 预留 10000 bytes 给其他字段，图片单独上传
        MAX_TOTAL_LENGTH = 250000
        
        title_bytes = title.encode('utf-8')
        content_bytes = content.encode('utf-8')
        total_bytes = len(title_bytes) + len(content_bytes)
        
        print(f"   标题长度: {len(title)} 字符 ({len(title_bytes)} bytes)")
        print(f"   正文长度: {len(content)} 字符 ({len(content_bytes)} bytes)")
        print(f"   总长度: {total_bytes} bytes")
        
        # 如果超长，截断正文
        if total_bytes > MAX_TOTAL_LENGTH:
            print(f"   ⚠️ 内容超长，截断正文...")
            # 保留标题，截断正文
            max_content_bytes = MAX_TOTAL_LENGTH - len(title_bytes) - 100  # 留100字节余量
            content = content_bytes[:max_content_bytes].decode('utf-8', errors='ignore')
            print(f"   截断后正文: {len(content)} 字符 ({len(content.encode('utf-8'))} bytes)")
        
        # 准备图片路径（逗号分隔）
        images_str = ",".join([str(img) for img in images])
        
        # 构建发布命令
        cmd = [
            "xhs", "post",
            "--title", title,
            "--body", content,
            "--images", images_str
        ]
        
        try:
            # 执行发布命令
            publish_result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=120
            )
            
            if publish_result.returncode == 0:
                print("✅ 发布成功！")
                print(f"   输出: {publish_result.stdout[:200]}...")
            else:
                print(f"❌ 发布失败: {publish_result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 发布超时")
            return False
        except Exception as e:
            print(f"❌ 发布异常: {e}")
            return False
        
        # 4. 标记为已发布
        self.scheduler.mark_posted(post_time, account)
        
        return True
    
    def run_daemon(self, interval=300):
        """守护进程模式运行"""
        print("🦞 小红书自动发布系统启动")
        print(f"检查间隔: {interval}秒")
        print("按 Ctrl+C 停止\n")
        
        try:
            while True:
                self.check_and_post()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n👋 系统已停止")

def init_account_config():
    """初始化账号配置文件模板"""
    base_path = Path("/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix")
    
    for account_id in ACCOUNTS.keys():
        env_file = base_path / f".env.{account_id}"
        if not env_file.exists():
            with open(env_file, 'w') as f:
                f.write(f"# 账号: {ACCOUNTS[account_id]['name']}\n")
                f.write("# 获取方式: 浏览器登录小红书 → F12 → Network → 任意请求的 Cookie\n")
                f.write("XHS_COOKIE=\n")
            print(f"✅ 创建配置模板: {env_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书自动发布系统")
    parser.add_argument("--init", action="store_true", help="初始化账号配置")
    parser.add_argument("--daemon", action="store_true", help="守护进程模式")
    parser.add_argument("--once", action="store_true", help="执行一次")
    parser.add_argument("--interval", type=int, default=300, help="检查间隔(秒)")
    
    args = parser.parse_args()
    
    if args.init:
        init_account_config()
    elif args.daemon:
        poster = AutoPoster()
        poster.run_daemon(args.interval)
    elif args.once:
        poster = AutoPoster()
        poster.check_and_post()
    else:
        # 默认显示今日计划
        scheduler = PostingScheduler()
        schedule = scheduler.get_today_schedule()
        
        print("🦞 今日发布计划:\n")
        for post in schedule:
            time_str = datetime.fromisoformat(post["time"]).strftime("%H:%M")
            status = "✅" if post["status"] == "posted" else "⏳"
            print(f"{status} [{time_str}] {post['account_name']}")
