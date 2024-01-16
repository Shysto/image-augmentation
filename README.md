# Image augmentation

## Installation

We recommend to use a virtual environment for Python, so that dependencies are not installed globally. <br>
Below is an exemple of virtual environment creation and activation using `pyenv`.
```bash
pyenv install 3.10.6
pyenv virtualenv 3.10.6 image-augmentation

# Activate the environment
pyenv local image-augmentation
```

Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```python
python run.py -d <INPUT_DATASET> -o <OUTPUT_DATASET> -a <AUGMENTATIONS...> -t <AUGMENTATION_TYPE>
```

The mandatory `-d` option specifies the input dataset of images. <br>
The folder structure will be conserved.

The mandatory `-o` option specifies the output folder (the augmented dataset).

The mandatory `-a` option specifies the list of augmentations to perform. <br>
Currently, the following augmentations are supported:

| Type | Explanation |
|-----|-----|
| `random_crop` | Randomly crops a portion of an image (black padding). |
| `blur` | Applies Gaussian noise (blurring) to an image. |
| `random_rotation` | Randomly rotates an image (black padding). |
| `random_shear` | Randomly shears an image (black padding). |
| `random_scale` | Randomly rescales an image (black padding). |
| `random_translation` | Randomly translates an image (black padding). |
| `left_right_flip` | Mirrors an image on the vertical axis. |
| `top_bottom_flip` | Mirrors an image on the horizontal axis. |
| `random_hue` | Randomly alterates the hue of an image. |
| `random_saturation` | Randomly alterates the saturation of an image. |
| `random_brightness` | Randomly alterates the brightness of an image. |

More details on how to control each augmentation can be found in the section [Configuration](#configuration).

The mandatory `-t` option specifies the type of augmentation to perform. <br>
Currently, the following types are supported:

| Type | Explanation |
|-----|-----|
| `separate` | For each image, performs each augmentation separately, once at a time, and save the corresponding image. |
| `mix` | For each image, performs each augmentation all at once, and save the resulting image. |
| `all` | Combination of `separate` and `mix` types (both are applied). |

By providing the facultative `-n` option, you can specify how many times to augment each image in the case au augmentation types `mix` or `all` (default is `10`).

## Configuration

You may tweak several parameters to controle the image augmentation by changing the following default values in the [src/config.py](./src/config.py) file.
```python
CROP_SIZE = (512, 512)
ROTATION_RANGE = (-30, 30)
HORIZONTAL_TRANSLATION_RANGE = (-100, 100)
VERTICAL_TRANSLATION_RANGE = (-100, 100)
HORIZONTAL_SHEAR_RANGE = (-0.3, 0.3)
VERTICAL_SHEAR_RANGE = (-0.3, 0.3)
SCALE_RANGE = (1.0, 2.0)
HUE_FACTOR_RANGE = (0.5, 1.5)
BRIGHTNESS_FACTOR_RANGE = (0.5, 1.5)
SATURATION_FACTOR_RANGE = (0.5, 1.5)
```

Below are the explanations for each parameter:

| Parameter | Type | Accepted values | Explanation |
|-----|-----|-----|-----|
| `CROP_SIZE` | `tuple(int, int)` | Should be positive | The maximum size `(width, height)` of the cropped region. A random size (not necessarily square) smaller than this value will be randomly chosen. |
| `ROTATION_RANGE` | `tuple(float, float)` | - | The possible range `(min_angle, max_angle)` for the rotation range, in degrees. A positive angle corresponds to a counterclockwise rotation. A random angle in this range will be randomly chosen. |
| `HORIZONTAL_TRANSLATION_RANGE` | `tuple(int, int)` | - | The possible range `(min_x, max_x)` for the translation range along the X-axis, in pixels. A positive value corresponds to a tanslation to the right. A random value in this range will be randomly chosen. |
| `VERTICAL_TRANSLATION_RANGE` | `tuple(int, int)` | - | The possible range `(min_y, max_y)` for the translation range along the Y-axis, in pixels. A positive value corresponds to a tanslation to the bottom. A random value in this range will be randomly chosen. |
| `HORIZONTAL_SHEAR_RANGE` | `tuple(float, float)` | - | The possible range `(min_x, max_x)` for the shear range along the X-axis. A positive value corresponds to a displacement to the right. A random value in this range will be randomly chosen. |
| `VERTICAL_SHEAR_RANGE` | `tuple(float, float)` | - | The possible range `(min_y, max_y)` for the shear range along the Y-axis. A positive value corresponds to a displacement to the bottom. A random value in this range will be randomly chosen. |
| `SCALE_RANGE` | `tuple(float, float)` | Should be positive | The possible range `(min_scale, max_scale)` for the image scaling range. The same scaling factor is applied to both axis. A value bigger than 1 enlarges the image. A random value in this range will be randomly chosen. |
| `HUE_FACTOR_RANGE` | `tuple(float, float)` | Should be positive | The possible range `(min_hue, max_hue)` for the hue (color) alteration factor range. A value bigger than 1 means more color. A random value in this range will be randomly chosen. |
| `BRIGHTNESS_FACTOR_RANGE` | `tuple(float, float)` | Should be positive | The possible range `(min_brightness, max_brightness)` for the brightness alteration factor range. A value bigger than 1 means brighter. A random value in this range will be randomly chosen. |
| `SATURATION_FACTOR_RANGE` | `tuple(float, float)` | Should be positive | The possible range `(min_saturation, max_saturation)` for the saturation (contrast) alteration factor range. A value bigger than 1 means more contrast. A random value in this range will be randomly chosen. |
