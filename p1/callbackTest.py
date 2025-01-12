import threading
import time

# Define the callback function
def callback(result):
    print(f"Callback received result: {result}")

# Define the worker function that will run in another thread
def worker(callback):
    for i in range(10):
        time.sleep(1)  # Simulate some work
        result = f"Result {i}"
        callback(result)

# Create and start the worker thread
worker_thread = threading.Thread(target=worker, args=(callback,))
worker_thread.start()

# Continue with other tasks in the main thread, if any
print("Main thread is doing other tasks.")

# Wait for the worker thread to finish
worker_thread.join()

print("Worker thread has finished.")
