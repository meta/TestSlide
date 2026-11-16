# pyre-unsafe
import inspect as inspect
from collections.abc import Callable as Callable
from typing import Any as Any

from testslide.core.lib import MOCKED_CLASS_ORIGINAL_ATTR as MOCKED_CLASS_ORIGINAL_ATTR
from testslide.core.mock_constructor import (
    AttrAccessValidation as AttrAccessValidation,
    mock_constructor as mock_constructor,
    unpatch_all_constructor_mocks as unpatch_all_constructor_mocks,
)

_MockConstructorDSL = Any
