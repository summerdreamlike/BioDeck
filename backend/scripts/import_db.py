import os
import sqlite3


def import_sqlite_db(db_path: str, dump_path: str) -> None:
    if not os.path.exists(dump_path):
        raise FileNotFoundError(f"未找到 dump.sql: {dump_path}")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)

    with sqlite3.connect(db_path) as conn:
        conn.text_factory = str
        cur = conn.cursor()
        with open(dump_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        cur.executescript(sql)
        conn.commit()

    print(f"✅ 已从 {dump_path} 导入到: {db_path}")


if __name__ == '__main__':
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(root, 'database.db')
    dump_path = os.path.join(os.path.dirname(__file__), 'dump.sql')
    import_sqlite_db(db_path, dump_path)
    print('导入完成。若后端运行中，请重启后端使变更生效。')


