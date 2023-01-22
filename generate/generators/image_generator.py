from typing import Tuple

import time
import numpy as np
import PIL.Image
import pickle
import torch
from logging import Logger


def make_transform(translate: Tuple[float, float], angle: float):
    m = np.eye(3)
    s = np.sin(angle / 360.0 * np.pi * 2)
    c = np.cos(angle / 360.0 * np.pi * 2)
    m[0][0] = c
    m[0][1] = s
    m[0][2] = translate[0]
    m[1][0] = -s
    m[1][1] = c
    m[1][2] = translate[1]
    return m


class ImageGenerator:
    """
    generates images from stylegan3 network .pkl file and returns them as pillow images.
    """
    def __init__(
            self,
            logger: Logger,
            network: str  # network pickle filename
        ) -> None:

        self._logger = logger

        # checking for cuda
        cuda_avail = torch.cuda.is_available()
        if cuda_avail:
            self._logger.info('cuda is available for stylegan')
            self._device = torch.device('cuda')
        else:
            self._logger.warning('cuda is not available for stylegan')
            self._device = torch.device('cpu')

        # loading model
        self._logger.debug(f'loading networks from "{network}"... ', end='')
        with open(network, 'rb') as file:
            self._G = pickle.load(file)['G_ema'].to(self._device)
        self._logger.info('done')

        # empty label
        self._label = torch.zeros([1, self._G.c_dim], device=self._device)

        self._network = network

    def generate(
            self,
            seed: int,  # random seed (same seed will generate same image)
            truncation_psi: float = 1,  # truncation psi (weirdness)
            noise_mode:
        str = 'const',  # noise mode ('const', 'random' or 'none')
            translate: Tuple[float, float] = (0, 0),  # translate XY-coordinate
            rotate: float = 0,  # rotation angle in degrees
        ) -> PIL.Image:
        # measure time
        start = time.time()

        # generate image

        self._logger.debug(
            f'generating image for seed {seed} with "{self._network}"... ',
            )
        z = torch.from_numpy(
            np.random.RandomState(seed).randn(1, self._G.z_dim)
            ).to(self._device)

        # construct an inverse rotation/translation matrix and pass to the generator.  The
        # generator expects this matrix as an inverse to avoid potentially failing numerical
        # operations in the network.
        if hasattr(self._G.synthesis, 'input'):
            m = make_transform(translate, rotate)
            m = np.linalg.inv(m)
            self._G.synthesis.input.transform.copy_(torch.from_numpy(m))

        img = self._G(
            z,
            self._label,
            truncation_psi=truncation_psi,
            noise_mode=noise_mode
            )
        img = (img.permute(0, 2, 3, 1) * 127.5
               + 128).clamp(0, 255).to(torch.uint8)
        pil_img = PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB')

        self._logger.debug(f'done in {time.time() - start}s')

        return pil_img