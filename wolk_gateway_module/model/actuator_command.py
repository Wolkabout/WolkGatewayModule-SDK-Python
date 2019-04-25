"""Actuator command received from WolkAbout IoT Platform."""
#   Copyright 2019 WolkAbout Technology s.r.o.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from dataclasses import dataclass, field
from typing import Union, Optional
from enum import Enum, unique, auto


@unique
class ActuatorCommandType(Enum):
    """Actuator command type."""

    GET = auto()
    SET = auto()


@dataclass
class ActuatorCommand:
    """Actuator command for reference with command and optionally value."""

    reference: str
    command: ActuatorCommandType
    value: Optional[Union[int, float, str]] = field(default=None)