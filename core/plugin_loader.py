import importlib
import pkgutil
import inspect
import sys
from core.base_module import BaseModule
from core.logger import logger

class PluginLoader:
    def __init__(self, modules_package="modules"):
        self.modules_package = modules_package
        self.plugins = []

    def load_all(self):
        logger.info(f"Carregando plugins de: {self.modules_package}")
        try:
            package = importlib.import_module(self.modules_package)

            prefix = package.__name__ + "."
            for _, name, _ in pkgutil.walk_packages(package.__path__, prefix):
                try:
                    module = importlib.import_module(name)
                    for member_name, member_obj in inspect.getmembers(module):
                        if (inspect.isclass(member_obj) and 
                            issubclass(member_obj, BaseModule) and 
                            member_obj is not BaseModule):
                            
                            instance = member_obj()
                            self.plugins.append(instance)
                            logger.debug(f"Carregado: [cyan]{instance.name}[/cyan]")
                except Exception as e:
                    pass 
        except Exception as e:
            logger.error(f"Erro crítico no loader: {e}")
        
        return self.plugins