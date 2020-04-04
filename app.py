import datetime
import queue
import threading
import time

q = queue.Queue()

max_wait_time = datetime.timedelta(seconds=0.6)
# How many seconds without an update.

last_process_time = datetime.datetime.now()
# The time of the last successful update.

n = 11
# number of events

def worker():
  global max_wait_time
  global last_process_time

  while True:
    item = q.get()

    # release thread
    if item is None:
      q.task_done()
      break

    start_process = item['timestamp']

    time.sleep(0.5)

    process_time = start_process - last_process_time

    print('.')
    if not q.empty() and process_time < max_wait_time:
        q.task_done()
        continue

    last_process_time = datetime.datetime.now()
    print('TRIGGER > process time:', process_time, 'queue size:', q.qsize(), 'payload:', item)

    q.task_done()

t = threading.Thread(target=worker)
t.start()

for i in range(n):
  data = { 'timestamp': datetime.datetime.now(), 'id': i }
  time.sleep(0.2)
  q.put(data)

time.sleep(5)
data = { 'timestamp': datetime.datetime.now(), 'id': n }
q.put(data)

time.sleep(10)
q.put(None)

t.join()
