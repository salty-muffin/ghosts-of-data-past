import os
import time
import torch
from aitextgen import aitextgen

# checking for cuda
cuda_avail = torch.cuda.is_available()
print(f'cuda {"not" if not cuda_avail else ""} is available.')

# ai = aitextgen(model_folder=os.path.join('models', 'german_2000'), to_gpu=True)
# ai = aitextgen(model='EleutherAI/gpt-neo-125M', to_gpu=True)
ai = aitextgen(model='distilgpt2', to_gpu=cuda_avail)

prompt = 'I can\'t believe'

start = time.time()
response = ai.generate_one(
    prompt=prompt, max_length=128, temperature=1.0, top_p=0.7
    )

print(response)
print(f'--- generation took {time.time() - start}s')