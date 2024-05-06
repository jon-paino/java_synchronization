import subprocess
import re
import matplotlib.pyplot as plt

def run_test(thread_type, array_size, state_type, num_threads, num_transitions):
    command = f"time java UnsafeMemory {thread_type} {array_size} {state_type} {num_threads} {num_transitions}"
    try:
        # Running the command with subprocess.run(), capturing both stdout and stderr
        result = subprocess.run(command, shell=True, check=True, timeout=3600, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout_output = result.stdout
        real_time_match = re.search(r"Total real time (\d+\.\d+) s", stdout_output)
        if real_time_match:
            real_time = float(real_time_match.group(1))
            return real_time
        else:
            print("Failed to parse real time from output")
            return None
    except subprocess.TimeoutExpired:
        print(f"Command timed out: {command}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Failed to run command: {e}")
        return None


def main():
    thread_types = ["Platform", "Virtual"]
    state_types = ["Null", "Synchronized", "Unsynchronized"]
    array_sizes = [5, 100]
    thread_counts = [1, 8, 40]
    num_transitions = 100000000
    results = {thread_type: {array_size: {state_type: [] for state_type in state_types} for array_size in array_sizes} for thread_type in thread_types}

    # Run tests
    for thread_type in thread_types:
        for array_size in array_sizes:
            for state_type in state_types:
                for num_threads in thread_counts:
                    real_time = run_test(thread_type, array_size, state_type, num_threads, num_transitions)
                    if real_time is not None:
                        results[thread_type][array_size][state_type].append(real_time)
                    else:
                        results[thread_type][array_size][state_type].append(float('nan'))

    # Plot results
    for thread_type in thread_types:
        for array_size in array_sizes:
            plt.figure(figsize=(10, 6))
            for state_type in state_types:
                plt.plot(thread_counts, results[thread_type][array_size][state_type], label=f'{state_type}', marker='o')
            plt.title(f'Performance Metrics for {thread_type} Threads with Array Size {array_size}')
            plt.xlabel('Number of Threads')
            plt.ylabel('Total Real Time (s)')
            plt.legend()
            plt.grid(True)
            plt.savefig(f'Performance_{thread_type}_{array_size}.png')
            plt.show()

if __name__ == "__main__":
    main()
