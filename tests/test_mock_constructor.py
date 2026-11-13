# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Any, cast

from pydantic import BaseModel
from testslide.core import TestCase
from testslide.core.lib import TypeCheckError
from testslide.core.mock_constructor import unpatch_all_constructor_mocks
from testslide.core.strict_mock import StrictMock


class ModelBase(BaseModel):
    value: str


class Model(ModelBase):
    pass


class Item:
    pass


class MockConstructorTest(TestCase):
    def test_pydantic_constructor_returns_configured_mock(self) -> None:
        mock = object()
        self.mock_constructor(__name__, "Model").to_return_value(mock)

        self.assertIs(Model(value="mocked"), mock)

    def test_annotations_resolved_while_mocked_accept_original_type(self) -> None:
        original_class = Item
        original = Item()
        strict_mock = cast(Any, StrictMock)(template=original_class)
        self.mock_constructor(__name__, "Item").to_return_value(strict_mock)

        class Consumer:
            def consume(self, items: list[Item]) -> str:
                return "original"

        consumer = Consumer()
        self.mock_callable(consumer, "consume").to_return_value("mocked")

        self.assertEqual(consumer.consume([original, strict_mock]), "mocked")
        with self.assertRaises(TypeCheckError):
            consumer.consume(cast(Any, [object()]))

        unpatch_all_constructor_mocks()
        self.assertEqual(consumer.consume([original, strict_mock]), "mocked")
        self.assertIs(Item, original_class)
