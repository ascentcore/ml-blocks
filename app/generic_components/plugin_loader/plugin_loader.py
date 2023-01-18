import os
from importlib import util
from typing import List

from app.generic_components.log_mechanism.log_mechanism import LOG


class PluginLoader(object):

    @staticmethod
    def load_module(path):
        try:
            name = os.path.split(path)[-1]
            spec = util.spec_from_file_location(name, path)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except SyntaxError as e:
            LOG.warn(f'Not loaded {path} due to {e}')

    @staticmethod
    def load_plugins(sources: List[str]) -> None:
        for source in sources:
            plugin_path = os.path.abspath(source)
            directory_plugin_path = os.path.dirname(plugin_path)
            for file_name in os.listdir(directory_plugin_path):
                if not file_name.startswith('.') and not file_name.startswith('__') and file_name.endswith('.py'):
                    file_path = os.path.join(directory_plugin_path, file_name)
                    LOG.info(f'Detected plugin {file_path}')
                    PluginLoader.load_module(file_path)
