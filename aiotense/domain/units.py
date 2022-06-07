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
"""Units domain."""
from __future__ import annotations

__all__ = ["Unit", "Minute", "Hour", "Day", "Week", "VirtualUnit"]

from dataclasses import dataclass
from typing import Iterable


@dataclass
class Unit:
    aliases: Iterable[str]
    duration: int


@dataclass
class VirtualUnit(Unit):
    pass


@dataclass
class Minute(Unit):
    duration: int = 60


@dataclass
class Hour(Unit):
    duration: int = 60 * 60


@dataclass
class Day(Unit):
    duration: int = 60 * 60 * 24


@dataclass
class Week(Unit):
    duration: int = 60 * 60 * 24 * 7