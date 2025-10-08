import os
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
import json
import torch.distributed as dist
import subprocess
import sys
from accelerate import Accelerator
from accelerate import DistributedDataParallelKwargs
from pathlib import Path
from argparse import ArgumentParser
from humaneval import HumanEval as evaltor
from transformers import AutoTokenizer, AutoModelForCausalLM
import datetime

if __name__ == '__main__':
    kwargs_handlers = [DistributedDataParallelKwargs(find_unused_parameters=True)]
    accelerator = Accelerator(mixed_precision="bf16", kwargs_handlers=kwargs_handlers)   


    parser = ArgumentParser()
    parser.add_argument("--model_path", type=str, required=True, help="Path to the model directory")
    parser.add_argument("--log_dir", type=str, default="tmp/", help="Directory for logging evaluation outputs")
    parser.add_argument("--language", type=str, default="", help="Programming language for evaluation")
    parser.add_argument("--dataroot", type=str, default="", help="Root directory for evaluation data")
    
    args = parser.parse_args()

    model_path = args.model_path
    log_dir = args.log_dir
    language = args.language

    start_time = datetime.datetime.now()

    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    tokenizer = dict(
        cls=AutoTokenizer,
        model_path=model_path,)

    dataroot = args.dataroot

    evaluator = evaltor(data_root=dataroot, max_seq_len=4096, tokenizer_cfg=tokenizer, log_dir=log_dir, n_sample=1, batch_size=32, language=language, max_gen_len=500)

    model = AutoModelForCausalLM.from_pretrained(model_path, device_map=accelerator.device, trust_remote_code=True, torch_dtype=torch.bfloat16)
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    evaluator.eval_model(model, accelerator, model_path=model_path, language=language, start_time=start_time)
