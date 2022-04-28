import os
from generators.image_generator import ImageGenerator
from generators.text_generator import TextGenerator

image_G = ImageGenerator(
    os.path.join('models', 'network-snapshot-000071.pkl'), 'images'
    )

text_G = TextGenerator('distilgpt2')

image_G.generate(0)
print(text_G.generate('I can\'t believe', 128))
