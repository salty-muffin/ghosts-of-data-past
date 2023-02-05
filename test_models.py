from typing import Dict

import os
import json
import subprocess
import logging
import glob
from datetime import datetime


def main() -> None:
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
        f'--delay={conf["delay"]}',  # how long to wait before starting (for documentation purposes)
        # f'--gpt_dir={conf["gpt_dir"]}',  # directory of gpt2 model
        f'--temp={conf["temp"]}',  # temperature for gpt2 generation
        f'--top_k={conf["top_k"]}',  # if nonzero, limits the sampled tokens to the top k values
        f'--top_p={conf["top_p"]}',  # if nonzero, limits the sampled tokens to the cumulative probability
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
        f'--runs=3',
        f'--memory={conf["memory"]}',
        '--rapid',  # '--verbose'
        ]

    # get all models
    model_dirs = sorted(glob.glob('test_models/*'))
    model_dirs.remove('test_models/old')

    try:
        for dir in model_dirs:
            logging.info(f'starting generation with {dir}')
            generate = subprocess.Popen([
                'conda',
                'run',
                '-n',
                'ghosts',
                'python3',
                os.path.join('generate', 'generate.py'),
                f'--gpt_dir={dir}',
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
    main()