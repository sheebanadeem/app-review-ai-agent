import time

def run_step(name, fn, *args):
    start = time.time()
    result = fn(*args)
    duration = round(time.time() - start, 2)
    print(f"[✓] {name} completed in {duration}s")
    return result
