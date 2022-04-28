# ghosts-of-data-past

a ghost from data generator - generates a chat with text messages and selfies from recorded conversations

## background

requires dataset recording, preperation and model finetuning with the following repositories:

- recording a chat between two performers: https://github.com/papayapeter/theater-chat
- preparing chat and mail data and finetuning a gpt-2 model with it: https://github.com/papayapeter/gpt-2-training
- finetuning a stylegan3 model with face images by performers: https://github.com/papayapeter/stylegan3
- generating notification sound abstractions: \_

## setup

1. to create the envorinment: `conda env create -f environment.yml`
2. activate the enviroment: `conda activate ghosts`
3. changes to the environment can be saved with: `conda env export --no-builds | grep -v "prefix" > environment.yml`
