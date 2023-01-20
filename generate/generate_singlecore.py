# script for generating a chat with 2 or more writers
# text generation with one gpt2 model trained on dialogue
# selfie generation with one stylegan3 model per writer
#
# zeno gries 2023

from http.client import responses
from typing import Union, List, Optional

import os
import re
import time
import random
import glob
import click
import json
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


def print_v(verbose: bool, message: str) -> None:
    if verbose: print(message)


class Sounds:
    def __init__(self, sound_paths: List[str]) -> None:
        self._sound_paths = sound_paths
        self._sound_paths_copy = []

    def get(self) -> bytes:
        # if the sound paths are empty
        # create a new copy and shuffle it
        if not self._sound_paths_copy:
            self._sound_paths_copy = self._sound_paths.copy()
            random.shuffle(self._sound_paths_copy)

        with open(self._sound_paths_copy.pop(), 'rb') as file:
            sound_data = file.read()

        return sound_data


class Prompts:
    def __init__(self, prompts: List[str]) -> None:
        self._prompts = [
            f'{prompt}\n' for prompt in prompts
            ]  # append newline to each prompt
        self._prompts_copy = []

    def get(self) -> str:
        # if the prompts are empty
        # create a new copy and shuffle it
        if not self._prompts_copy:
            self._prompts_copy = self._prompts.copy()
            random.shuffle(self._prompts_copy)

        return self._prompts_copy.pop()


# yapf: disable
@click.command()
@click.option('--delay',           type=float,                   default=0, help='how long to wait before starting (for documentation purposes)', required=True)
@click.option('--gpt_dir',         type=click.Path(exists=True), help='directory of gpt2 model', required=True)
@click.option('--temp',            type=float,                   default=0.7, help='temperature for gpt2 generation', required=True)
@click.option('--top_k',           type=int,                     default=0, help='if nonzero, limits the sampled tokens to the top k values', required=True)
@click.option('--top_p',           type=float,                   default=0.7, help='if nonzero, limits the sampled tokens to the cumulative probability', required=True)
@click.option('--best_of',         type=int,                     default=1, help='how many generations should be done at a time (if n > 1, the result will be selected randomly', required=True)
@click.option('--stylegan_dir',    type=click.Path(exists=True), help='directory of stylegan3 model file (formatted like this: \'folder/{{role}}_stylegan3_model.pkl\')', required=True)
@click.option('--sound_dir',       type=click.Path(exists=True), help='directory where the notification sounds are located', required=True)
@click.option('--prompts_file',    type=click.Path(exists=True), help='path to json file with starting prompts', required=True)
@click.option('--run_length',      type=int,                     default=50, help='how long is an average conversation run, before the next prompt gets set. set top 0 to deactive', required=True)
@click.option('--run_deviation',   type=parse_min_max,           default=[0.75, 1.25], help='minimun & maximum deviation of the conversation run length', required=True)
@click.option('--role_format',     type=str,                     help='how a role is declared in the text (e.g. \'[{{role}}] \'). must include {{role}}/{{ROLE}}', required=True)
@click.option('--image_string',    type=str,                     help='how an image is declared in the text (e.g. [image])', required=True)
@click.option('--roles',           type=parse_comma_list,        help='list of roles (e.g \'artist, scientist\'). must be all lower case', required=True)
@click.option('--colors',          type=parse_comma_list,        help='colors for the roles in the terminal (should be the same count as roles)', required=True)
@click.option('--base_time',       type=float,                   default=3.0, help='minimum time for writing all types of messages', required=True)
@click.option('--letter_time',     type=float,                   default=0.2, help='time it takes to write one letter', required=True)
@click.option('--image_time',      type=float,                   default=6.0, help='time it takes to take an image', required=True)
@click.option('--run_time',        type=float,                   default=10.0, help='time to wait between runs', required=True)
@click.option('--write_deviation', type=parse_min_max,           default=[0.8, 1.2], help='minimun & maximum deviation of the write time', required=True)
@click.option('--read_deviation',  type=parse_min_max,           default=[0.6, 1.4], help='minimun & maximum deviation of the read time', required=True)
@click.option('--rapid',           is_flag=True,                 help='skip all wait times')
@click.option('--verbose',         is_flag=True,                 help='print additional information')
# yapf: enable
def generate(
        delay: int,
        gpt_dir: str,
        temp: float,
        top_k: int,
        top_p: float,
        best_of: int,
        stylegan_dir: str,
        sound_dir: str,
        prompts_file: str,
        run_length: int,
        run_deviation: List[float],
        role_format: str,
        image_string: str,
        roles: List[str],
        colors: List[str],
        base_time: float,
        letter_time: float,
        image_time: float,
        run_time: float,
        write_deviation: List[float],
        read_deviation: List[float],
        rapid: bool,
        verbose: bool
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
            verbose=verbose
            )
    text_G = TextGenerator(model_folder=gpt_dir, verbose=verbose)
    print_v(verbose, 'setup generators.')

    # setup writing states
    writing_state = {}
    for role in roles:
        writing_state[role] = db.Hash(f'writing:{role}')
        writing_state[role].update(writer=role, state=0)
    print_v(verbose, 'setup writing states.')

    # get all notification sound paths
    sounds = Sounds(glob.glob(os.path.join(sound_dir, '*')))
    print_v(verbose, 'setup sounds')

    # set image seed starting points
    image_seed = {}
    for role in roles:
        image_seed[role] = random.randint(
            0, 10000
            )  # make sure it is a random seed so it always starts at a different point
    print_v(verbose, f'setup image seeds: {image_seed}')

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

    # setup prompts
    with open(prompts_file) as file:
        prompts_list = json.load(file)
    prompts = Prompts(prompts_list)
    prompt = prompts.get()
    print_v(verbose, f'setup prompts. first prompt: {prompt}')

    # setup run
    current_run_length = int(
        run_length * random.uniform(run_deviation[0], run_deviation[1])
        )
    print_v(verbose, f'setup run length: {current_run_length}')

    last_message = {
        'sender': re.search(sender_pattern, prompt).group('sender').lower(),
        'text': re.sub(role_pattern, '', prompt).strip(),
        'image_data': b'',
        'alt': b'',
        'sound_data': sounds.get(),
        'image_terminal': '',
        'new_run': False
        }
    last_sender = last_message['sender']
    print_v(
        verbose,
        f'generated first message (this should be the prompt): {last_message["sender"]}> {last_message["text"]} image: {bool(last_message["image_data"])}'
        )

    # set variables
    start = 0
    new_run = False

    time.sleep(delay)

    # - main loop --------------------------------------------------------------------------------
    try:
        while True:
            # wait according to last message (next message in the queue) (reading), but only if the sender changed from the last one
            if last_sender != last_message['sender']:
                read_time = get_wait_time(
                    last_message['text'],
                    bool(last_message['image_data']),
                    base_time,
                    letter_time,
                    image_time,
                    read_deviation
                    )
            else:
                # if it is the same sender as last time only wait for a short time
                read_time = get_wait_time('', False, 1, 0, 0, [1.0, 2.5])
            last_sender = last_message['sender']
            print_v(verbose, f'waiting for readtime: {read_time}')
            if not rapid: time.sleep(read_time)

            if not verbose: print(f'{last_message["sender"]}> ', end='')

            # set sender of last message (next message in the queue) to writing
            writing_state[last_message['sender']
                          ].update(writer=last_message['sender'], state=1)
            print_v(verbose, f'set writing: {last_message["sender"]}')

            # record generation start time
            start = start if start else time.time(
            )  # don't record starttime on repeat generation

            # generate a message
            if not current_run_length <= 0 or run_length == 0:
                responses = text_G.generate(
                    prompt,
                    max_length=128,
                    temperature=temp,
                    top_k=top_k,
                    top_p=top_p,
                    n=best_of
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
            else:
                # if conversation run is at an end, get a new prompt from command line parameters
                responses_list = [prompts.get()]
                current_run_length = int(
                    run_length
                    * random.uniform(run_deviation[0], run_deviation[1])
                    )
                new_run = True
                print_v(
                    verbose,
                    f'conversation run ended. new prompt: {prompt}. new run length: {current_run_length}'
                    )

            # if not proper responses were generated, start with new prompt
            if not responses_list:
                responses_list = [prompts.get()]
                current_run_length = int(
                    run_length
                    * random.uniform(run_deviation[0], run_deviation[1])
                    )
                new_run = True
                print_v(
                    verbose,
                    f'conversation run ended. new prompt: {prompt}. new run length: {current_run_length}'
                    )
            # get sender
            sender = re.search(sender_pattern,
                               responses_list[0]).group('sender').lower()

            # only go on, if sender is valid
            if sender in roles:
                # remove sender from message
                text = re.sub(role_pattern, '', responses_list[0]).strip()

                # get promt for the next generation
                prompt = responses_list[0]

                # is there an image
                image_data = b''
                alt = ''
                image_terminal = ''
                if image_string in text:
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
                    image_terminal = climage.convert(image_output, width=40)

                    image_output.close()

                    image_seed[sender] += 1

                    # get image alt
                    alt = f'selfie of {sender}'

                    # remove image placeholder string from message text
                    text = re.sub(r'  +', ' ', text.replace(image_string, '')
                                  ).strip()  # get rid of duplicate spaces

                # wait according to last message (writing)
                write_duration = time.time() - start
                start = 0
                write_time = max(
                    0,
                    get_wait_time(
                        last_message['text'],
                        bool(last_message['image_data']),
                        base_time,
                        letter_time,
                        image_time,
                        write_deviation
                        ) -
                    write_duration  # subtract the the time the generation took from the time this writing should take
                    )
                print_v(verbose, f'waiting for writetime: {write_time}')
                if not rapid: time.sleep(write_time)

                # if it is a new run, wait the run_time
                if last_message['new_run'] and not rapid:
                    time.sleep(run_time)

                # push the last generated message to the database
                message = db.Hash(shortuuid.uuid())
                message.update(
                    sender=last_message['sender'],
                    text=last_message['text'],
                    image_data=last_message['image_data'],
                    alt=last_message['alt'],
                    sound_data=last_message['sound_data']
                    )
                message.expire(120)
                # unset the writing state
                writing_state[sender].update(
                    writer=last_message['sender'], state=0
                    )

                current_run_length -= 1

                # print the message to terminal
                if verbose: print(f'{last_message["sender"]}> ', end='')
                print(
                    colored(
                        last_message['text'],
                        colors[roles.index(last_message["sender"])]
                        )
                    )
                if (last_message['image_terminal']):
                    print(last_message['image_terminal'], end='')

                # save massage to be sent after next generation. it is necessary
                # to send this message only after the next was generated, because
                # the sender is not known before generation, thus the writing state
                # cannot be set before generation.
                last_message = {
                    'sender': sender,
                    'text': text,
                    'image_data': image_data,
                    'alt': alt,
                    'sound_data': sounds.get(),
                    'image_terminal': image_terminal,
                    'new_run': new_run
                    }
                new_run = False
                print_v(
                    verbose,
                    f'generated message: {last_message["sender"]}> {last_message["text"]} image: {bool(last_message["image_data"])}'
                    )

    except KeyboardInterrupt:
        raise SystemExit


if __name__ == '__main__':
    generate()