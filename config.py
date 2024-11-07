from __future__ import annotations
import flet as ft
import src.pipe
from src.ui.pipe import PipeTile
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage
    from packages.process.pipe import ProcessPipe
    import ray

class ProcessConfig(src.pipe.Config):
    pipe: src.pipe.Pipe | None = None
    cpus: int = 1
    gpus: int = 1
    _process: ray.ObjectRef | None = None

class ProcessConfigUI(src.pipe.ConfigUI):
    def __init__(self, instance: ProcessPipe, manager: Manager, config_page: ConfigPage) -> None:
        super().__init__(instance, manager, config_page)
        self.instance: ProcessPipe = instance
        self.content: ft.Column = ft.Column([
            PipeTile(
                "Pipe",
                self.manager,
                self.config_page,
                self.select_pipe,
                self.delete_pipe,
                self.instance.config.pipe,
            ),
            ft.TextField(self.instance.config.cpus, label="Number of CPUs", border_color="grey", input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9\.]", replacement_string="")),
            ft.TextField(self.instance.config.gpus, label="Number of GPUs", border_color="grey", input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9\.]", replacement_string="")),
        ])

    def select_pipe(self, cls: type[src.pipe.Pipe] | src.pipe.Pipe) -> src.pipe.Pipe:
        if isinstance(cls, type):
            cls: src.pipe.Pipe = cls(cls.cls_name, self.manager, cls.cls_config())
        return cls

    def delete_pipe(self, e) -> None:
        self.content.pipe_selector.value = None
        self.content.select_changed(None)
        self.update()

    def dismiss(self) -> None:
        self.instance.config.pipe = self.content.controls[0].instance
        self.instance.config.cpus = int(self.content.controls[1].value)
        self.instance.config.gpus = int(self.content.controls[2].value)
