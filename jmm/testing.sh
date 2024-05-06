#!/bin/bash

# Array of thread counts to test
thread_counts=(1 8 40)
array_sizes=(5 100)
thread_types=("Platform" "Virtual")

# Output CSV file
output_file="performance_data.csv"

# Write the CSV header
echo "ThreadCount,SyncType,ThreadType,ArraySize,RealTime,AvgSwapTime,OutputMismatch" > "$output_file"

# Test different synchronization types
for sync_type in Null Synchronized Unsynchronized; do
    for thread_count in "${thread_counts[@]}"; do
        for thread_type in "${thread_types[@]}"; do
            for array_size in "${array_sizes[@]}"; do
                echo "Testing $sync_type with $thread_count $thread_type threads and array size $array_size..."
                
                # Run the Java program and capture its output
                output=$(time timeout 3600 java UnsafeMemory "$thread_type" "$array_size" "$sync_type" "$thread_count" 100000000 2>&1)
                
                # Extract relevant metrics from output
                real_time=$(echo "$output" | grep 'Total real time' | awk '{print $4}')
                avg_swap_time=$(echo "$output" | grep 'Average real swap time' | awk '{print $5}')
                output_sum=$(echo "$output" | grep 'output sum mismatch' | awk '{print $3}')
                
                # Append data to CSV
                echo "$thread_count,$sync_type,$thread_type,$array_size,$real_time,$avg_swap_time,$output_sum" >> "$output_file"
            done
        done
    done
done
