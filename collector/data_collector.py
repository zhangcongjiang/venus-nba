from collector.database import PsqlConnect


class PsqlCollector:

    @staticmethod
    def collect(key_words, source, database):
        psql = PsqlConnect()
        conn = psql.connect(host="localhost",
                            database="spider",
                            user="postgres",
                            password="postgres",
                            port="5432")

        cur = conn.cursor()

        key_list = []
        for item in key_words:
            msg = f"msg like '%{item}%'"
            key_list.append(msg)
        likewords = ' or '.join(key_list)
        sql = f"""SELECT id, author, msg,  "created_at" FROM public.{database} where ({likewords}) and author ='{source}'  order by "created_at";"""

        cur.execute(sql)
        rows = cur.fetchall()

        # 定义一个空列表，用于存储转换后的字典
        result = []

        # 遍历查询结果，并将每一行转换为字典
        for row in rows:
            # 将查询结果的列名和对应的值组成键值对，并添加到字典中
            row_dict = dict(zip([column[0] for column in cur.description], row))
            # 将字典添加到结果列表中
            result.append(row_dict)

        data = []
        seen = set()
        for item in result:
            field_value = item['author'] + item['msg']
            if field_value not in seen:
                data.append(item)
                seen.add(field_value)

        cur.close()
        conn.close()
        return data

    def today(self):
        psql = PsqlConnect()
        conn = psql.connect(host="localhost",
                            database="spider",
                            user="postgres",
                            password="postgres",
                            port="5432")

        cur = conn.cursor()
        sql = f"""SELECT id, author, msg, news_type, created_at 
        FROM public.hot_news 
        WHERE "created_at"  between  CURRENT_DATE - INTERVAL '1 day' and CURRENT_DATE and author IN ('微博','今日头条','百度') and news_type is not null
        order by "news_type", "created_at";"""

        cur.execute(sql)
        rows = cur.fetchall()

        # 定义一个空列表，用于存储转换后的字典
        result = []

        # 遍历查询结果，并将每一行转换为字典
        for row in rows:
            # 将查询结果的列名和对应的值组成键值对，并添加到字典中
            row_dict = dict(zip([column[0] for column in cur.description], row))
            # 将字典添加到结果列表中
            result.append(row_dict)

        data = []
        seen = set()
        for item in result:
            field_value = item['author'] + item['msg']
            # 过滤不需要的条目
            filters = [18925, 18875, 19488]
            if field_value not in seen and item['id'] not in filters:
                data.append(item)
                seen.add(field_value)

        cur.close()
        conn.close()
        return data


