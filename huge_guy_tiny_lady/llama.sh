#!/bin/bash

set -e
sudo dmesg --console-off
MODEL_FILEPATH=<path_to_llm_model>
QUERY_FILEPATH=<path_to_query_file>
ANSWER_FILEPATH=<path_to_save_answer>
THINKING_FILEPATH=<path_to_save_thinking>
THINKING_CHUNK=500
<path_where_llama.cpp_was_cloned>/llama.cpp/build/bin/llama-cli \
-m $MODEL_FILEPATH \
-f $QUERY_FILEPATH \
--temp 1.0 \
--min-p 0.00 \
--top-p 0.95 \
--top-k 20 \
--gpu-layers 999 \
--cpu-moe \
--flash-attn on \
-ot ".ffn_.*_exps.=CPU" \
--mlock \
--single-turn \
--set-thinking-chunk $THINKING_CHUNK \
--save-thinking $THINKING_FILEPATH 
#--save-answer $ANSWER_FILEPATH
