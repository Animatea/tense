# Copyright 2022 Animatea
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" """
from __future__ import annotations

__all__ = ["TenseParser"]

from typing import Any

from aiotense.adapters import parsers, repository
from aiotense.domain import model

from . import exceptions
from .ports import parsers as abc_parsers

_tenses = repository.TenseRepository()


class TenseParser:
    """Base parsers factory.

    Parameters:
    -----------
    parser_cls: :class:`Any` = DIGIT
        Concrete parser type.
    tense: :class:`model.Tense` = model.Tense.from_dict(_tenses.source), *
        Configuration for concrete parser.

    Raises:
    -------
    :class:`exceptions.InvalidParserType`
        Raises if 'parser_cls' is not subclass of :class:`abc_parsers.AbstractParser`
    """
    TIMEDELTA = parsers.TimedeltaParser
    DIGIT = parsers.DigitParser

    def __new__(
        cls,
        parser_cls: Any = DIGIT,
        *,
        tense: model.Tense = model.Tense.from_dict(_tenses.source),
    ) -> abc_parsers.AbstractParser:
        if not issubclass(parser_cls, abc_parsers.AbstractParser):
            raise exceptions.InvalidParserType(
                f"Invalid parser type, you can only use {parsers.__all__}."
            )
        instance = parser_cls.__new__(parser_cls)
        instance.__init__(tense=tense)
        return instance
