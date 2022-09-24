import time
import torch
import random
from aitextgen import aitextgen


class TextGenerator:
    """
    generates text from prompts with a gpt-2/gpt-2neo model and returns them as a string.
    """
    def __init__(
            self,
            model: str = None,
            model_folder: str = None,
            verbose: bool = True
        ) -> None:

        self._verbose = verbose

        # checking for cuda
        cuda_avail = torch.cuda.is_available()
        print(f'cuda is {"not" if not cuda_avail else ""} available for gpt')

        self._gpt2 = aitextgen(
            model=model, model_folder=model_folder, to_gpu=cuda_avail
            )

        self._model = model if model else model_folder

    def generate(
        self,
        prompt: str,
        max_length: int,
        seed: int = None,
        temperature: float = 0.7,  # controls the "craziness" of the text
        top_k:
        float = 0,  # if nonzero, limits the sampled tokens to the top k values
        top_p:
        float = 0.7,  # if nonzero, limits the sampled tokens to the cumulative probability
        n: int = 1
        ):

        if self._verbose:
            print(
                f'generating message for seed {seed} with "{self._model}"... ',
                )

        start = time.time()

        which_n = 0
        if n > 1:
            which_n = random.randrange(n)

        responses = self._gpt2.generate(
            prompt=prompt,
            n=n,
            return_as_list=True,
            max_length=max_length,
            seed=seed,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            )

        # for index, response in enumerate(responses):
        #     if '[image]' in response:
        #         which_n = index

        if self._verbose: print(f'done in {time.time() - start}s')

        return responses[which_n]