import random
import shutil
from pathlib import Path
from argparse import ArgumentParser

from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from tqdm import tqdm
import cv2

from .log import setup_logger
from .config import *

logger = setup_logger(__name__)

class DataAugmentation:
    def __init__(self, dataset_path, output_path, augmentations):
        self.dataset_path = dataset_path.absolute()
        self.output_path = output_path.absolute()
        self.augmentations = augmentations

        self.build_augmentation_pipeline(self.augmentations)
        self.remove_folder(self.output_path)
        self.copy_dir(self.dataset_path, self.output_path)

        self.load_dataset()

    def remove_folder(self, directory):
        if not directory.exists():
            logger.debug(f"Directory '{str(directory)}' does not exist.")
            return

        for item in directory.iterdir():
            if item.is_file():
                item.unlink()  # Remove file
            elif item.is_dir():
                self.remove_folder(item)  # Recursively remove subdirectories

        directory.rmdir()  # Remove the directory itself

    def copy_dir(self, src, dest):
        dest.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            if item.is_file():
                logger.debug(f'Copy file {str(item)} to {str(dest)}')
                shutil.copy2(item, dest)
            elif item.is_dir():
                new_destination = dest.joinpath(item.name)
                new_destination.mkdir(parents=True, exist_ok=True)
                self.copy_dir(item, new_destination)

    def load_dataset(self, pattern=IMG_EXTENSIONS):
        self.src_images = []

        for files in pattern:
            self.src_images.extend(Path(self.dataset_path).rglob(files))

        self.src_images = sorted(self.src_images)

    def load_image(self, image_path):
        return Image.open(str(image_path)).convert('RGB')

    def get_relative_path(self, image_path):
        return image_path.absolute().relative_to(self.dataset_path)

    def save_image(self, image, src_image_path, tag=''):
        dst_image_path = self.output_path.joinpath(self.get_relative_path(src_image_path))
        parent_folder = dst_image_path.parent
        parent_folder.mkdir(parents=True, exist_ok=True)
        dst_image_path = parent_folder.joinpath(dst_image_path.stem + tag + '.jpg')
        if dst_image_path.exists():
            logger.warning(f'Image {str(dst_image_path)} already exists, overwriting it...')
        open_cv_image = np.array(image)
        # Convert RGB to BGR
        try:
            open_cv_image = open_cv_image[:, :, ::-1].copy()
        except Exception as e:
            print(f"Image {str(src_image_path)}: {e}.")
            return
        #image.save(str(dst_image_path))
        cv2.imwrite(str(dst_image_path), open_cv_image)

    def _check_range(self, range, assert_positive=False):
        range = sorted(tuple(range))
        if len(range) == 1:
            range = (-range[0], range[0])

        if assert_positive:
            range = self._assure_positive_range(range)

        return range

    def _clamp_value(self, val, min_val, max_val):
        return max(min(val, max_val), min_val)

    def _assure_positive_range(self, range):
        return (max(0, range[0]), max(0, range[1]))

    def _swap_value_in_increasing_order(self, box, i, j):
        if box[min(i, j)] > box[max(i, j)]:
            tmp_val = box[min(i, j)]
            box[min(i, j)] = box[max(i, j)]
            box[max(i, j)] = tmp_val
        return box

    def crop(self, image, box):
        image_width, image_height = image.size

        box = (self._clamp_value(box[0], 0, image_width - 1),
               self._clamp_value(box[1], 0, image_height - 1),
               self._clamp_value(box[2], 0, image_width - 1),
               self._clamp_value(box[3], 0, image_height - 1))

        box = self._swap_value_in_increasing_order(box, 0, 2)
        box = self._swap_value_in_increasing_order(box, 1, 3)

        return image.crop(box)

    def random_crop(self, image, crop_size=CROP_SIZE):
        image_width, image_height = image.size
        crop_width, crop_height = crop_size

        crop_width = min(crop_width, image_width - 1)
        crop_height = min(crop_height, image_height - 1)

        start_x = random.randint(0, image_width - crop_width)
        start_y = random.randint(0, image_height - crop_height)

        cropping_box = (start_x, start_y, start_x + crop_width, start_y + crop_height)

        cropped_image = self.crop(image, cropping_box)

        # Calculate the position to paste the image at the center
        center_x = (image_width - cropped_image.width) // 2
        center_y = (image_height - cropped_image.height) // 2
        paste_position = (center_x, center_y)

        # Paste the image at the center of the black image
        out_image = Image.new('RGB', image.size)
        out_image.paste(cropped_image, paste_position)
        return out_image

    def blur(self, image):
        return image.filter(filter=ImageFilter.BLUR)

    def rotate(self, image, theta):
        # This method returns a copy of this image, rotated the given number of degrees counter clockwise around its centre.
        return image.rotate(angle=theta)

    def random_rotation(self, image, rotation_range=ROTATION_RANGE):
        rotation_range = self._check_range(rotation_range)
        theta = random.randint(rotation_range[0], rotation_range[1])
        return self.rotate(image, theta)

    def transform(self, image, params):
        return image.transform(image.size, Image.AFFINE, data=params)

    def random_translation(self, image,
                           horizontal_translation_range=HORIZONTAL_TRANSLATION_RANGE,
                           vertical_translation_range=VERTICAL_TRANSLATION_RANGE):
        horizontal_translation_range = self._check_range(horizontal_translation_range)
        vertical_translation_range = self._check_range(vertical_translation_range)

        translate_x = random.randint(horizontal_translation_range[0], horizontal_translation_range[1])
        translate_y = random.randint(vertical_translation_range[0], vertical_translation_range[1])

        translation_params = (1, 0, translate_x, 0, 1, translate_y)
        return self.transform(image, translation_params)

    def random_shear(self, image,
                     horizontal_shear_range=HORIZONTAL_SHEAR_RANGE,
                     vertical_shear_range=VERTICAL_SHEAR_RANGE):
        horizontal_shear_range = self._check_range(horizontal_shear_range)
        vertical_shear_range = self._check_range(vertical_shear_range)

        horizontal_shear_value = random.uniform(horizontal_shear_range[0], horizontal_shear_range[1])
        vertical_shear_value = random.uniform(vertical_shear_range[0], vertical_shear_range[1])

        shear_params = (1, horizontal_shear_value, 0, vertical_shear_value, 1, 0)
        return self.transform(image, shear_params)

    def random_scale(self, image, scale_range=SCALE_RANGE):
        scale_range = self._check_range(scale_range, assert_positive=True)
        scale_value = random.uniform(scale_range[0], scale_range[1])

        scale_params = (scale_value, 0, 0, 0, scale_value, 0)
        return self.transform(image, scale_params)

    def left_right_flip(self, image):
        return image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)

    def top_bottom_flip(self, image):
        return image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)

    def random_hue(self, image, hue_factor_range=HUE_FACTOR_RANGE):
        hue_factor_range = self._check_range(hue_factor_range, assert_positive=True)
        hue_factor = random.uniform(hue_factor_range[0], hue_factor_range[1])

        enhanced_image = ImageEnhance.Color(image)
        return enhanced_image.enhance(hue_factor)

    def random_brightness(self, image, brightness_factor_range=BRIGHTNESS_FACTOR_RANGE):
        brightness_factor_range = self._check_range(brightness_factor_range, assert_positive=True)
        brightness_factor = random.uniform(brightness_factor_range[0], brightness_factor_range[1])

        enhanced_image = ImageEnhance.Brightness(image)
        return enhanced_image.enhance(brightness_factor)

    def random_saturation(self, image, saturation_factor_range=SATURATION_FACTOR_RANGE):
        saturation_factor_range = self._check_range(saturation_factor_range, assert_positive=True)
        saturation_factor = random.uniform(saturation_factor_range[0], saturation_factor_range[1])

        enhanced_image = ImageEnhance.Contrast(image)
        return enhanced_image.enhance(saturation_factor)

    def build_augmentation_pipeline(self, augmentations):
        self.pipeline = {}

        for a in augmentations:
            if a == 'random_crop':
                self.pipeline[a] = self.random_crop
            elif a == 'blur':
                self.pipeline[a] = self.blur
            elif a == 'random_rotation':
                self.pipeline[a] = self.random_rotation
            elif a == 'random_shear':
                self.pipeline[a] = self.random_shear
            elif a == 'random_scale':
                self.pipeline[a] = self.random_scale
            elif a == 'random_translation':
                self.pipeline[a] = self.random_translation
            elif a == 'left_right_flip':
                self.pipeline[a] = self.left_right_flip
            elif a == 'top_bottom_flip':
                self.pipeline[a] = self.top_bottom_flip
            elif a == 'random_hue':
                self.pipeline[a] = self.random_hue
            elif a == 'random_saturation':
                self.pipeline[a] = self.random_saturation
            elif a == 'random_brightness':
                self.pipeline[a] = self.random_brightness
            else:
                logger.error(f'Augmentation "{a}" is not supported yet.')
                continue

    def single_augment(self, image_path):
        image = self.load_image(image_path)

        for name, f in self.pipeline.items():
            logger.debug(f'Applying {name}')
            aug_image = f(image)
            self.save_image(aug_image, image_path, AUGMENTATIONS[name])

    def multiple_augment(self, image_path, suffix):
        image = self.load_image(image_path)

        for name, f in self.pipeline.items():
            logger.debug(f'Applying {name}')
            image = f(image)

        self.save_image(image, image_path, suffix)


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('-d', '--data', type=Path, default=IMAGES_FOLDER,
        help='Path to the dataset directory.')
    ap.add_argument('-o', '--output', type=Path, default=Path('./test_augmentation'),
        help='Path to the output directory.')
    ap.add_argument('-a', '--augmentations', type=str, nargs='+', choices=tuple(AUGMENTATIONS.keys()), default=tuple(AUGMENTATIONS.keys()),
        help='List of augmentations to perform.')

    args = ap.parse_args()

    data_augmentor = DataAugmentation(args.data, args.output, args.augmentations)

    for image_path in tqdm(data_augmentor.src_images):
        data_augmentor.single_augment(image_path)
        data_augmentor.multiple_augment(image_path, '_aug')
