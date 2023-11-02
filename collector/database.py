import psycopg2


class PsqlConnect:

    @staticmethod
    def connect(host, database, user, password, port):
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        return conn
