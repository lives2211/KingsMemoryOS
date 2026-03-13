"""
基于 xiaohongshu-cli 的 API 发布器
使用逆向工程API，更稳定、更安全
"""

import subprocess
import json
from typing import List, Optional, Dict
from dataclasses import dataclass
from loguru import logger


@dataclass
class APIPublishConfig:
    """API发布配置"""
    title: str
    content: str
    images: List[str]
    hashtags: Optional[List[str]] = None


class XHSAPIPublisher:
    """
    基于 xiaohongshu-cli 的API发布器
    
    优势：
    - 使用逆向工程API，不依赖浏览器
    - xsec_token + xsec_source 成对缓存
    - 更像真实浏览器请求链
    - Anti-detection: Chrome指纹、sec-ch-ua对齐、高斯抖动
    """
    
    def __init__(self):
        self.cli = "xhs"
        self._check_cli()
    
    def _check_cli(self):
        """检查CLI是否安装"""
        try:
            result = subprocess.run(
                [self.cli, "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logger.info(f"xiaohongshu-cli 已安装: {result.stdout.strip()}")
            else:
                logger.warning("xiaohongshu-cli 可能未正确安装")
        except FileNotFoundError:
            raise RuntimeError(
                "xiaohongshu-cli 未安装，请运行: pip install xiaohongshu-cli"
            )
    
    def _run_cmd(self, args: List[str], capture: bool = True) -> tuple:
        """运行CLI命令"""
        cmd = [self.cli] + args
        logger.debug(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True
        )
        
        return result.returncode, result.stdout, result.stderr
    
    def check_auth(self) -> bool:
        """检查登录状态"""
        code, stdout, stderr = self._run_cmd(["whoami"])
        
        if code == 0 and "nickname" in stdout.lower():
            logger.info("已登录")
            return True
        
        logger.warning("未登录或登录已过期")
        return False
    
    def login(self) -> bool:
        """
        扫码登录
        使用 browser-cookie3 自动提取浏览器Cookie
        """
        logger.info("启动登录流程...")
        
        # 尝试自动提取浏览器Cookie
        code, stdout, stderr = self._run_cmd(["auth", "--auto"])
        
        if code == 0:
            logger.info("自动登录成功")
            return True
        
        # 如果自动失败，提示手动扫码
        logger.info("自动登录失败，请手动扫码...")
        code, stdout, stderr = self._run_cmd(["auth"])
        
        return code == 0
    
    def search_notes(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索笔记
        支持 xsec_token + xsec_source 缓存
        """
        logger.info(f"搜索关键词: {keyword}")
        
        code, stdout, stderr = self._run_cmd([
            "search", keyword,
            "--limit", str(limit),
            "--yaml"
        ])
        
        if code != 0:
            logger.error(f"搜索失败: {stderr}")
            return []
        
        # 解析YAML输出
        try:
            import yaml
            data = yaml.safe_load(stdout)
            return data.get("data", {}).get("items", [])
        except Exception as e:
            logger.error(f"解析搜索结果失败: {e}")
            return []
    
    def read_note(self, index: int = 1) -> Optional[Dict]:
        """
        读取笔记详情
        使用短索引: xhs read 1
        """
        code, stdout, stderr = self._run_cmd([
            "read", str(index),
            "--yaml"
        ])
        
        if code != 0:
            logger.error(f"读取笔记失败: {stderr}")
            return None
        
        try:
            import yaml
            data = yaml.safe_load(stdout)
            return data.get("data", {})
        except Exception as e:
            logger.error(f"解析笔记失败: {e}")
            return None
    
    def get_comments(self, index: int = 1) -> List[Dict]:
        """
        获取评论
        支持 xsec_token 复用
        """
        code, stdout, stderr = self._run_cmd([
            "comments", str(index),
            "--yaml"
        ])
        
        if code != 0:
            logger.error(f"获取评论失败: {stderr}")
            return []
        
        try:
            import yaml
            data = yaml.safe_load(stdout)
            return data.get("data", {}).get("comments", [])
        except Exception as e:
            logger.error(f"解析评论失败: {e}")
            return []
    
    def like_note(self, index: int = 1) -> bool:
        """点赞笔记"""
        code, stdout, stderr = self._run_cmd(["like", str(index)])
        
        if code == 0:
            logger.info(f"点赞成功: {index}")
            return True
        
        logger.error(f"点赞失败: {stderr}")
        return False
    
    def favorite_note(self, index: int = 1) -> bool:
        """收藏笔记"""
        code, stdout, stderr = self._run_cmd(["favorite", str(index)])
        
        if code == 0:
            logger.info(f"收藏成功: {index}")
            return True
        
        logger.error(f"收藏失败: {stderr}")
        return False
    
    def comment_on_note(self, index: int = 1, content: str = "") -> bool:
        """评论笔记"""
        code, stdout, stderr = self._run_cmd([
            "comment", str(index),
            "-c", content
        ])
        
        if code == 0:
            logger.info(f"评论成功: {index}")
            return True
        
        logger.error(f"评论失败: {stderr}")
        return False
    
    def get_feed(self, limit: int = 10) -> List[Dict]:
        """获取推荐流"""
        code, stdout, stderr = self._run_cmd([
            "feed",
            "--limit", str(limit),
            "--yaml"
        ])
        
        if code != 0:
            logger.error(f"获取推荐流失败: {stderr}")
            return []
        
        try:
            import yaml
            data = yaml.safe_load(stdout)
            return data.get("data", {}).get("items", [])
        except Exception as e:
            logger.error(f"解析推荐流失败: {e}")
            return []
    
    def get_hot(self, category: str = "food", limit: int = 10) -> List[Dict]:
        """
        获取热门笔记
        
        Categories: fashion, food, cosmetics, movie, career, love, home, gaming, travel, fitness
        """
        code, stdout, stderr = self._run_cmd([
            "hot",
            "-c", category,
            "--limit", str(limit),
            "--yaml"
        ])
        
        if code != 0:
            logger.error(f"获取热门失败: {stderr}")
            return []
        
        try:
            import yaml
            data = yaml.safe_load(stdout)
            return data.get("data", {}).get("items", [])
        except Exception as e:
            logger.error(f"解析热门失败: {e}")
            return []
    
    def get_my_notes(self, limit: int = 20) -> List[Dict]:
        """获取我的笔记"""
        code, stdout, stderr = self._run_cmd([
            "my-notes",
            "--limit", str(limit),
            "--yaml"
        ])
        
        if code != 0:
            logger.error(f"获取我的笔记失败: {stderr}")
            return []
        
        try:
            import yaml
            data = yaml.safe_load(stdout)
            return data.get("data", {}).get("notes", [])
        except Exception as e:
            logger.error(f"解析我的笔记失败: {e}")
            return []


def main():
    """测试代码"""
    publisher = XHSAPIPublisher()
    
    # 检查登录
    if not publisher.check_auth():
        print("未登录，请先运行: xhs auth")
        return
    
    # 获取推荐流
    print("\n获取推荐流...")
    feed = publisher.get_feed(limit=5)
    for i, item in enumerate(feed, 1):
        print(f"{i}. {item.get('title', '无标题')}")
    
    # 搜索
    print("\n搜索 'AI工具'...")
    results = publisher.search_notes("AI工具", limit=3)
    for i, item in enumerate(results, 1):
        print(f"{i}. {item.get('title', '无标题')}")


if __name__ == "__main__":
    main()