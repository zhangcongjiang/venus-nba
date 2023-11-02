from collector.database import PsqlConnect


class DataClean:
    @staticmethod
    def clean():
        psql = PsqlConnect()
        conn = psql.connect(host="localhost",
                            database="spider",
                            user="postgres",
                            password="postgres",
                            port="5432")

        cur = conn.cursor()
        tag = ['news', 'shopping', 'tech', 'ent', 'developer', 'community']
        for item in tag:
            sql = f"""DELETE FROM hot_{item}
            WHERE id NOT IN (
              SELECT MIN(id)
              FROM hot_{item}
              GROUP BY "msg" 
            );"""
            cur.execute(sql)
            print(f"{item}清理完成")
        cur.close()
        conn.close()


if __name__ == '__main__':
    dc = DataClean()
    dc.clean()
