from collector.database import PsqlConnect
import pandas as pd


def execute_sql(sql):
    psql = PsqlConnect()
    conn = psql.connect(host="localhost",
                        database="spider",
                        user="postgres",
                        password="postgres",
                        port="5432")

    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()

    # 定义一个空列表，用于存储转换后的字典
    result = []

    # 遍历查询结果，并将每一行转换为字典
    for row in rows:
        # 将查询结果的列名和对应的值组成键值对，并添加到字典中
        # row_dict = dict(zip([column[0] for column in cur.description], row))
        # 将字典添加到结果列表中
        result.append(row[0])

    cur.close()
    conn.close()

    return result


if __name__ == '__main__':
    sql = """SELECT pts FROM public.player_regular_game where player_name ='Stephen Curry ';"""
    result = execute_sql(sql)
    total = [0]
    sum = 0
    for data in result:
        sum += data
        total.append(sum)
    df = pd.DataFrame([total], columns=[f'{i}' for i in range(len(total))])
    df.to_excel('Curry.xlsx', index=False)
