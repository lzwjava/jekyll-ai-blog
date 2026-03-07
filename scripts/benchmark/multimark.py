import multiprocessing
import random
import time
import os
import matplotlib.pyplot as plt


def sort_chunk(arr, start, end, conn):
    chunk = arr[start:end]
    chunk.sort()
    conn.send(chunk)
    conn.close()


def merge(left, right):
    result = []
    i = j = 0
    left_len, right_len = len(left), len(right)
    while i < left_len and j < right_len:
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def parallel_sort(arr, process_count):
    n = len(arr)
    chunk_size = (n + process_count - 1) // process_count
    processes = []
    parent_conns = []

    # Sort each chunk in a separate process
    for i in range(process_count):
        start = i * chunk_size
        end = min(start + chunk_size, n)
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(
            target=sort_chunk, args=(arr, start, end, child_conn)
        )
        processes.append(p)
        parent_conns.append(parent_conn)
        p.start()

    sorted_chunks = [conn.recv() for conn in parent_conns]
    for p in processes:
        p.join()

    # Merge sorted chunks
    while len(sorted_chunks) > 1:
        merged_chunks = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                merged = merge(sorted_chunks[i], sorted_chunks[i + 1])
                merged_chunks.append(merged)
            else:
                merged_chunks.append(sorted_chunks[i])
        sorted_chunks = merged_chunks

    return sorted_chunks[0] if sorted_chunks else []


def benchmark(process_count=1, list_size=1000000):
    arr = [random.randint(0, 1000000) for _ in range(list_size)]
    start = time.time()
    parallel_sort(arr, process_count)
    end = time.time()
    return end - start


if __name__ == "__main__":
    print(f"CPU cores: {os.cpu_count()}")
    process_counts = [1, 2, 4, 8, 16, 32, 64]
    times = []
    list_size = 50_000_000  # Adjust for reasonable runtime

    for n in process_counts:
        t = benchmark(process_count=n, list_size=list_size)
        print(f"Processes: {n}, Time taken: {t:.4f} seconds")
        times.append(t)

    # Print results as CSV for external plotting
    print("\nProcessCount,TimeTakenSeconds")
    for i in range(len(process_counts)):
        print(f"{process_counts[i]},{times[i]:.6f}")

    plt.figure()
    plt.plot(process_counts, times, marker="o")
    plt.xlabel("Number of Processes")
    plt.ylabel("Time Taken (seconds)")
    plt.title("Process Count vs Time Taken")
    plt.grid(True)
    plt.savefig("test/process.png")
