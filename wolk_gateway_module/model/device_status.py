"""Device statuses as defined on WolkAbout IoT Platform."""
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
class DeviceStatus(Enum):
    """Enumeration of available device statuses.

    :ivar CONNECTED: Device currently connected
    :vartype CONNECTED: int
    :ivar OFFLINE: Device currently offline
    :vartype OFFLINE: int
    :ivar SERVICE: Device currently in service mode
    :vartype SERVICE: int
    :ivar SLEEP: Device currently in sleep mode
    :vartype SLEEP: int
    """

    CONNECTED = 0
    OFFLINE = 1
    SLEEP = 2
    SERVICE = 3
