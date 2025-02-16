import pandas as pd
import sqlite3

def store_tables_in_sqlite(tables, db_path="tables.db"):
    """
    将解析后的表格（HTML 格式）通过 Pandas 解析后存入 SQLite 数据库，每个表格
    生成一个或多个数据表。
    """
    conn = sqlite3.connect(db_path)
    for i, table_html in enumerate(tables):
        try:
            # 解析 HTML 中所有的 table 元素
            dfs = pd.read_html(table_html)
            for j, df in enumerate(dfs):
                table_name = f"table_{i}_{j}"
                df.to_sql(table_name, con=conn, if_exists="replace", index=False)
                print(f"已存入表：{table_name}")
        except Exception as e:
            print(f"处理第 {i} 个表格失败: {e}")
    conn.close()

def query_table(query, db_path="tables.db"):
    """
    对存储的表格数据执行 SQL 查询，返回查询结果的 DataFrame。
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df