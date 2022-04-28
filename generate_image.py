# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
"""Generate images using pretrained network pickle."""

from typing import Tuple

import os
import time
import numpy as np
import PIL.Image
import pickle
import torch


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


def generate_image(
        network_pkl: str,  # network pickle filename
        seed: int,  # random seed (same seed will generate same image)
        outdir: str,  # where to save the output images
        truncation_psi: float = 1,  # truncation psi (weirdness)
        noise_mode: str = 'const',  # noise mode ('const', 'random' or 'none')
        translate: Tuple[float, float] = (0, 0),  # translate XY-coordinate
        rotate: float = 0,  # rotation angle in degrees
    ):
    """
    generate image using pretrained network pickle.
    """

    # checking for cuda
    cuda_avail = torch.cuda.is_available()
    if cuda_avail:
        print('cuda is available.')
        device = torch.device('cuda')
    else:
        print('cuda is not available.')
        device = torch.device('cpu')
    print(f'device: "{device}"')

    # loading model
    print(f'Loading networks from "{network_pkl}"...')
    with open(network_pkl, 'rb') as file:
        G = pickle.load(file)['G_ema'].to(device)

    # create out directory, if it doesn't exist yet
    os.makedirs(outdir, exist_ok=True)

    # measure time
    start = time.time()

    # generate from seed
    label = torch.zeros([1, G.c_dim], device=device)

    # generate image
    print(f'Generating image for seed {seed}...')
    z = torch.from_numpy(np.random.RandomState(seed).randn(1, G.z_dim)
                         ).to(device)

    # construct an inverse rotation/translation matrix and pass to the generator.  The
    # generator expects this matrix as an inverse to avoid potentially failing numerical
    # operations in the network.
    if hasattr(G.synthesis, 'input'):
        m = make_transform(translate, rotate)
        m = np.linalg.inv(m)
        G.synthesis.input.transform.copy_(torch.from_numpy(m))

    img = G(z, label, truncation_psi=truncation_psi, noise_mode=noise_mode)
    img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
    PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB').save(
        os.path.join(outdir, f'seed{seed:04d}.png')
        )

    print(f'--- generation took {time.time() - start}s')


#----------------------------------------------------------------------------

if __name__ == "__main__":
    generate_image(
        os.path.join('models', 'network-snapshot-000071.pkl'), 0, 'images'
        )
