import csv
import psycopg2
import os
import threading
import queue
conn = psycopg2.connect(os.getenv("DB"))



CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS orders_tmp (
    id SERIAL PRIMARY KEY,
    order_id INT,
    be_id VARCHAR(255)
    
)
"""
CREATE_INDEXES = """
CREATE INDEX IF NOT EXISTS orders_tmp_order_id_idx ON orders_tmp (order_id);
CREATE INDEX IF NOT EXISTS orders_tmp_uuid_idx ON orders_tmp (be_id);
"""

CREATE_INDEXES_CONCURRENTLY = """
CREATE INDEX CONCURRENTLY IF NOT EXISTS be_order_id_idx ON recv_order (be_order_id);
"""

with conn.cursor() as cursor:
    cursor.execute(CREATE_TABLE)
    cursor.execute(CREATE_INDEXES)


PRINTER_QUEUE = queue.Queue()

def printer():
    while True:
        item = PRINTER_QUEUE.get()
        if item is None:
            break
        print(item)

printer_thread = threading.Thread(target=printer)
printer_thread.start()
def process(conn, id_, be_order_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id from recv_order where be_order_id = %s", (be_order_id,))
        order_id = cursor.fetchone()
        if order_id is not None:
            order_id = order_id[0]
            cursor.execute("INSERT INTO orders_tmp (id, order_id, be_id) VALUES (%s, %s, %s)", (id_, order_id, be_order_id))
        else:
            PRINTER_QUEUE.put(be_order_id)
        conn.commit()

def insert_process(queue):
    conn = psycopg2.connect(os.getenv("DB"))
    while True:
        item = queue.get()
        if item is None:
            queue.put(None)
            conn.close()
            break
        else:
            id_, be_order_id = item
            process(conn, id_, be_order_id)

queue = queue.Queue()
threads = [threading.Thread(target=insert_process, args=(queue,)) for _ in range(10)]
[thread.start() for thread in threads]
with open("sqllab_query_analyticsdelivery_eta_total_orders_rate_20250127T071640.csv")  as file:
    reader = csv.reader(file)
    with conn.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE orders_tmp")
        conn.commit()
        for i, row in enumerate(reader):
            be_id = row[0]
            queue.put([i, be_id])
queue.put(None)

[thread.join() for thread in threads]
PRINTER_QUEUE.put(None)
printer_thread.join()
conn.close()

