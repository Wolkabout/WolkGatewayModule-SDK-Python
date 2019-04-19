"""Actuator states as defined on WolkAbout IoT Platform."""
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


from enum import Enum, unique


@unique
class ActuatorState(Enum):
    """Enumeration of available actuator states.

    :ivar BUSY: Actuator currently in busy state
    :vartype BUSY: int
    :ivar ERROR: Actuator currently in error state
    :vartype ERROR: int
    :ivar READY: Actuator currently in ready state
    :vartype READY: int
    """

    READY = 0
    BUSY = 1
    ERROR = 2
