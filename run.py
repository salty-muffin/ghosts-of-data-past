import os
import subprocess
import random
import string


def random_string(length: int) -> str:
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


if __name__ == '__main__':
    redis: subprocess.Popen = None
    link: subprocess.Popen = None
    serve: subprocess.Popen = None
    generate: subprocess.Popen = None

    try:
        gate = random_string(4)

        print(gate)

        subprocess.run(['npm', 'run', 'build'],
                       cwd='serve/site',
                       env=dict(os.environ, GATE=gate))
        subprocess.run(['npm', 'run', 'build'],
                       cwd='link/site',
                       env=dict(os.environ, GATE=gate))

        redis = subprocess.Popen(['redis-server', 'redis.conf'],
                                 env=dict(os.environ, GATE=gate))
        link = subprocess.Popen([
            'conda', 'run', '-n', 'ghosts-cpu', 'python3', 'link/app.py'
            ],
                                env=dict(os.environ, GATE=gate))
        serve = subprocess.Popen([
            'conda', 'run', '-n', 'ghosts-cpu', 'python3', 'serve/app.py'
            ],
                                 env=dict(os.environ, GATE=gate))
        generate = subprocess.Popen([
            'conda',
            'run',
            '-n',
            'ghosts-cpu',
            'python3',
            'generate/generate.py',
            ],
                                    env=dict(os.environ, GATE=gate))

        generate.wait()

    except:
        if redis: redis.terminate()
        if link: link.terminate()
        if serve: serve.terminate()
        if generate: generate.terminate()
