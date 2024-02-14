model_gpt="gpt-3.5-turbo-0125"
model_gpt="mistral-medium"
max_iters="77"
benchmark="mbpp" # Setting benchmark to "mbpp" directly

run_async_main() {
    local language="$1"
    local strategy="$2"
    local few_shot="$3"
    local post_process="$4"
    local out_file="$5"

    start_time=$(date +%s)
    if [[ "$post_process" == "True" ]]; then
        python async_main.py --language "$language" --strategy "$strategy" --max_iters "$max_iters" --few_shot "$few_shot" --model "$model_gpt" --post_process "True" --benchmark "$benchmark" > "$out_file"
    else
        python async_main.py --language "$language" --strategy "$strategy" --max_iters "$max_iters" --few_shot "$few_shot" --model "$model_gpt" --benchmark "$benchmark" > "$out_file"
    fi
    end_time=$(date +%s)
    echo "Completed async_main.py with language $language, strategy $strategy, few_shot $few_shot, model $model_gpt, and benchmark $benchmark in $((end_time - start_time)) seconds"
}

# Using the function to run commands with different parameters
run_async_main py prompt_extract 1 False "out1.txt"

# Few shot with various few_shot values and strategies
run_async_main py few_shot_2 1 True "out2.txt"
run_async_main py few_shot_2 2 True "out3.txt"
run_async_main py few_shot_2 3 True "out4.txt"
run_async_main py few_shot_2 4 True "out5.txt"
run_async_main py few_shot_2 5 True "out6.txt"

run_async_main py few_shot 3 True "out7.txt"
run_async_main py few_shot 4 True "out8.txt"

# COT with various few_shot values and strategies
run_async_main py cot_2 1 True "out9.txt"
run_async_main py cot_2 2 True "out10.txt"
run_async_main py cot_2 3 True "out11.txt"
run_async_main py cot_2 4 True "out12.txt"
run_async_main py cot_2 5 True "out13.txt"

run_async_main py cot 3 True "out14.txt"
run_async_main py cot 4 True "out15.txt"

# Iterative and Retry strategies
run_async_main py iterative 1 True "out16.txt"
run_async_main py iterative 4 True "out17.txt"
run_async_main py retry 4 True "out18.txt"
