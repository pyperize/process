from __future__ import annotations
from packages.process.config import ProcessConfig
from src.pipe.function import IO, Function

class ProcessFunction(Function):
    def __init__(self, config: ProcessConfig) -> None:
        self.config: ProcessConfig = config

    def __call__(self, input: IO) -> IO:
        if self.config._process is not None:
            return self.config._process.__call__.remote(input).future().result()
        return IO()
