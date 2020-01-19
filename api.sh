 #!/usr/bin/env bash
python -m rasa_core.run \ 
    --enable_api "http://10.1.58.21:5000" \
    -d models/dialogue \ 
    -u projects/ccb_nlu/new_nlu \
    -o out.log
