import threading
import time

# Function to be executed in a separate thread
def infinite_loop_worker():
    global data
    data = 1
    while True:
        data +=1
        print("Worker thread is running...")
        time.sleep(2)  # Sleep for 2 seconds to avoid flooding the console

# Start the worker thread with the infinite loop
worker_thread = threading.Thread(target=infinite_loop_worker)

# Set the thread as a daemon so it will automatically exit when the main program finishes
worker_thread.daemon = True

# Start the thread
data = 0
worker_thread.start()
# Main thread continues to run
for i in range(10):
    print(f"Main thread iteration {i}")
    print(data)
    time.sleep(1)

# The program ends here, but the worker thread will keep running in the background because it's a daemon