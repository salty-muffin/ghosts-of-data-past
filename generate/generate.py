import os
import re
import time
from io import BytesIO

from generators.image_generator import ImageGenerator
from generators.text_generator import TextGenerator


def generate() -> None:
    # setup generators
    image_Gs = {
        'artist':
        ImageGenerator(
            os.path.join('generate', 'models', 'artist_stylegan3_model.pkl')
            ),
        'scientist':
        ImageGenerator(
            os.path.join('generate', 'models', 'artist_stylegan3_model.pkl')
            )
        }
    text_G = TextGenerator(
        model_folder=os.path.join('generate', 'models', 'gpt2_model')
        )

    prompt = '[SCIENTIST:] I can\'t believe you.'
    image_seed = {'artist': 0, 'scientist': 0}
    start = 0
    try:
        while True:
            start = start if start else time.time(
            )  # don't record starttime on repeat generation

            # get the response without the prompt
            response = text_G.generate(
                prompt, max_length=128, temperature=0.7
                ).replace(prompt, '')

            # find the next messages
            matches = [match for match in re.finditer(r'\[.*:\]', response)]

            # TODO optimize: use the whole response
            # only go on, if there are matches, else repeat
            if matches:
                # get sender
                sender = re.sub(
                    r'\[|:\]',
                    '',
                    response[matches[0].start():matches[0].end()]
                    ).lower()

                # only go on, if the sender matches, else repeat
                if sender in image_Gs.keys():
                    # get message
                    if len(matches) == 1:
                        text = response[matches[0].end():].strip()
                    else:
                        text = response[matches[0].end():matches[1].start(
                        )].strip()

                    # get next prompt
                    prompt = f'[{sender.upper()}:] {text}'

                    # check for images
                    image_data = b''
                    alt = ''
                    if (img_str := '[IMAGE]') in text:
                        image = image_Gs[sender].generate(image_seed[sender])
                        # save image as binary
                        image_output = BytesIO()
                        image.save(
                            image_output,
                            "JPEG",
                            quality=80,
                            optimize=True,
                            progressive=True
                            )
                        image_data = image_output.getvalue()
                        image_output.close()

                        alt = f'selfie of {sender}'

                        image_seed[sender] += 1

                        text = re.sub(r' *', ' ', text.replace(img_str, '')
                                      ).strip()  # get rid of duplicate spaces

                    # wait if message generation was shorter than minimum duration
                    min_duration = len(text) * 0.2
                    if image_data: min_duration += 10
                    duration = time.time() - start
                    start = 0
                    time.sleep(max(0, min_duration - duration))

                    # TODO send message to redis
                    chat_message = {
                        'sender': sender,
                        'text': text,
                        'imageData': image_data,
                        'alt': alt
                        }

                    print(sender.upper(), text, bool(image_data))

    except KeyboardInterrupt:
        raise SystemExit


if __name__ == '__main__':
    generate()