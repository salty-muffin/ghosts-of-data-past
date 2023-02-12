# for testing different models with a set of parameters
#
# zeno gries 2023

from typing import Union, List

import os
import json
import subprocess
import logging
import glob
import click
from datetime import datetime


# click parsers
def parse_comma_list_float(s: Union[str, List]) -> List[float]:
    if isinstance(s, list):
        return s

    return [float(item) for item in map(str.strip, str(s).split(','))]


# click parsers
def parse_comma_list_int(s: Union[str, List]) -> List[int]:
    if isinstance(s, list):
        return s

    return [int(item) for item in map(str.strip, str(s).split(','))]


# yapf: disable
@click.command()
@click.option('--runs', type=int, help='how many runs to do', required=True)
@click.option('--models_dir', type=click.Path(exists=True), help='the directory in which the models are found', required=True)
@click.option('--temps', type=parse_comma_list_float, help='temperature for gpt2 generation', required=True)
@click.option('--top_ks', type=parse_comma_list_int, help='if nonzero, limits the sampled tokens to the top k values', required=True)
@click.option('--top_ps', type=parse_comma_list_float, help='if nonzero, limits the sampled tokens to the cumulative probability', required=True)
@click.option('--verbose', is_flag=True, help='print additional information')
# yapf: enable
def test(
        runs: int,
        models_dir: str,
        temps: List[float],
        top_ks: List[float],
        top_ps: List[float],
        verbose: bool
    ) -> None:
    # setup logging
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(
                os.path.join(
                    'logs',
                    f'test_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log'
                    ),
                encoding='utf-8'
                ),
            logging.StreamHandler()
            ]
        )

    # declare popen objects, so they can be terminated in case of exception
    generate: subprocess.Popen = None

    # open json configuration file
    try:
        with open('conf.json') as file:
            conf = json.load(file)
    except Exception as ex:
        logging.error(f"could not open 'conf.json': {ex}")
        return

    # setup settings list
    settings = [
        # f'--delay={conf["delay"]}',  # how long to wait before starting (for documentation purposes)
        f'--delay=0',
        # f'--gpt_dir={conf["gpt_dir"]}',  # directory of gpt2 model
        # f'--temp={conf["temp"]}',  # temperature for gpt2 generation
        # f'--top_k={conf["top_k"]}',  # if nonzero, limits the sampled tokens to the top k values
        # f'--top_p={conf["top_p"]}',  # if nonzero, limits the sampled tokens to the cumulative probability
        f'--best_of={conf["best_of"]}',  # how many generations should be done at a time (if n > 1, the result will be selected randomly
        f'--stylegan_dir={conf["stylegan_dir"]}',  # directory of stylegan3 model file (formatted like this: 'folder/{{role}}_stylegan3_model.pkl')
        f'--sound_dir={conf["sound_dir"]}',  # directory where the notification sounds are located
        f'--prompts_file={conf["prompts_file"]}',  # path to json file with starting prompts
        f'--run_length={conf["run_length"]}',  # how long is an average conversation run, before the next prompt gets set. set to 0 to deactive
        f'--run_deviation={",".join(str(n) for n in conf["run_deviation"])}',  # minimun & maximum deviation of the conversation run length
        f'--role_format={conf["role_format"]}',  # how a role is declared in the text (e.g. '[{{role}}] '). must include {{role}}/{{ROLE}}
        f'--image_string={conf["image_string"]}',  # how an image is declared in the text (e.g. [image])
        f'--roles={",".join(str(n) for n in conf["roles"])}',  # list of roles (e.g 'artist, scientist'). must be all lower case
        f'--base_time={conf["base_time"]}',  # minimum time for writing all types of messages
        f'--letter_time={conf["letter_time"]}',  # time it takes to write one letter
        f'--image_time={conf["image_time"]}',  # time it takes to take an image
        f'--run_time={conf["run_time"]}',  # time to wait between runs
        f'--write_deviation={",".join(str(n) for n in conf["write_deviation"])}',  # minimun & maximum deviation of the write time
        f'--read_deviation={",".join(str(n) for n in conf["read_deviation"])}',  # minimun & maximum deviation of the read time
        f'--runs={runs}',
        f'--memory={conf["memory"]}',
        '--rapid',  # '--verbose'
        ]

    if verbose:
        settings.append('--verbose')

    # get all models
    model_dirs = sorted(glob.glob(os.path.join(models_dir, '*')))
    if os.path.join(models_dir, 'old') in model_dirs:
        model_dirs.remove(os.path.join(models_dir, 'old'))

    try:
        for dir in model_dirs:
            for temp in temps:
                for top_k in top_ks:
                    for top_p in top_ps:
                        logging.info(
                            f'starting generation with {dir}, temp {temp}, top_k: {top_k}, top_p: {top_p}'
                            )
                        generate = subprocess.Popen([
                            'conda',
                            'run',
                            '-n',
                            'ghosts-cpu',
                            'python3',
                            os.path.join('generate', 'generate.py'),
                            f'--logfile={os.path.split(dir)[-1]}'
                            f'--gpt_dir={dir}',
                            f'--temp={temp}',
                            f'--top_k={top_k}',
                            f'--top_p={top_p}',
                            *settings,
                            ])

                        generate.wait()

    except Exception as ex:
        logging.error(f'program terminated due to error: {ex}')
    except KeyboardInterrupt:
        logging.info('program terminated by user')
    finally:
        logging.info('exiting...')
        # in case of any exception (including KeyboardInterrupt) terminate all processes
        if generate:
            generate.terminate()
            generate.wait()


if __name__ == '__main__':
    test()