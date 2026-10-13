"""Driver registry — name -> driver instance."""
from __future__ import annotations

from src.pipeline.drivers.cpp_driver import CppDriver
from src.pipeline.drivers.csharp_driver import CSharpDriver
from src.pipeline.drivers.java_driver import JavaDriver
from src.pipeline.drivers.python_driver import PythonDriver

_REGISTRY = {
    "python_driver": PythonDriver(),
    "cpp_driver": CppDriver(),
    "csharp_driver": CSharpDriver(),
    "java_driver": JavaDriver(),
}


def get_driver(name: str):
    if name not in _REGISTRY:
        raise KeyError(f"unknown driver: {name}")
    return _REGISTRY[name]