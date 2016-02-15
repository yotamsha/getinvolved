__author__ = 'avishayb'

from jinja2 import Template, Environment, StrictUndefined


def merge(template_body, data):
    """
    Merge a template
    :param template_body:  the template body
    :param data: data to be used for merge
    :return: the merged template
    """
    if not template_body or not isinstance(template_body,str):
        raise Exception('template body must be none empty string')
    if not data or not isinstance(data,dict):
        raise Exception('data must be none empty dict')
    template = Template(template_body, undefined=StrictUndefined)
    return template.render(data)
