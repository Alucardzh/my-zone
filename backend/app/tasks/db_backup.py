"""备份数据"""
from pathlib import Path
from datetime import datetime
import sqlite3
from app.config import db_settings


def safe_backup() -> None:
    """热备份sqlite"""
    backup_path = Path(db_settings.sqlite_db_path).parent / "backup"
    backup_path.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    source = sqlite3.connect(db_settings.sqlite_db_path)
    backup = sqlite3.connect(f"{backup_path}/backup_{now}.sqlite3")
    with backup:
        source.backup(backup)
    backup.close()
    source.close()


if __name__ == "__main__":
    safe_backup()