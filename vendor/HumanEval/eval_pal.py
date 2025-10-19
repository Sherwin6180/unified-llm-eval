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
    parser.add_argument("--model_name_or_path", type=str, required=True, help="Path or HF ID of the model to evaluate.")
    parser.add_argument("--logdir", type=str, default="", help="Directory to save logs and results.")
    parser.add_argument("--language", type=str, default="")
    parser.add_argument("--dataroot", type=str, default="")
    parser.add_argument("--temperature", type=float, default=0.0, help="Temperature for generation.")
    parser.add_argument("--batch_size", type=int, default=1, help="Number of problems to process in a batch.")
    
    args = parser.parse_args()

    model_path = args.model_name_or_path
    logdir = args.logdir
    language = args.language
    batch_size = args.batch_size
    temperature = args.temperature

    start_time = datetime.datetime.now()

    if logdir == "":
        logdir = "tmp/"
        
    tokenizer = dict(
        cls=AutoTokenizer,
        model_path=model_path,)

    dataroot = args.dataroot

    evaluator = evaltor(
        data_root=dataroot,
        max_seq_len=4096,
        tokenizer_cfg=tokenizer,
        log_dir=logdir,
        n_sample=1,
        batch_size=batch_size,
        language=language,
        max_gen_len=500,
        temperature=temperature
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map=accelerator.device, 
        trust_remote_code=True, 
        torch_dtype=torch.bfloat16
    )
    
    if evaluator.tokenizer.pad_token is None:
        print("[INFO] 'pad_token' is not set. Setting 'pad_token = eos_token'...")
        evaluator.tokenizer.pad_token = evaluator.tokenizer.eos_token
    
    if model.config.pad_token_id is None:
        print("[INFO] 'model.config.pad_token_id' is not set. Syncing...")
        model.config.pad_token_id = evaluator.tokenizer.pad_token_id

    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    evaluator.eval_model(
        model, 
        accelerator, 
        model_path=model_path,
        language=language, 
        start_time=start_time
    )