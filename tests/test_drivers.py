"""Driver parsing tests."""
from __future__ import annotations

from src.pipeline.drivers.cpp_driver import CppDriver
from src.pipeline.drivers.csharp_driver import CSharpDriver
from src.pipeline.drivers.java_driver import JavaDriver
from src.pipeline.drivers.python_driver import PythonDriver


def test_python_driver_extracts_one_block() -> None:
    draft = "```python\nx = 1\n```\n"
    arts = PythonDriver().parse(draft, target="python")
    assert len(arts) == 1
    assert arts[0].content == "x = 1\n"


def test_cpp_driver_splits_cpp_and_hpp() -> None:
    draft = "```cpp\nint main(){}\n```\n```hpp\n#pragma once\n```\n"
    arts = CppDriver().parse(draft, target="cpp")
    assert {a.rel_path.suffix for a in arts} == {".cpp", ".hpp"}


def test_csharp_driver_ignores_other_langs() -> None:
    draft = "```python\npass\n```\n```csharp\nclass A{}\n```\n"
    arts = CSharpDriver().parse(draft, target="csharp")
    assert len(arts) == 1
    assert arts[0].rel_path.suffix == ".cs"


def test_java_driver_only_java() -> None:
    draft = "```java\npublic class A{}\n```\n```python\npass\n```\n"
    arts = JavaDriver().parse(draft, target="java")
    assert len(arts) == 1
    assert arts[0].rel_path.suffix == ".java"
</thinking>