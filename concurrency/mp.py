import multiprocessing


def worker():
    print(f"Process {multiprocessing.current_process().name} is running")

processes = []
for i in range(5):
    p = multiprocessing.Process(target=worker)
    p.start()
    processes.append(p)

for p in processes:
    p.join()

print("All processes have completed")