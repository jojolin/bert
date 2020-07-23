python run_ner_baidu_ie.py \
  --task_name=NER \
  --do_train=true \
  --do_eval=true \
  --do_predict=false \
  --data_dir=$BAIDU_IE_DIR \
  --vocab_file=$BERT_CHINESE_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_CHINESE_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_CHINESE_BASE_DIR/bert_model.ckpt \
  --max_seq_length=128 \
  --train_batch_size=64 \
  --learning_rate=2e-5 \
  --num_train_epochs=3.0 \
  --output_dir=./ner_baidu_ie

