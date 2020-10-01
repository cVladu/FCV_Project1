import os
import glob


def read_config_file(file_path, _type='text'):
    """
    Read and decode the config file.
    :param file_path: The path to the config file.
    :param _type: The type of the file. At the moment, only plain text file is supported.
    Possible JSON support in the future
    :return: A list containing config dict. The dicts are in the form:
    {'func': <function_to_be_applied>
     'params': <dictionary_of_params_for_the_function>
     'str_format': <string_used_in_formating_the_name_of_the_new_image>
    }
    """
    augmentation_list = []
    if _type == 'text':
        from CONFIG import CONFIG_DICT
        with open(file_path, 'rt') as config_file:
            for line in config_file.readlines():
                line_split = line.split(' ')
                param_dict = {}
                func = CONFIG_DICT[line_split[0]]['func']
                PARAM_DICT = CONFIG_DICT[line_split[0]]
                for index, param in enumerate(line_split[1:]):
                    dtype_ = PARAM_DICT['params'][index]['dtype']
                    param_dict[PARAM_DICT['params'][index]['name']] = dtype_(param)
                augmentation_list.append({'func': func, 'params': param_dict, 'str_format': line_split[0]})
    else:
        raise NotImplementedError
    return augmentation_list


def get_all_images(dir_path, img_format='jpeg', recurse=False):
    """
    Get a list of all the desired images from a directory with or without recursion.
    :param dir_path: The path to the directory containing the images.
    :param img_format: The format of the image (jpg, gif, etc). Only works with single value at the momemnt.
    :param recurse: If the search should recurse in the sub directories or not
    :return: The list of all the images of the format given
    """

    search_format = '{}*.{}'
    return glob.glob(os.path.join(dir_path, search_format.format('**/' if recurse else "", img_format)),
                     recursive=recurse)

