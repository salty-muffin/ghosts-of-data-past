from typing import Union, List, Optional

import os
import re
import time
import random
import glob
import click
import shortuuid
from io import BytesIO
from walrus import Database
import climage
from termcolor import colored

from generators.image_generator import ImageGenerator
from generators.text_generator import TextGenerator

# constants
IMAGE_PLACEHOLDER = '[IMAGE]'  # should be cause for image generation & then removed
ROLE_PATTERN = r'\[.*:\]'  # used to find where messages begin and end
SENDER_PATTERN = r'\[|:\]'  # all characters to remove from sender
SENDER_STRING = '[{}:]'  # how is the sender to be formatted


# click parsers
def parse_comma_list(s: Union[str, List]) -> List[str]:
    if isinstance(s, list):
        return s

    return [item for item in map(str.strip, str(s).split(','))]


def parse_random_factor(s: Union[str, List]) -> List[float]:
    if isinstance(s, list):
        return s

    return [float(factor) for factor in map(str.strip, str(s).split(','))]


# yapf: disable
@click.command()
@click.option('--gptdir',       type=click.Path(exists=True),   help='directory of gpt2 model', required=True)
@click.option('--stylegandir',  type=click.Path(exists=True),   help='directory of stylegan3 model file (formatted like this: \'folder/{{role}}_stylegan3_model.pkl\')', required=True)
@click.option('--sounddir',     type=click.Path(exists=True),   help='directory where the notification sounds are located', required=True)
@click.option('--prompt',       type=str,                       help='starting prompt', required=True)
@click.option('--roles',        type=parse_comma_list,          help='list of roles (e.g \'artist, scientist\')', required=True)
@click.option('--colors',       type=parse_comma_list,          help='colors for the roles in the terminal (should be the same count as roles)', required=True)
@click.option('--basetime',     type=float,                     default=3.0, help='minimum time for writing all types of messages', required=True)
@click.option('--lettertime',   type=float,                     default=0.2, help='time it takes to write one letter', required=True)
@click.option('--imagetime',    type=float,                     default=6.0, help='time it takes to take an image', required=True)
@click.option('--readfactor',   type=float,                     default=0.8, help='how long should reading the message take in relation to writing it', required=True)
@click.option('--randomfactor', type=parse_random_factor,       default=[1.0, 1.0], help='minimun & maximum random factor to be applied to the time', required=True)
# yapf: enable
def generate(
        gptdir: str,
        stylegandir: str,
        sounddir: str,
        prompt: str,
        roles: List[str],
        colors: List[str],
        basetime: float,
        lettertime: float,
        imagetime: float,
        readfactor: float,
        randomfactor: List[float]
    ) -> None:
    # setup redis database
    db = Database(host='localhost', db=0)

    # setup generators
    image_Gs = {}
    for role in roles:
        image_Gs[role] = ImageGenerator(
            os.path.join(stylegandir, f'{role}_stylegan3_model.pkl'),
            verbose=False
            )
    text_G = TextGenerator(model_folder=gptdir, verbose=False)

    # setup writing states
    writing_state = {}
    for role in roles:
        writing_state[role] = db.Hash(f'writing:{role}')
        writing_state[role].update(writer=role, state=0)

    # get all notification sound paths in a list
    sound_paths = glob.glob(os.path.join(sounddir, '*'))

    # set variables
    image_seed = {}
    seed = 0
    for role in roles:
        image_seed[role] = seed
        seed += 100
    start = 0
    write_duration = 0
    sender = ''
    try:
        while True:
            # get the sender and set them to writing
            previous_sender = sender
            role_index = random.randint(0, len(roles) - 1)
            sender = roles[role_index]
            sender_readfactor = 0.2 if previous_sender == sender else 1

            # wait for the read duration
            wait_time = write_duration * readfactor * random.uniform(
                randomfactor[0], randomfactor[1]
                ) * sender_readfactor
            time.sleep(wait_time)

            writing_state[sender].update(writer=sender, state=1)

            # record start time
            start = start if start else time.time(
            )  # don't record starttime on repeat generation

            # get the response without the prompt
            prompt = f'{prompt}\n{SENDER_STRING.format(sender.upper())}'
            response = text_G.generate(
                prompt, max_length=128, temperature=0.7
                ).replace(prompt, '')

            # find the next messages
            matches = [match for match in re.finditer(ROLE_PATTERN, response)]

            # TODO optimize: use the whole response

            # only go on, if there are matches, else repeat
            image_string = ''
            if matches:
                # get message
                text = response[:matches[0].start()].strip()

                # get next prompt
                prompt = f'[{sender.upper()}:] {text}'

                # check for images
                image_data = b''
                alt = ''
                if IMAGE_PLACEHOLDER in text:
                    image = image_Gs[sender].generate(image_seed[sender])
                    # save image as binary
                    image_output = BytesIO()
                    image.save(
                        image_output,
                        "JPEG",
                        quality=70,
                        optimize=True,
                        progressive=True
                        )
                    image_data = image_output.getvalue()
                    image_string = climage.convert(image_output, width=40)

                    image_output.close()

                    alt = f'selfie of {sender}'

                    image_seed[sender] += 1

                    text = re.sub(
                        r'  +', ' ', text.replace(IMAGE_PLACEHOLDER, '')
                        ).strip()  # get rid of duplicate spaces

                # get a sound sound path and load it
                sound_path = sound_paths.pop(
                    random.randint(0, len(sound_paths) - 1)
                    )
                with open(sound_path, 'rb') as file:
                    sound_data = file.read()

                # relaod all sound effects if all of them have been used
                if (not sound_paths):
                    sound_paths = glob.glob(os.path.join(sounddir, '*'))

                # wait if message generation was shorter than minimum write_duration
                min_duration = basetime + len(text) * lettertime
                if image_data: min_duration += imagetime
                write_duration = time.time() - start
                write_duration *= random.uniform(
                    randomfactor[0], randomfactor[1]
                    )  # multiply by random factor
                start = 0

                wait_time = max(0, min_duration - write_duration)
                time.sleep(wait_time)

                # send message to redis
                message = db.Hash(shortuuid.uuid())
                message.update(
                    sender=sender,
                    text=text,
                    image_data=image_data,
                    alt=alt,
                    sound_data=sound_data
                    )
                message.expire(120)
                writing_state[sender].update(writer=sender, state=0)

                print(f'{sender}>', colored(text, colors[role_index]))
                if (image_string): print(image_string, end='')

    except KeyboardInterrupt:
        raise SystemExit


if __name__ == '__main__':
    generate()