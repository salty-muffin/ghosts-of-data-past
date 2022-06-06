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
5. install redis according to these [instructions](https://redis.io/docs/getting-started/installation/install-redis-on-linux/)
6. start redis with the config file in this project `redis-server redis.conf` (from this directory)

## serve - to do

- [x] add keys to svelte each https://svelte.dev/tutorial/keyed-each-blocks
- [ ] construct chat bubbles (this might help https://svelte.dev/tutorial/dimensions)
- [x] autoscroll to the bottom https://svelte.dev/tutorial/update (doesn't work with images yet on the desktop) including notifications for new messages if not scrolled to the bottom
- [x] optimize https://svelte.dev/tutorial/svelte-options
- [x] BETTER: pause css animations when not visible https://css-tricks.com/how-to-play-and-pause-css-animations-with-css-custom-properties/, https://abcdinamo.com/news/using-variable-fonts-on-the-web, https://svelte.dev/repl/c461dfe7dbf84998a03fdb30785c27f3?version=3.16.7, https://www.npmjs.com/package/svelte-intersection-observer
- [x] implement soft transitions between pages https://dev.to/evanwinter/page-transitions-with-svelte-kit-35o6
- [ ] scroll down on return from about
- [x] change intersection observer for better performance an readability by only adding new elements
- [x] limit the number of chat messages

## generate - to do

- [x] add redis installation to the setup documentation
- [x] secure redis
- [ ] fix saving to redis
