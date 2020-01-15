CURRENT_DIR=`pwd`

# python main.py train
# python main.py train --use_cuda=False --batch_size=10

# base模型
# python al_main.py train --use_cuda=False --batch_size=100 \
#      --rnn_layer=2 --dropout_ratio=0.2 --dropout1=0.2 \
#      --base_epoch=2 \
#      --albert_path=tdata/albert_base_zh/ \
#      --vocab=tdata/albert_base_zh/vocab.txt
#使用小模型
python al_main.py train --use_cuda=False --batch_size=400 \
     --rnn_layer=2 --dropout_ratio=0.2 --dropout1=0.2 \
     --rnn_hidden=200 \
     --base_epoch=2 \
     --conf="/mnt/data/dev/github/标注数据/Bert-BiLSTM-CRF-pytorch/result/config.json" \
     --albert_embedding=312 \
     --albert_path=tdata/albert_tiny/ \
     --vocab=tdata/albert_tiny/vocab.txt




# export BERT_BASE_DIR=$CURRENT_DIR/prev_trained_model/albert_tiny
# export DATA_DIR=$CURRENT_DIR/dataset
# export OUTPUR_DIR=$CURRENT_DIR/outputs
# TASK_NAME="terryner"

# python run_classifier.py \
#   --model_type=albert \
#   --model_name_or_path=$BERT_BASE_DIR \
#   --task_name=$TASK_NAME \
#   --do_train \
#   --do_eval \
#   --do_lower_case \
#   --data_dir=$DATA_DIR/${TASK_NAME}/ \
#   --max_seq_length=512 \
#   --per_gpu_train_batch_size=32 \
#   --per_gpu_eval_batch_size=64 \
#   --learning_rate=1e-8 \
#   --num_train_epochs=60.0 \
#   --logging_steps=3731 \
#   --save_steps=3731 \
#   --output_dir=$OUTPUR_DIR/${TASK_NAME}_output/ \
#   --overwrite_output_dir



# python run_classifier.py \
#   --model_type=albert \
#   --model_name_or_path=$BERT_BASE_DIR \
#   --task_name=$TASK_NAME \
#   --do_train \
#   --do_eval \
#   --do_lower_case \
#   --data_dir=$DATA_DIR/${TASK_NAME}/ \
#   --max_seq_length=128 \
#   --per_gpu_train_batch_size=64 \
#   --per_gpu_eval_batch_size=64 \
#   --learning_rate=1e-4 \
#   --num_train_epochs=5.0 \
#   --logging_steps=3731 \
#   --save_steps=3731 \
#   --output_dir=$OUTPUR_DIR/${TASK_NAME}_output/ \
#   --overwrite_output_dir
