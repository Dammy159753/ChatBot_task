#!/usr/bin/env bash
python -m rasa_nlu.train --data ./tools/train_file_new.json \
    --config ccb_chatbot_config.yml \
    --path projects \
    --fixed_model_name new_nlu \
    --project ccb_nlu
