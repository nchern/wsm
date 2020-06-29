import psycopg2

from wsm.settings import DSN


INSERT_SQL_STMT = '''INSERT INTO check_result
        (id, created, url, status, response_time_ms)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;'''


def save_to_db(batch):
    # this is not the most optimal way to send data to the database
    with psycopg2.connect(**DSN) as conn:
        with conn.cursor() as cur:
            for item in batch:
                cur.execute(
                    INSERT_SQL_STMT,
                    (
                        item.id,
                        item.created,
                        item.url,
                        item.status,
                        item.response_time_ms,
                    ),
                )
