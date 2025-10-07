import torch
import numpy as np
import time
from accelerate import Accelerator

def reproduce_error():
    """
    A minimal function to reproduce the NCCL error caused by an uneven workload.
    """
    accelerator = Accelerator()
    
    # Define a total number of items that is not divisible by the number of processes (4).
    TOTAL_ITEMS = 10
    
    # Simulate the manual, uneven data splitting from your original code.
    # Splitting 10 items across 4 processes with np.array_split results in chunks of [3, 3, 2, 2].
    all_indices = np.arange(TOTAL_ITEMS)
    indices_this_rank = np.array_split(all_indices, accelerator.num_processes)[accelerator.process_index]
    
    # Print the workload for each process to show that it's unbalanced.
    accelerator.print(
        f"[Rank {accelerator.process_index}] "
        f"I have been assigned {len(indices_this_rank)} items to process."
    )
    
    # Simulate processing each item, with each taking 0.5 seconds.
    for i in range(len(indices_this_rank)):
        accelerator.print(f"[Rank {accelerator.process_index}] Processing my item #{i+1}...")
        time.sleep(0.5)

    accelerator.print(
        f"[Rank {accelerator.process_index}] "
        f"✅ Work finished! Reaching the barrier and waiting..."
    )

    # Wait for all processes to finish their work.
    # This is where the error is triggered.
    # The processes with 2 items will arrive here first and wait for a long time
    # for the processes with 3 items to finish. This long wait and desynchronization
    # ultimately causes the NCCL backend to time out or fail.
    try:
        accelerator.wait_for_everyone()
        accelerator.print(f"[Rank {accelerator.process_index}] 🟢 Successfully passed the barrier! (This is not expected to happen)")
    except Exception as e:
        # You will catch the error here.
        accelerator.print(f"[Rank {accelerator.process_index}] 💥 FAILED at the barrier! Error: {type(e).__name__}")


if __name__ == "__main__":
    reproduce_error()