import threading
import queue
import time

# Job queue
task_queue = queue.Queue()

def worker():
    while True:
        task_func, args = task_queue.get()

        try:
            print(f"[Background Worker] Running task: {task_func.__name__}")
            task_func(*args)
        except Exception as e:
            print(f"[Background Worker] Error: {e}")

        task_queue.task_done()


def start_worker():
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()


def add_task(func, *args):
    task_queue.put((func, args))

def simulate_build(project_name):
    print(f"Starting build for {project_name}")
    time.sleep(5)
    print(f"Build finished for {project_name}")