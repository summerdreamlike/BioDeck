import os
import sqlite3


def export_sqlite_db(db_path: str, dump_path: str) -> None:
    os.makedirs(os.path.dirname(dump_path), exist_ok=True)
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"未找到数据库文件: {db_path}")

    with sqlite3.connect(db_path) as conn:
        conn.text_factory = str
        cur = conn.cursor()
        cur.execute('PRAGMA foreign_keys=OFF;')
        cur.execute('PRAGMA journal_mode=OFF;')

        with open(dump_path, 'w', encoding='utf-8') as f:
            f.write('-- SQLite database dump\n')
            f.write('PRAGMA foreign_keys=OFF;\n')
            f.write('BEGIN TRANSACTION;\n')
            for line in conn.iterdump():
                # 跳过事务控制语句，使用我们自定义的 BEGIN/COMMIT
                if line.startswith('BEGIN TRANSACTION') or line.startswith('COMMIT'):
                    continue
                f.write(f"{line}\n")
            f.write('COMMIT;\n')

    print(f"✅ 已导出到: {dump_path}")


if __name__ == '__main__':
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(root, 'database.db')
    dump_path = os.path.join(os.path.dirname(__file__), 'dump.sql')
    export_sqlite_db(db_path, dump_path)
    print('使用方法: 在目标机器运行 import_db.py 即可导入该 dump.sql')


