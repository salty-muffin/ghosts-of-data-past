# ghosts of data past

a ghost from data generator - generates a chat with text messages and selfies from recorded conversations

## background

requires dataset recording, preperation and model finetuning with the following repositories:

- recording a chat between two performers: https://github.com/salty-muffin/theater-chat
- preparing chat and mail data and finetuning a gpt-2 model with it: https://github.com/salty-muffin/gpt-2-training
- finetuning a stylegan3 model with face images by performers: https://github.com/salty-muffin/stylegan3
- generating notification sound abstractions: https://github.com/papayapeter/nsynth-notification-sound-generation

using [aitextgen](https://github.com/minimaxir/aitextgen) for text generation, [stylegan3](https://github.com/NVlabs/stylegan3) and [nsynth](https://github.com/magenta/magenta/tree/main/magenta/models/nsynth) for sound abstractions. some code has been copied over from the original stylegan3 repo to make image generation and text generation work seamlessly together.

all ai models used as part of this work were finetuned with data captured or created by me and are not publicy avaliable. you are however free to use this code with your own models under the licenses below.

the same applies to the sounds used.

## setup

1. to create the envorinment: `conda env create -f environment.yml` or `conda env create -f environment-cpu.yml` for a cpu only version
2. activate the enviroment: `conda activate ghosts` or `conda activate ghosts-cpu`
3. as the site served is built with sveltekit, it's dependencies must be installed and it must be built: `cd serve/site && npm install && npm run build`
4. install redis according to these [instructions](https://redis.io/docs/getting-started/installation/install-redis-on-linux/)
5. possibly necessary to disable redis autostart `sudo systemctl disable redis-server`

## run

all the steps below should be executed from individual terminals or at least in individual processes

1. start the redis server: `redis-server redis.conf`
2. enter the conda environment: `conda activate ghosts` or `conda activate ghosts-cpu`
3. start the generate script with `python3 generate/generate.py --gptdir=generate/models/gpt2_model --stylegandir=generate/models --sounddir=generate/notification-sounds --prompt=[SCIENTIST:] I can't believe you. --roles=artist,scientist --colors=cyan,green --basetime=3.0 --lettertime=0.2 --imagetime=6.0 --readfactor=0.8 --randomfactor=0.9,1.1` (this is only an example configuration)
4. start the server with `python3 serve/app.py`

## notes

this repo includes a modified version of [@jsdevtools/rehype-toc](https://github.com/JS-DevTools/rehype-toc). i had to modify it to get the automatically generated table of contents working with mdsvex and put it in the root of this repo as a .tgz file.

the fonts used in this project are [abc favorit](https://abcdinamo.com/typefaces/favorit) variable and [pw smokey](https://www.dafont.com/pwsmokey.font). the fonts are not tracked in this repo for licensing reasons.

## mentions

the work on this project was sponsored by the [kulturstiftung des freistaates sachsen](https://kdfs.de). this measure is co-financed by tax funds on the basis of the of the budget passed by the saxon state parliament.

<div style="padding: 1em; background-color: white; max-width: 400px; margin: 1em 0">
    <img src="doc/KDFS_Logo%2BWappen%2BText_2020_RGB.jpg" alt="kdfs logo">
</div>

## to dos

### serve

- [x] add keys to svelte each https://svelte.dev/tutorial/keyed-each-blocks
- [x] construct chat bubbles (this might help https://svelte.dev/tutorial/dimensions)
- [x] autoscroll to the bottom https://svelte.dev/tutorial/update (doesn't work with images yet on the desktop) including notifications for new messages if not scrolled to the bottom
- [x] optimize https://svelte.dev/tutorial/svelte-options
- [x] BETTER: pause css animations when not visible https://css-tricks.com/how-to-play-and-pause-css-animations-with-css-custom-properties/, https://abcdinamo.com/news/using-variable-fonts-on-the-web, https://svelte.dev/repl/c461dfe7dbf84998a03fdb30785c27f3?version=3.16.7, https://www.npmjs.com/package/svelte-intersection-observer
- [x] implement soft transitions between pages https://dev.to/evanwinter/page-transitions-with-svelte-kit-35o6
- [x] scroll down on return from about
- [x] change intersection observer for better performance an readability by only adding new elements
- [x] limit the number of chat messages
- [x] decrease the distance between messages from the same sender
- [x] remove the name of messages by the same sender
- [x] implement sidenotes on about
- [x] implement proper menu on about with mute controls
- [x] fix clicking, touching & hovering behaviour on sidenotes (add resize listener, fix clicking vs. hovering, remove clicking behaviour on desktops)
- [x] check, whether socketio.on is triggered after recieving all data
- [x] maybe transfer the font animation to the index page (if it is not used in the about pages)
- [x] check whether the intersection observer works when returning from the abouts page
- [x] add rehype plugin for toc
- [x] fix breathing intersection observers for heading with automatic toc
- [x] beautify layout for about pages
- [x] seperate the nav out (one for chat and one for the about pages)
- [ ] donate for pw smokey https://www.dafont.com/pwsmokey.font
- [x] change the scrolling behaviour (possibly scroll on the main window and make the nav fixed)
- [x] keep scroll position on navigation
- [x] add ability to unmute video
- [x] add favicon
- [x] update to sveltekit 1.0 (including app.html) for this and the documentation
- [ ] implement wildcard response from serve app (especially so that connects with wrong ids get captured)
- [ ] try to implement a routing system in the svelte app that rerenders with the id but only for the main page

### generate

- [x] add redis installation to the setup documentation
- [x] secure redis
- [x] fix saving to redis

## license

parts of this code (specifically `generate/dnnlib/*`, `generate/torch_utils/*` & `generate/generators/image_generator.py`) are taken or derived from [stylegan3](https://github.com/NVlabs/stylegan3) by nvidia in accordance with the [nvidia source code license](https://github.com/NVlabs/stylegan3/blob/main/LICENSE.txt). nvidia's copyright applies there.

stylegan3 was autored by tero karras, miika aittala, samuli laine, erik harkonen, janne hellsten, jaakko Lehtinen and timo aila in 2021.

all other parts of this code are written by me and licensed under a [creative commons attribution-noncommercial-sharealike 4.0 international license](http://creativecommons.org/licenses/by-nc-sa/4.0/).

[![cc icon](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)
