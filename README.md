# ghosts-of-data-past

a ghost from data generator - generates a chat with text messages and selfies from recorded conversations

## background

requires dataset recording, preperation and model finetuning with the following repositories:

- recording a chat between two performers: https://github.com/papayapeter/theater-chat
- preparing chat and mail data and finetuning a gpt-2 model with it: https://github.com/papayapeter/gpt-2-training
- finetuning a stylegan3 model with face images by performers: https://github.com/papayapeter/stylegan3
- generating notification sound abstractions: \_

using [aitextgen](https://github.com/minimaxir/aitextgen) for text generation & [stylegan3](https://github.com/NVlabs/stylegan3). some code has been copies over from the original stylegan3 repo to make image generation and textgeneration work seamlessly together.

## setup

1. to create the envorinment: `conda env create -f environment.yml`
2. activate the enviroment: `conda activate ghosts`
3. changes to the environment can be saved with: `conda env export --no-builds | grep -v "prefix" > environment.yml`
4. as the site served is built with sveltekit, it's dependencies must be installed and it must be built: `cd serve/site && npm install && npm run build`
