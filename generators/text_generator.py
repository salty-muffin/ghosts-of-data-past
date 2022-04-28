import time
import torch
from aitextgen import aitextgen


class TextGenerator:
    def __init__(
        self,
        model: str,
        ) -> None:

        # checking for cuda
        cuda_avail = torch.cuda.is_available()
        print(f'cuda {"not" if not cuda_avail else ""} is available.')

        self._gpt2 = aitextgen(model=model, to_gpu=cuda_avail)

    def generate(
        self,
        prompt: str,
        max_length: int,
        temperature: float = 0.7,  # controls the "craziness" of the text
        top_k:
        float = 0,  # if nonzero, limits the sampled tokens to the top k values
        top_p:
        float = 0.7  # if nonzero, limits the sampled tokens to the cumulative probability
        ):

        start = time.time()

        response = self._gpt2.generate_one(
            prompt=prompt,
            max_length=max_length,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p
            )

        print(f'--- text generation took {time.time() - start}s')

        return response