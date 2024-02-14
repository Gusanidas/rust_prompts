# model = "mistral-medium"
max_iters="42"
model_gpt="mistral-medium"
model_gpt="gpt-3.5-turbo-0125"

python async_main.py --language rs --strategy iterative --max_iters "$max_iters" --few_shot 1 --model "$model_gpt" --post_process "True" > "out1.txt"
end_time=$(date +%s)
echo "Completed async_main.py with language rs and few_shot 1 and model $model_gpt in $((end_time - start_time)) seconds"
start_time=$(date +%s)

python async_main.py --language py --strategy iterative --max_iters "$max_iters" --few_shot 1 --model "$model_gpt" --post_process "True" > "out1.txt"
end_time=$(date +%s)
echo "Completed async_main.py with language rs and few_shot 1 and model $model_gpt in $((end_time - start_time)) seconds"
start_time=$(date +%s)


python async_main.py --language rs --strategy retry --max_iters "$max_iters" --few_shot 1 --model "$model_gpt" --post_process "True" > "out1.txt"
end_time=$(date +%s)
echo "Completed async_main.py with language rs and few_shot 1 and model $model_gpt in $((end_time - start_time)) seconds"
start_time=$(date +%s)

python async_main.py --language py --strategy retry --max_iters "$max_iters" --few_shot 1 --model "$model_gpt" --post_process "True" > "out1.txt"
end_time=$(date +%s)
echo "Completed async_main.py with language rs and few_shot 1 and model $model_gpt in $((end_time - start_time)) seconds"
start_time=$(date +%s)