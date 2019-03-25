source ./ENV.sh

python run_ner_CoNLL_2003.py \
  --task_name=NER \
  --do_train=true \
  --do_eval=false \
  --do_predict=true \
  --data_dir=$CONLL_2003_DIR \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --max_seq_length=128 \
  --train_batch_size=32 \
  --learning_rate=2e-5 \
  --num_train_epochs=3.0 \
  --output_dir=/tmp/baidu_ie/
