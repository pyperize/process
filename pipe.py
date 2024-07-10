from __future__ import annotations
import ray
ray.init(ignore_reinit_error=True)

import src.pipe as pipe
from packages.process.config import ProcessConfig, ProcessConfigUI
from packages.process.function import ProcessFunction
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage

class ProcessPipe(pipe.Pipe):
    cls_name: str = "Process"
    cls_config: type[ProcessConfig] = ProcessConfig
    cls_function: type[ProcessFunction] = ProcessFunction

    def __init__(self, name: str, manager: Manager, config: ProcessConfig) -> None:
        super().__init__(name, manager, config)
        self.config: ProcessConfig = config

    def config_ui(self, manager: Manager, config_page: ConfigPage) -> ProcessConfigUI:
        return ProcessConfigUI(self, manager, config_page)

    def play(self, manager: Manager) -> None:
        if self.playing:
            return
        self.playing = True
        if self.config.pipe: 
            self.config.pipe.play(manager)
            self.config._process = ray.remote(num_cpus=self.config.cpus, num_gpus=self.config.gpus)(self.config.pipe.cls_function).remote(self.config.pipe.config)

    def stop(self, manager: Manager, result) -> None:
        if not self.playing:
            return
        self.playing = False
        if self.config._process:
            ray.kill(self.config._process)
        if self.config.pipe:
            self.config.pipe.stop(manager, result)
