# script for generating a chat with 2 or more writers
# text generation with one gpt2 model trained on dialogue
# selfie generation with one stylegan3 model per writer
#
# zeno gries 2022

from http.client import responses
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


# click parsers
def parse_comma_list(s: Union[str, List]) -> List[str]:
    if isinstance(s, list):
        return s

    return [item for item in map(str.strip, str(s).split(','))]


def parse_min_max(s: Union[str, List]) -> List[float]:
    if isinstance(s, list):
        return s

    return [float(factor) for factor in map(str.strip, str(s).split(','))]


# helper functions & classes
def get_wait_time(
        message: str,
        image: bool,
        base_time: float,
        letter_time: float,
        image_time: float,
        deviation: List[float]
    ) -> float:
    wait_time = base_time + len(message) * letter_time
    if image: wait_time += image_time
    wait_time *= random.uniform(deviation[0], deviation[1])
    return wait_time


class Sounds:
    def __init__(self, sound_paths: List[str]) -> None:
        self._sound_paths = sound_paths
        self._sound_paths_copy = []

    def get(self) -> str:
        # if the sound paths are empty
        # create a new copy and shuffle it
        if not self._sound_paths_copy:
            self._sound_paths_copy = self._sound_paths.copy()
            random.shuffle(self._sound_paths_copy)

        return self._sound_paths_copy.pop()


# yapf: disable
@click.command()
@click.option('--gpt_dir',         type=click.Path(exists=True), help='directory of gpt2 model', required=True)
@click.option('--temp',            type=float,                   default=0.7, help='temperature for gpt2 generation', required=True)
@click.option('--stylegan_dir',    type=click.Path(exists=True), help='directory of stylegan3 model file (formatted like this: \'folder/{{role}}_stylegan3_model.pkl\')', required=True)
@click.option('--sound_dir',       type=click.Path(exists=True), help='directory where the notification sounds are located', required=True)
@click.option('--prompt',          type=str,                     help='starting prompt', required=True)
@click.option('--role_format',     type=str,                     help='how a role is declared in the text (e.g. \'[{{role}}] \'). must include {{role}}/{{ROLE}}', required=True)
@click.option('--image_string',    type=str,                     help='how an image is declared in the text (e.g. [image])', required=True)
@click.option('--roles',           type=parse_comma_list,        help='list of roles (e.g \'artist, scientist\'). must be all lower case', required=True)
@click.option('--colors',          type=parse_comma_list,        help='colors for the roles in the terminal (should be the same count as roles)', required=True)
@click.option('--base_time',       type=float,                   default=3.0, help='minimum time for writing all types of messages', required=True)
@click.option('--letter_time',     type=float,                   default=0.2, help='time it takes to write one letter', required=True)
@click.option('--image_time',      type=float,                   default=6.0, help='time it takes to take an image', required=True)
@click.option('--write_deviation', type=parse_min_max,           default=[0.8, 1.2], help='minimun & maximum deviation of the time', required=True)
@click.option('--read_deviation',  type=parse_min_max,           default=[0.6, 1.4], help='minimun & maximum deviation of the time', required=True)
# yapf: enable
def generate(
        gpt_dir: str,
        temp: float,
        stylegan_dir: str,
        sound_dir: str,
        prompt: str,
        role_format: str,
        image_string: str,
        roles: List[str],
        colors: List[str],
        base_time: float,
        letter_time: float,
        image_time: float,
        write_deviation: List[float],
        read_deviation: List[float]
    ) -> None:
    """
    generates text messages with gpt2 & selfies with stylegan3.
    pushes these messages to a redis database
    """
    # setup redis database
    db = Database(host='localhost', db=0)

    # setup generators
    image_Gs = {}
    for role in roles:
        image_Gs[role] = ImageGenerator(
            os.path.join(stylegan_dir, f'{role}_stylegan3_model.pkl'),
            verbose=False
            )
    text_G = TextGenerator(model_folder=gpt_dir, verbose=False)

    # setup writing states
    writing_state = {}
    for role in roles:
        writing_state[role] = db.Hash(f'writing:{role}')
        writing_state[role].update(writer=role, state=0)

    # get all notification sound paths
    sounds = Sounds(glob.glob(os.path.join(sound_dir, '*')))

    # set image seed starting points
    image_seed = {}
    for role in roles:
        image_seed[role] = random.randint(
            0, 10000
            )  # make sure it is a random seed so it always starts at a different point

    # get regex patterns
    role_holder = role_format.split(r'{role}')
    split_pattern = re.compile(
        fr'(?={re.escape(role_holder[0])}\w+{re.escape(role_holder[1])})(?!{re.escape(image_string)})'
        )
    role_pattern = re.compile(
        fr'(?!{re.escape(image_string)}){re.escape(role_holder[0])}\w+{re.escape(role_holder[1])}'
        )
    sender_pattern = re.compile(
        fr'(?!{re.escape(image_string)}){re.escape(role_holder[0])}(?P<sender>\w+){re.escape(role_holder[1])}'
        )

    # main loop
    prompt = f'{prompt}\n'  # append newline to the prompt (TODO: make it work with launch.json)
    try:
        while True:
            # generate a message
            responses = text_G.generate(
                prompt, max_length=128, temperature=temp
                ).replace(prompt, '')
            # split the message so it only contains single responses in a list
            responses_list = [
                response.strip(
                    ' '
                    )  # strip any leading or trailing spaces (but not newlines)
                for response in re.split(split_pattern, responses)
                if re.search(role_pattern, response) is
                not None  # response must include a sender to be valid
                ]

            # only go on if there is a valid message
            if responses_list:
                prompt = responses_list[0]

                message_text = responses_list[0]

                # get sender
                sender = re.search(sender_pattern,
                                   message_text).group('sender').lower()
                # remove sender from message
                message_text = re.sub(role_pattern, '', message_text).strip()

    except KeyboardInterrupt:
        raise SystemExit


if __name__ == '__main__':
    generate()