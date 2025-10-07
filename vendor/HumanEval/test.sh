#!/bin/bash
echo "--- Attempting to Reproduce the NCCL Error ---"
echo "4 processes will handle 10 items, creating an uneven workload."
echo "Ranks 2 and 3 are expected to finish early and wait, eventually causing the error."
echo "------------------------------------------------"
sleep 2

accelerate launch --config_file accelerate_config.yaml test.py