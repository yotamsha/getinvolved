__author__ = 'avishayb'

from jinja2 import Template, Environment, StrictUndefined, FileSystemLoader
import os


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class GIFileSystemLoader(FileSystemLoader):
    def __init__(self, root_folder, lang='en'):
        super(GIFileSystemLoader, self).__init__(root_folder + '/data/' + lang)

    def get_source(self, environment, template):
        return super(GIFileSystemLoader, self).get_source(_j2_env, template)


_j2_env = Environment(loader=None, undefined=StrictUndefined,
                      trim_blocks=True, cache_size=0)


def merge(template_body, data):
    """
    Merge a template
    :param template_body:  the template body
    :param data: data to be used for merge
    :return: the merged template
    """
    if not template_body or not isinstance(template_body, str):
        raise Exception('template body must be none empty string')
    if not data or not isinstance(data, dict):
        raise Exception('data must be none empty dict')
    template = Template(template_body, undefined=StrictUndefined)
    return template.render(data)


def load_and_merge(template_name, data, lang='en'):
    """
    Load and Merge a template
    :param template_name:  the template name
    :param data: data to be used for merge
    :param lang: the template language (this used as a sub folder under data folder)
    :return: the merged template
    """
    if not template_name or not isinstance(template_name, str):
        raise Exception('template_name  must be none empty string')
    if not data or not isinstance(data, dict):
        raise Exception('data must be none empty dict')
    _j2_env.loader = GIFileSystemLoader(THIS_DIR, lang=lang)
    template = _j2_env.get_template(template_name)
    return template.render(data)



