# script for generating a chat with 2 or more writers
# text generation with one gpt2 model trained on dialogue
# selfie generation with one stylegan3 model per writer
#
# zeno gries 2023

from typing import Union, List, Dict
from queue import Queue
from PIL.Image import Image

import os
import multiprocessing
import queue
import re
import time
import random
import glob
import click
import json
import shortuuid
import logging
from datetime import datetime
from io import BytesIO
from walrus import Database, Hash

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
        self._prompts = prompts
        self._prompts_copy = []

    def get(self) -> str:
        # if the prompts are empty
        # create a new copy and shuffle it
        if not self._prompts_copy:
            self._prompts_copy = self._prompts.copy()
            random.shuffle(self._prompts_copy)

        return self._prompts_copy.pop()


def generate_images(
        stylegan_dir, logger: logging.Logger, **queues: Queue
    ) -> None:
    # setup image generators
    image_Gs: Dict[str, ImageGenerator] = {}
    for role in queues:
        image_Gs[role] = ImageGenerator(
            logger, os.path.join(stylegan_dir, f'{role}_stylegan3_model.pkl')
            )

    # set image seed starting points
    image_seed = {}
    for role in queues:
        image_seed[role] = random.randint(
            0, 10000
            )  # make sure it is a random seed so it always starts at a different point
    logger.debug(f'setup image seeds: {image_seed}')

    # generate images
    while True:
        for role, _queue in queues.items():
            if _queue.qsize() < 3:
                logger.debug(
                    f"generating image for '{role}' with seed: {image_seed[role]}"
                    )
                _queue.put(image_Gs[role].generate(image_seed[role]))
                image_seed[role] += 1
        time.sleep(1)


# yapf: disable
@click.command()
@click.option('--delay',            type=float, default=0,                         help='how long to wait before starting (for documentation purposes)', required=True)
@click.option('--gpt_dir',          type=click.Path(exists=True, file_okay=False), help='directory of gpt2 model', required=True)
@click.option('--temp',             type=float, default=0.7,                       help='temperature for gpt2 generation', required=True)
@click.option('--top_k',            type=int, default=0,                           help='if nonzero, limits the sampled tokens to the top k values', required=True)
@click.option('--top_p',            type=float, default=0.7,                       help='if nonzero, limits the sampled tokens to the cumulative probability', required=True)
@click.option('--best_of',          type=int, default=1,                           help='how many generations should be done at a time (if n > 1, the result will be selected randomly', required=True)
@click.option('--stylegan_dir',     type=click.Path(exists=True, file_okay=False), help='directory of stylegan3 model file (formatted like this: \'folder/{{role}}_stylegan3_model.pkl\')', required=True)
@click.option('--sound_dir',        type=click.Path(exists=True, file_okay=False), help='directory where the notification sounds are located', required=True)
@click.option('--prompts_file',     type=click.Path(exists=True, dir_okay=False),  help='path to json file with starting prompts', required=True)
@click.option('--run_length',       type=int, default=50,                          help='how long is an average conversation run, before the next prompt gets set. set to 0 to deactive', required=True)
@click.option('--run_deviation',    type=parse_min_max, default=[0.75, 1.25],      help='minimun & maximum deviation of the conversation run length', required=True)
@click.option('--role_format',      type=str,                                      help='how a role is declared in the text (e.g. \'[{{role}}] \'). must include {{role}}/{{ROLE}}', required=True)
@click.option('--image_string',     type=str,                                      help='how an image is declared in the text (e.g. [image])', required=True)
@click.option('--roles',            type=parse_comma_list,                         help='list of roles (e.g \'artist, scientist\'). must be all lower case', required=True)
@click.option('--base_time',        type=float, default=3.0,                       help='minimum time for writing all types of messages', required=True)
@click.option('--letter_time',      type=float, default=0.2,                       help='time it takes to write one letter', required=True)
@click.option('--image_time',       type=float, default=6.0,                       help='time it takes to take an image', required=True)
@click.option('--run_time',         type=float, default=10.0,                      help='time to wait between runs', required=True)
@click.option('--write_deviation',  type=parse_min_max, default=[0.8, 1.2],        help='minimun & maximum deviation of the write time', required=True)
@click.option('--read_deviation',   type=parse_min_max, default=[0.6, 1.4],        help='minimun & maximum deviation of the read time', required=True)
@click.option('--runs',             type=int, default=0,                           help='how many runs to do (infinite, if zero)', required=True)
@click.option('--memory',           type=int, default=1,                           help='how many generated messages get used for the prompt (e.g. the last 2)', required=True)
@click.option('--logfile',          type=str, default='generate',                  help='name of the logfile (creation time gets added at the end)', required=True)
@click.option('--rapid',            is_flag=True,                                  help='skip all wait times')
@click.option('--verbose',          is_flag=True,                                  help='print additional information')
@click.option('--out_dir',          type=click.Path(file_okay=False),              help='directory to generate the conversation to (messages in a .json file and images as .jpgs)', required=False)
@click.option('--conversation_dir', type=click.Path(file_okay=False, exists=True), help='directory to generate the conversation from (from previous generation)', required=False)
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
        base_time: float,
        letter_time: float,
        image_time: float,
        run_time: float,
        write_deviation: List[float],
        read_deviation: List[float],
        runs: int,
        memory: int,
        logfile: str,
        rapid: bool,
        verbose: bool,
        out_dir: str = None,
        conversation_dir: str = None
    ) -> None:
    """
    generates text messages with gpt2 & selfies with stylegan3.
    pushes these messages to a redis database
    """

    remaining_runs = runs

    # setup logging
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(
                os.path.join(
                    'logs',
                    f'{logfile}_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log'
                    ),
                encoding='utf-8'
                ),
            logging.StreamHandler()
            ]
        )
    logger = logging.getLogger(__name__)

    # print out all command line arguments
    logger.info(f'delay: {delay}')
    logger.info(f'gpt_dir: {gpt_dir}')
    logger.info(f'temp: {temp}')
    logger.info(f'top_k: {top_k}')
    logger.info(f'top_p: {top_p}')
    logger.info(f'best_of: {best_of}')
    logger.info(f'stylegan_dir: {stylegan_dir}')
    logger.info(f'sound_dir: {sound_dir}')
    logger.info(f'prompts_file: {prompts_file}')
    logger.info(f'run_length: {run_length}')
    logger.info(f'run_deviation: {run_deviation}')
    logger.info(f'role_format: {role_format}')
    logger.info(f'image_string: {image_string}')
    logger.info(f'roles: {roles}')
    logger.info(f'base_time: {base_time}')
    logger.info(f'letter_time: {letter_time}')
    logger.info(f'image_time: {image_time}')
    logger.info(f'run_time: {run_time}')
    logger.info(f'write_deviation: {write_deviation}')
    logger.info(f'read_deviation: {read_deviation}')
    logger.info(f'runs: {runs}')
    logger.info(f'memory: {memory}')
    logger.info(f'rapid: {rapid}')
    logger.info(f'verbose: {verbose}')

    # setup redis database
    db = Database(host='localhost', db=0)

    # prepare generation to file
    messages = []
    image_counter = 0
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # prepare generation from file
    loaded_messages: List[Dict[str, Union[str, bool]]] = []
    message_count = 1
    if conversation_dir:
        with open(os.path.join(conversation_dir, 'messages.json')) as file:
            loaded_messages = json.load(file)

    try:
        if not conversation_dir:
            # setup queues
            queues: Dict[str, Queue] = {}
            for role in roles:
                queues[role] = multiprocessing.Queue()

            # start image generation process
            process = multiprocessing.Process(
                target=generate_images,
                kwargs=({
                    'logger': logger, 'stylegan_dir': stylegan_dir, **queues
                    })
                )
            process.start()
            logger.info('setup image generators.')

            # setup text generators
            text_G = TextGenerator(logger, model_folder=gpt_dir)
            logger.info('setup text generator.')
        else:
            process = None

        # setup writing states
        writing_state: Dict[str, Hash] = {}
        for role in roles:
            writing_state[role] = db.Hash(f'writing:{role}')
            writing_state[role].update(writer=role, state=0)
        logger.info('setup writing states.')

        # get all notification sound paths
        sounds = Sounds(glob.glob(os.path.join(sound_dir, '*')))
        logger.info('setup sounds')

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
        prompt = [prompts.get()]
        logger.info(f'setup prompts. first prompt: {prompt[0]}')

        # setup run
        current_run_length = int(
            run_length * random.uniform(run_deviation[0], run_deviation[1])
            )
        logger.info(f'setup run length: {current_run_length}')

        last_message = {
            'sender': re.search(sender_pattern,
                                prompt[0]).group('sender').lower(),
            'text': re.sub(role_pattern, '', prompt[0]).strip(),
            'image_data': b'',
            'alt': b'',
            'sound_data': sounds.get(),
            'new_run': False,
            'image_path': ''
            }
        if conversation_dir:
            last_message = {
                'sender': loaded_messages[0]['sender'],
                'text': loaded_messages[0]['text'],
                'image_data': b'',
                'alt': b'',
                'sound_data': sounds.get(),
                'new_run': False,
                'image_path': ''
                }
        last_sender = last_message['sender']
        logger.info(
            f'first message (this should be the prompt): {last_message["sender"]}> {last_message["text"]} [image: {bool(last_message["image_data"])}]'
            )

        # set variables
        start = 0
        new_run = False

        time.sleep(delay)

        # - main loop --------------------------------------------------------------------------------
        while message_count < len(loaded_messages) or not loaded_messages:
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
            logger.debug(f'waiting for readtime: {read_time}')
            if not rapid: time.sleep(read_time)

            # if it is a new run, wait the run_time
            if last_message['new_run']:
                logger.info(
                    f'conversation run ended. new prompt: {responses_list[0]}. new run length: {current_run_length}.'
                    )

                if not rapid: time.sleep(run_time)

            # set sender of last message (next message in the queue) to writing
            writing_state[last_message['sender']
                          ].update(writer=last_message['sender'], state=1)
            logger.debug(f'set writing: {last_message["sender"]}')

            # record generation start time
            start = start if start else time.time(
            )  # don't record starttime on repeat generation

            # generate a message
            if not conversation_dir:
                if not current_run_length <= 0 or run_length == 0:
                    current_prompt = '\n'.join([
                        line.strip() for line in prompt
                        ]) + '\n'
                    responses = text_G.generate(
                        current_prompt,
                        max_length=128,
                        temperature=temp,
                        top_k=top_k,
                        top_p=top_p,
                        n=best_of,  # batch_size=best_of
                        ).replace(current_prompt, '')
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

                    # stop if designated runs are reached
                    if runs:
                        remaining_runs -= 1
                        if remaining_runs <= 0:
                            raise SystemExit

                # if not proper responses were generated, start with new prompt
                if not responses_list:
                    responses_list = [prompts.get()]
                    current_run_length = int(
                        run_length
                        * random.uniform(run_deviation[0], run_deviation[1])
                        )
                    new_run = True

                    logger.warning(
                        f'no valid messages. starting new run. new prompt: {responses_list[0]}. new run length: {current_run_length}. The new run will appear one line later in the log.'
                        )
                # get sender
                sender = re.search(sender_pattern,
                                   responses_list[0]).group('sender').lower()

                # remove sender from message
                text = re.sub(role_pattern, '', responses_list[0]).strip()
            else:
                sender = loaded_messages[message_count]['sender']
                text = loaded_messages[message_count]['text']

                if 'new_run' in loaded_messages[message_count].keys():
                    new_run = True

            # only go on, if sender is valid & and there is text
            if sender in roles and text or conversation_dir:
                # is there an image
                image_data = b''
                image_path = ''
                alt = ''

                if not conversation_dir:
                    # get prompt for the next generation
                    prompt.append(responses_list[0])
                    if len(prompt) > memory:
                        prompt.pop(0)

                    if image_string in text:
                        # get image from queue
                        image: Image = None
                        while image is None:
                            try:
                                image = queues[sender].get()
                            except queue.Empty:
                                logger.warning(
                                    f"queue for '{sender}' is empty. trying again in 1 second."
                                    )
                                time.sleep(1)

                        # save image as binary
                        image_output = BytesIO()
                        image.save(
                            image_output,
                            'JPEG',
                            quality=70,
                            optimize=True,
                            progressive=True
                            )

                        # save image to file, if outdir is set
                        if out_dir:
                            image_path = f'image_{str(image_counter).zfill(10)}.jpg'
                            image.save(
                                os.path.join(out_dir, image_path),
                                'JPEG',
                                quality=70,
                                optimize=True,
                                progressive=True
                                )
                            image_counter += 1

                        image_data = image_output.getvalue()

                        image_output.close()

                        # get image alt
                        alt = f'selfie of {sender}'

                        # remove image placeholder string from message text
                        text = re.sub(
                            r'  +', ' ', text.replace(image_string, '')
                            ).strip()  # get rid of duplicate spaces
                else:
                    if 'image_path' in loaded_messages[message_count].keys():
                        with open(
                            os.path.join(
                                conversation_dir,
                                loaded_messages[message_count]['image_path']
                                ),
                            'rb'
                            ) as file:
                            image_data = file.read()

                        # get image alt
                        alt = f'selfie of {sender}'

                    message_count += 1

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
                logger.debug(f'waiting for writetime: {write_time}')
                if not rapid: time.sleep(write_time)

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

                # write message to file, if out_dir is set
                if out_dir:
                    new_message = {
                        'sender': last_message['sender'],
                        'text': last_message['text'],
                        }
                    if last_message['image_path']:
                        new_message['image_path'] = last_message['image_path']
                    if last_message['new_run']:
                        new_message['new_run'] = last_message['new_run']
                    messages.append(new_message)
                    with open(
                        os.path.join(out_dir, 'messages.json'), "w+"
                        ) as file:
                        json.dump(messages, file)

                current_run_length -= 1

                # print the message to terminal
                logger.info(
                    f'{last_message["sender"]}> {last_message["text"]} [image: {bool(last_message["image_data"])}]'
                    )

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
                    'new_run': new_run,
                    'image_path': image_path
                    }
                new_run = False
                logger.debug(
                    f'generated message: {last_message["sender"]}> {last_message["text"]} [image: {bool(last_message["image_data"])}]'
                    )

            else:
                logger.warning('invalid sender or text')

    except Exception as ex:
        logger.error(f'terminated because of error: {ex}')
    except KeyboardInterrupt:
        logger.info('process ended by user')
    finally:
        logger.info('terminating subprocesses and closing queues...')
        if process: process.terminate()
        if process: process.join()
        for _queue in queues.values():
            if _queue: _queue.close()
            if _queue: _queue.join_thread()


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    generate()