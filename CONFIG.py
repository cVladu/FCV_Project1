from augmentations import *

CONFIG_DICT = {
    'Rotation': {
        'func': rotate_image,
        'params': [{'name': 'angle', 'dtype': int},
                   ]
    },
    'Tint': {
        'func': tint_image,
        'params': [{'name': 'channel', 'dtype': str},
                   {'name': 'value', 'dtype': int},
                   ]
    },
    'Dummy': {
        'func': dummy_func,
        'params': [{'name': 'dummy', 'dtype': str},
                   ]
    }
}

TEST = True

img_name_format = '{name}_{augmentation}_{index}{ext}'

