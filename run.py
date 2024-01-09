from pathlib import Path
from argparse import ArgumentParser

from tqdm import tqdm

from src import *

if __name__ == '__main__':
    logger = setup_logger(__name__)

    ap = ArgumentParser()
    ap.add_argument('-d', '--data', type=Path, required=True,
        help='Path to the dataset directory.')
    ap.add_argument('-o', '--output', type=Path, required=True,
        help='Path to the output directory.')
    ap.add_argument('-a', '--augmentations', type=str, nargs='+', choices=tuple(AUGMENTATIONS.keys()), required=True,
        help='List of augmentations to perform.')
    ap.add_argument('-t', '--augmentation_type', type=str, choices=AUGMENTATION_TYPE, required=True,
        help='Whether to copy the original image (unchanged) in the output dataset.')
    ap.add_argument('-n', type=int, default=10,
        help='How many times to augment each image.')

    args = ap.parse_args()

    data_augmentor = DataAugmentation(args.data, args.output, args.augmentations)

    for image_path in tqdm(data_augmentor.src_images):
        if args.augmentation_type in [SEPARATE_TYPE, ALL_TYPE]:
            data_augmentor.single_augment(image_path)

        if args.augmentation_type in [MIX_TYPE, ALL_TYPE]:
            for i in range(args.n):
                data_augmentor.multiple_augment(image_path, '_' + str(i).zfill(2))

    logger.info("Script finished successfully.")
