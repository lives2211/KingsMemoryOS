"""
内容加载器
从内容农场读取小红书笔记
"""

import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from loguru import logger


@dataclass
class XHSNote:
    """小红书笔记数据结构"""
    title: str
    content: str
    hashtags: List[str]
    source_file: str
    created_date: str
    
    @property
    def full_content(self) -> str:
        """获取完整内容（含标签）"""
        tag_line = " ".join([f"#{tag}" for tag in self.hashtags])
        return f"{self.content}\n\n{tag_line}"


class ContentLoader:
    """内容加载器"""
    
    def __init__(self, content_dir: str = "../xiaohongshu"):
        self.content_dir = Path(content_dir)
        
    def load_notes_by_date(
        self,
        date: Optional[str] = None,
        limit: int = 10
    ) -> List[XHSNote]:
        """
        加载指定日期的笔记
        
        Args:
            date: 日期字符串 (YYYY-MM-DD)，默认为今天
            limit: 最大加载数量
            
        Returns:
            笔记列表
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        date_dir = self.content_dir / date
        if not date_dir.exists():
            logger.warning(f"日期目录不存在: {date_dir}")
            return []
        
        notes = []
        md_files = sorted(date_dir.glob("*.md"))
        
        for md_file in md_files[:limit]:
            try:
                note = self._parse_note_file(md_file)
                if note:
                    notes.append(note)
            except Exception as e:
                logger.error(f"解析文件失败 {md_file}: {e}")
        
        logger.info(f"加载 {len(notes)} 篇笔记")
        return notes
    
    def load_all_pending_notes(self, limit: int = 20) -> List[XHSNote]:
        """
        加载所有待发布的笔记（按日期倒序）
        
        Args:
            limit: 最大加载数量
            
        Returns:
            笔记列表
        """
        notes = []
        
        # 获取所有日期目录
        date_dirs = sorted(
            [d for d in self.content_dir.iterdir() if d.is_dir()],
            reverse=True
        )
        
        for date_dir in date_dirs:
            md_files = sorted(date_dir.glob("*.md"))
            
            for md_file in md_files:
                if len(notes) >= limit:
                    break
                
                try:
                    note = self._parse_note_file(md_file)
                    if note:
                        notes.append(note)
                except Exception as e:
                    logger.error(f"解析文件失败 {md_file}: {e}")
            
            if len(notes) >= limit:
                break
        
        logger.info(f"加载 {len(notes)} 篇待发布笔记")
        return notes
    
    def _parse_note_file(self, file_path: Path) -> Optional[XHSNote]:
        """
        解析笔记文件
        
        支持的格式:
        - 标题行（第一个#开头）
        - 正文内容
        - 标签行（最后一行#开头的标签）
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
        if not title_match:
            logger.warning(f"未找到标题: {file_path}")
            return None
        
        title = title_match.group(1).strip()
        
        # 提取标签（最后一行#开头的标签）
        lines = content.split('\n')
        hashtags = []
        
        for line in reversed(lines):
            line = line.strip()
            if line.startswith('#'):
                # 提取所有标签
                tags = re.findall(r'#(\S+)', line)
                hashtags.extend(tags)
                break
        
        # 提取正文（去掉标题和标签行）
        content_lines = []
        in_content = False
        
        for line in lines:
            # 跳过标题
            if line.startswith('# ') and not in_content:
                in_content = True
                continue
            
            # 跳过标签行
            if line.strip().startswith('#') and all(c.startswith('#') or c.isspace() for c in line.split()):
                continue
            
            if in_content:
                content_lines.append(line)
        
        body = '\n'.join(content_lines).strip()
        
        # 提取日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', str(file_path))
        created_date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")
        
        return XHSNote(
            title=title,
            content=body,
            hashtags=hashtags,
            source_file=str(file_path),
            created_date=created_date
        )
    
    def get_notes_count_by_date(self, date: Optional[str] = None) -> int:
        """获取指定日期的笔记数量"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        date_dir = self.content_dir / date
        if not date_dir.exists():
            return 0
        
        return len(list(date_dir.glob("*.md")))
    
    def list_available_dates(self) -> List[str]:
        """列出所有有内容的日期"""
        dates = []
        
        for item in self.content_dir.iterdir():
            if item.is_dir():
                # 检查是否有markdown文件
                if any(item.glob("*.md")):
                    dates.append(item.name)
        
        return sorted(dates, reverse=True)


def main():
    """测试代码"""
    loader = ContentLoader("../xiaohongshu")
    
    # 列出可用日期
    dates = loader.list_available_dates()
    print(f"可用日期: {dates}")
    
    # 加载今天的笔记
    notes = loader.load_notes_by_date()
    
    for note in notes:
        print(f"\n标题: {note.title}")
        print(f"标签: {note.hashtags}")
        print(f"内容预览: {note.content[:100]}...")


if __name__ == "__main__":
    main()
