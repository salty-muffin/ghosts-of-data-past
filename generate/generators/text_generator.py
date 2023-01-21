import time
import torch
import random
from aitextgen import aitextgen
from logging import Logger


class TextGenerator:
    """
    generates text from prompts with a gpt-2/gpt-2neo model and returns them as a string.
    """
    def __init__(
            self,
            model: str = None,
            model_folder: str = None,
            logger: Logger = True
        ) -> None:

        self._logger = logger

        # checking for cuda
        cuda_avail = torch.cuda.is_available()
        self._warning(
            f'cuda is {"not" if not cuda_avail else ""} available for gpt'
            )

        self._gpt2 = aitextgen(
            model=model, model_folder=model_folder, to_gpu=cuda_avail
            )

        self._model = model if model else model_folder

    def _debug(self, message: str) -> None:
        if self._logger: self._logger.debug(message)

    def _warning(self, message: str) -> None:
        if self._logger: self._logger.warning(message)
        else: print(message)

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

        self._debug(
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

        self._debug(f'done in {time.time() - start}s')

        return responses[which_n]