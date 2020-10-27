import os
import glob


# noinspection PyUnreachableCode
def read_config_file(file_path, _type='.yaml'):
    """
    Read and decode the config file.

    :param file_path: The path to the config file.
    :param _type: The type of the file. Only yaml file supported. Other types raise Not
    :return: augmentation_dict - a dict containing all the transformations that need to be applied.
        The dictionaries are in the form:
        {"<Transformation_name> : # The name will be used to format the output image name
            {'func': <name_of_the_function> # The name of the transformation to be applied.
             'params': <dict_of_params> # The dictionary of params to be passed to the function.
                                        # Must be in the form of <param> : <value>
             'en': <bool>  # Specify if the transformation shall be applied as a standalone. It can miss. In this case, the default is True
        }
                chain_list - a list containing all the transformation that need to be applied as a chain. The transformation
                are given as a name in the already defined augmentation_list
    :raises: NotImplementedError in case the chosen file type is not yaml
    """
    if _type == '.txt':
        raise NotImplementedError("{} file handling not implemented".format(_type))
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
    elif _type == '.yaml' or _type == '.yml':
        import yaml
        from CONFIG import FUNC_MAPPING
        with open(file_path) as yaml_f:
            data = yaml.load(yaml_f)
        augmentation_dict = data['Transformations']
        chain_list = data['Chain_Transformation']
        for func_dict in augmentation_dict.values():
            try:
                func_dict['func'] = FUNC_MAPPING[func_dict['func'].lower()]
            except KeyError:
                raise KeyError("{} function is not valid or it couldn't be found".format(func_dict['func']))
    else:
        if _type:
            raise NotImplementedError("{} file handling not implemented".format(_type))
        else:
            raise Exception("Configuration file not selected")
    return augmentation_dict, chain_list


def get_all_images(dir_path, img_format='jpeg', recurse=False):
    """
    Get a list of all the desired images from a directory with or without recursion.

    :param dir_path: The path to the directory containing the images.
    :param img_format: The format of the image (jpg, gif, etc). Only works with single value at the moment.
    :param recurse: If the search should recurse in the sub directories or not
    :return: The list of all the images of the format given
    """

    search_format = '{}*.{}'
    return glob.glob(os.path.join(dir_path, search_format.format('**/' if recurse else "", img_format)),
                     recursive=recurse)

