import threading


def worker():
    print(f"Thread {threading.current_thread().name} is running")

threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("All threads have completed")