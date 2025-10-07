# export NCCL_DEBUG=INFO

# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/deepseek-6.7b-instruct/"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/FFT-Ruby"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/FFT-instruct-Ruby-nogc"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/FFT-instruct-Ruby-b64"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/FFT-instruct-Ruby-600maxstep"

# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/FFT-instruct-Julia-3/"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/random_merged_models/merged_models_window_5/merged_model_random_layers_0-2-18-19-31/"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/rust_merged_models/merged_model_full/"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/FFT-instruct-Golang-linuxmreitt"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/FFT-instruct-Rust-ammar-100k"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/FFT-instruct-Golang-linuxmreitt-ExAi"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/FFT-instruct-Golang-standard-instruct"
# MODEL_NAME_OR_PATH="/scratch/shared_dir/xinyu/workdir/sandhi-work/merged_model_final_rust_go_final_rust_go"

DATASET_ROOT="data/"
# LANGUAGE="python"
CUDA_VISIBLE_DEVICES=0,1,5,6 python -m accelerate.commands.launch --config_file test_config.yaml eval_pal.py --logdir ${MODEL_NAME_OR_PATH} --language ${LANGUAGE} --dataroot ${DATASET_ROOT}
