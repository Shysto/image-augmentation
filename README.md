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
