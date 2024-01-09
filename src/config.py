"""Provides configuration related parameters."""

from pathlib import Path

# =========================
# Folders
# =========================

ROOT = Path(__file__).absolute().parent.parent

IMAGES_FOLDER = ROOT.joinpath('images')


# =========================
# Logger
# =========================

# CRITICAL: 50
# ERROR: 40
# WARNING: 30
# INFO: 20
# DEBUG: 10
# NOTSET: 0
LOG_LEVEL = 20  # Ignore logging messages which are less severe
if LOG_LEVEL < 20:
    LOG_FORMAT = '%(levelname)s %(filename)s (%(lineno)d) : %(message)s'  # Logging messages string format (for development)
else:
    LOG_FORMAT = '%(levelname)s : %(message)s'  # Logging messages string format (for release)
LOG_FILENAME = None  # Save logging messages to file. None: console


# =========================
# Images
# =========================

IMG_EXTENSIONS = ('*.png', '*.PNG',
                    '*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.jpe', '*.JPE',
                    '*.bmp', '*.BMP', '*.dib', '*.DIB',
                    '*.jp2', '*.JP2',
                    '*.webp', '*.WEBP',
                    '*.pbm', '*.PBM', '*.pgm', '*.PGM', '*.ppm', '*.PPM', '*.pxm', '*.PXM', '*.pnm', '*.PNM',
                    '*.pfm', '*.PFM',
                    '*.sr', '*.SR', '*.ras', '*.RAS',
                    '*.tiff', '*.TIFF', '*.tif', '*.TIF',
                    '*.erx', '*.EXR',
                    '*.hdr', '*.HDR', '*.pic', '*.PIC'
                )

AUGMENTATIONS = {
    'random_crop': '_crop',
    'blur': '_blur',
    'random_rotation': '_rot',
    'random_shear': '_shear',
    'random_scale': '_scale',
    'random_translation': '_trans',
    'left_right_flip': '_lr_flip',
    'top_bottom_flip': '_tb_flip',
    'random_hue': '_hue',
    'random_saturation': '_sat',
    'random_brightness': '_bright'
}

# =========================
# Augmentation
# =========================

SEPARATE_TYPE = 'separate'
MIX_TYPE = 'mix'
ALL_TYPE = 'all'
AUGMENTATION_TYPE = (SEPARATE_TYPE, MIX_TYPE, ALL_TYPE)

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
