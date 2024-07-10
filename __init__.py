from __future__ import annotations
from packages.process.config import ProcessConfig, ProcessConfigUI
from packages.process.function import ProcessFunction
from packages.process.pipe import ProcessPipe

from src.package.package import Package
from typing import TYPE_CHECKING, Iterable
if TYPE_CHECKING:
    from src.pipe import Pipe

class ProcessPackage(Package):
    name: str = "Process"
    _pipes: Iterable[type[Pipe]] = [ProcessPipe]
    dependencies: dict[str, Package] = {}
