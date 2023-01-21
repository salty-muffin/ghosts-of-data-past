import os
import json
import time
import subprocess
import random
import string
import argparse
import logging
from datetime import datetime


def random_string(length: int) -> str:
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def main() -> None:
    # setup logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    os.makedirs('logs', exist_ok=True)

    sh = logging.StreamHandler()
    fh = logging.FileHandler(
        os.path.join(
            'logs', f'run_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log'
            ),
        encoding='utf-8'
        )

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )

    sh.setFormatter(formatter)
    sh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)

    logger.addHandler(sh)
    logger.addHandler(fh)

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('domain')
    args = parser.parse_args()

    # declare popen objects, so they can be terminated in case of exception
    redis: subprocess.Popen = None
    link: subprocess.Popen = None
    serve: subprocess.Popen = None
    generate: subprocess.Popen = None
    browser: subprocess.Popen = None

    # set gate (access code) and domain to later be used as environment variables
    gate = random_string(4)
    domain = args.domain
    logger.info(f'the gate is: {gate}')
    logger.info(f'the domain is: {domain}')

    # open json configuration file
    try:
        with open('conf.json') as file:
            conf = json.load(file)
    except Exception as ex:
        logger.error(f"could not open 'conf.json': {ex}")
        return

    # setup settings list
    settings = [
        f'--delay={conf["delay"]}',  # how long to wait before starting (for documentation purposes)
        f'--gpt_dir={conf["gpt_dir"]}',  # directory of gpt2 model
        f'--temp={conf["temp"]}',  # temperature for gpt2 generation
        f'--top_k={conf["top_k"]}',  # if nonzero, limits the sampled tokens to the top k values
        f'--top_p={conf["top_p"]}',  # if nonzero, limits the sampled tokens to the cumulative probability
        f'--best_of={conf["best_of"]}',  # how many generations should be done at a time (if n > 1, the result will be selected randomly
        f'--stylegan_dir={conf["stylegan_dir"]}',  # directory of stylegan3 model file (formatted like this: 'folder/{{role}}_stylegan3_model.pkl')
        f'--sound_dir={conf["sound_dir"]}',  # directory where the notification sounds are located
        f'--prompts_file={conf["prompts_file"]}',  # path to json file with starting prompts
        f'--run_length={conf["run_length"]}',  # how long is an average conversation run, before the next prompt gets set. set top 0 to deactive
        f'--run_deviation={",".join(str(n) for n in conf["run_deviation"])}',  # minimun & maximum deviation of the conversation run length
        f'--role_format={conf["role_format"]}',  # how a role is declared in the text (e.g. '[{{role}}] '). must include {{role}}/{{ROLE}}
        f'--image_string={conf["image_string"]}',  # how an image is declared in the text (e.g. [image])
        f'--roles={",".join(str(n) for n in conf["roles"])}',  # list of roles (e.g 'artist, scientist'). must be all lower case
        f'--colors={",".join(str(n) for n in conf["colors"])}',  # colors for the roles in the terminal (should be the same count as roles)
        f'--base_time={conf["base_time"]}',  # minimum time for writing all types of messages
        f'--letter_time={conf["letter_time"]}',  # time it takes to write one letter
        f'--image_time={conf["image_time"]}',  # time it takes to take an image
        f'--run_time={conf["run_time"]}',  # time to wait between runs
        f'--write_deviation={",".join(str(n) for n in conf["write_deviation"])}',  # minimun & maximum deviation of the write time
        f'--read_deviation={",".join(str(n) for n in conf["read_deviation"])}',  # minimun & maximum deviation of the read time
        '--rapid' if conf["rapid"] else None,  # skip all wait times
        '--verbose'
        if conf["verbose"] else None  # print additional information
        ]
    # filter out none
    settings = list(filter(lambda setting: setting is not None, settings))

    try:
        logger.info('building the link site...')
        subprocess.run(['npm', 'run', 'build'],
                       cwd=os.path.join('link', 'site'),
                       env=dict(os.environ, GATE=gate, DOMAIN=domain))

        logger.info('building the serve site...')
        subprocess.run(['npm', 'run', 'build'],
                       cwd=os.path.join('serve', 'site'))

        logger.info('starting redis...')
        redis = subprocess.Popen(['redis-server', 'redis.conf'])

        logger.info('starting link server...')
        link = subprocess.Popen([
            'conda',
            'run',
            '-n',
            'ghosts-cpu',
            'python3',
            os.path.join('link', 'app.py')
            ])

        logger.info('starting site server...')
        serve = subprocess.Popen([
            'conda',
            'run',
            '-n',
            'ghosts-cpu',
            'python3',
            os.path.join('serve', 'app.py')
            ],
                                 env=dict(os.environ, GATE=gate))

        logger.info('starting browser in 5 sec...')
        time.sleep(5)
        browser = subprocess.Popen([
            'chromium', '--start-fullscreen', 'http://localhost:8000'
            ])

        logger.info('starting generation...')
        generate = subprocess.Popen([
            'conda',
            'run',
            '-n',
            'ghosts-cpu',
            'python3',
            os.path.join('generate', 'generate.py'),
            # '--verbose',
            *settings
            ])

        serve.wait()

    except Exception as ex:
        logger.error(f'program terminated due to error: {ex}')
    except KeyboardInterrupt:
        logger.info('program terminated by user')
    finally:
        logger.info('exiting...')
        # in case of any exception (including KeyboardInterrupt) terminate all processes
        if redis: redis.terminate()
        if link: link.terminate()
        if serve: serve.terminate()
        if generate: generate.terminate()
        if browser: browser.terminate()


if __name__ == '__main__':
    main()