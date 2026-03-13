"""
小红书卡片生成器
整合 Auto-Redbook-Skills 的图片渲染功能
"""

import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
from loguru import logger


@dataclass
class CardConfig:
    """卡片配置"""
    theme: str = "playful-geometric"  # 主题
    mode: str = "auto-split"  # 分页模式
    width: int = 1080
    height: int = 1440
    dpr: int = 2


class CardGenerator:
    """卡片生成器"""
    
    # 可用主题
    THEMES = [
        "default",
        "playful-geometric",
        "neo-brutalism",
        "botanical",
        "professional",
        "retro",
        "terminal",
        "sketch"
    ]
    
    # 分页模式
    MODES = ["separator", "auto-fit", "auto-split", "dynamic"]
    
    def __init__(self, renderer_path: str = "./card-renderer"):
        self.renderer_path = Path(renderer_path).resolve()
        self.script_path = self.renderer_path / "scripts" / "render_xhs.py"
        
        if not self.script_path.exists():
            raise FileNotFoundError(f"渲染脚本不存在: {self.script_path}")
    
    def generate_from_markdown(
        self,
        markdown_file: str,
        output_dir: str,
        config: Optional[CardConfig] = None
    ) -> List[str]:
        """
        从Markdown文件生成卡片
        
        Args:
            markdown_file: Markdown文件路径
            output_dir: 输出目录
            config: 卡片配置
            
        Returns:
            生成的图片路径列表
        """
        if config is None:
            config = CardConfig()
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成卡片: {markdown_file}")
        logger.info(f"主题: {config.theme}, 模式: {config.mode}")
        
        # 构建命令
        cmd = [
            "python3",
            str(self.script_path),
            markdown_file,
            "-t", config.theme,
            "-m", config.mode,
            "--width", str(config.width),
            "--height", str(config.height),
            "--dpr", str(config.dpr)
        ]
        
        try:
            # 执行渲染
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.renderer_path)
            )
            
            if result.returncode != 0:
                logger.error(f"渲染失败: {result.stderr}")
                raise RuntimeError(f"卡片渲染失败: {result.stderr}")
            
            # 查找生成的图片
            cards = self._find_generated_cards(self.renderer_path)
            
            # 移动到输出目录
            moved_cards = []
            for card in cards:
                dest = output_path / card.name
                card.rename(dest)
                moved_cards.append(str(dest))
            
            logger.info(f"生成 {len(moved_cards)} 张卡片")
            return moved_cards
            
        except Exception as e:
            logger.error(f"生成卡片失败: {e}")
            raise
    
    def generate_from_content(
        self,
        title: str,
        content: str,
        output_dir: str,
        config: Optional[CardConfig] = None
    ) -> List[str]:
        """
        从内容字符串生成卡片
        
        Args:
            title: 标题
            content: 正文内容
            output_dir: 输出目录
            config: 卡片配置
            
        Returns:
            生成的图片路径列表
        """
        # 创建临时Markdown文件
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            delete=False,
            encoding='utf-8'
        ) as f:
            # 写入封面内容
            f.write(f"# {title}\n\n")
            f.write(content)
            temp_path = f.name
        
        try:
            return self.generate_from_markdown(temp_path, output_dir, config)
        finally:
            # 清理临时文件
            Path(temp_path).unlink(missing_ok=True)
    
    def _find_generated_cards(self, search_path: Path) -> List[Path]:
        """查找生成的卡片图片"""
        cards = []
        
        # 查找 cover.png 和 card_*.png
        for pattern in ["cover.png", "card_*.png"]:
            cards.extend(search_path.glob(pattern))
        
        # 按文件名排序
        cards.sort(key=lambda x: x.name)
        
        return cards
    
    @staticmethod
    def get_available_themes() -> List[str]:
        """获取可用主题列表"""
        return CardGenerator.THEMES
    
    @staticmethod
    def get_available_modes() -> List[str]:
        """获取可用分页模式"""
        return CardGenerator.MODES


def main():
    """测试代码"""
    generator = CardGenerator()
    
    # 测试生成
    cards = generator.generate_from_content(
        title="测试标题",
        content="这是测试内容\n\n---\n\n第二页内容",
        output_dir="./output",
        config=CardConfig(theme="retro", mode="auto-split")
    )
    
    print(f"生成卡片: {cards}")


if __name__ == "__main__":
    main()
