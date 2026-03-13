"""
账号管理器
支持多账号Cookie隔离和管理
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from loguru import logger


@dataclass
class Account:
    """账号信息"""
    name: str
    alias: str
    cookie_file: str
    created_at: str
    last_used: Optional[str] = None
    status: str = "inactive"  # inactive, active, expired
    notes_count: int = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Account":
        return cls(**data)


class AccountManager:
    """账号管理器"""
    
    def __init__(self, accounts_dir: str = "./cookies"):
        self.accounts_dir = Path(accounts_dir)
        self.accounts_dir.mkdir(exist_ok=True)
        self.accounts_file = self.accounts_dir / "accounts.json"
        self.accounts: Dict[str, Account] = {}
        self._load_accounts()
    
    def _load_accounts(self):
        """加载账号列表"""
        if self.accounts_file.exists():
            try:
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, acc_data in data.items():
                        self.accounts[name] = Account.from_dict(acc_data)
                logger.info(f"加载 {len(self.accounts)} 个账号")
            except Exception as e:
                logger.error(f"加载账号失败: {e}")
    
    def _save_accounts(self):
        """保存账号列表"""
        try:
            data = {name: acc.to_dict() for name, acc in self.accounts.items()}
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存账号失败: {e}")
    
    def add_account(self, name: str, alias: str = "") -> Account:
        """添加新账号"""
        if name in self.accounts:
            raise ValueError(f"账号 {name} 已存在")
        
        account = Account(
            name=name,
            alias=alias or name,
            cookie_file=f"{name}.json",
            created_at=datetime.now().isoformat()
        )
        
        self.accounts[name] = account
        self._save_accounts()
        logger.info(f"添加账号: {name}")
        return account
    
    def remove_account(self, name: str) -> bool:
        """删除账号"""
        if name not in self.accounts:
            return False
        
        account = self.accounts[name]
        
        # 删除Cookie文件
        cookie_file = self.accounts_dir / account.cookie_file
        if cookie_file.exists():
            cookie_file.unlink()
        
        del self.accounts[name]
        self._save_accounts()
        logger.info(f"删除账号: {name}")
        return True
    
    def get_account(self, name: str) -> Optional[Account]:
        """获取账号"""
        return self.accounts.get(name)
    
    def list_accounts(self) -> List[Account]:
        """列出所有账号"""
        return list(self.accounts.values())
    
    def set_default(self, name: str) -> bool:
        """设置默认账号"""
        if name not in self.accounts:
            return False
        
        # 保存默认账号配置
        config_file = self.accounts_dir / "default.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump({"default": name}, f)
        
        logger.info(f"设置默认账号: {name}")
        return True
    
    def get_default(self) -> Optional[Account]:
        """获取默认账号"""
        config_file = self.accounts_dir / "default.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    default_name = data.get("default")
                    if default_name:
                        return self.accounts.get(default_name)
            except Exception as e:
                logger.error(f"读取默认账号失败: {e}")
        
        # 返回第一个账号
        if self.accounts:
            return list(self.accounts.values())[0]
        return None
    
    def update_status(self, name: str, status: str):
        """更新账号状态"""
        if name in self.accounts:
            self.accounts[name].status = status
            self.accounts[name].last_used = datetime.now().isoformat()
            self._save_accounts()
    
    def increment_notes(self, name: str):
        """增加笔记计数"""
        if name in self.accounts:
            self.accounts[name].notes_count += 1
            self._save_accounts()
    
    def get_cookie_path(self, name: str) -> Optional[Path]:
        """获取Cookie文件路径"""
        account = self.accounts.get(name)
        if account:
            return self.accounts_dir / account.cookie_file
        return None
    
    def cookie_exists(self, name: str) -> bool:
        """检查Cookie是否存在"""
        cookie_path = self.get_cookie_path(name)
        return cookie_path.exists() if cookie_path else False


def main():
    """测试代码"""
    manager = AccountManager()
    
    # 添加测试账号
    try:
        acc = manager.add_account("test_account", "测试账号")
        print(f"添加账号: {acc}")
    except ValueError as e:
        print(f"账号已存在: {e}")
    
    # 列出账号
    accounts = manager.list_accounts()
    print(f"\n共有 {len(accounts)} 个账号:")
    for acc in accounts:
        print(f"  - {acc.name} ({acc.alias}): {acc.status}")
    
    # 获取默认账号
    default = manager.get_default()
    if default:
        print(f"\n默认账号: {default.name}")


if __name__ == "__main__":
    main()
