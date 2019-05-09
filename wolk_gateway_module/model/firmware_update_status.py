"""Firmware update status model."""
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
from enum import Enum, unique


@unique
class FirmwareUpdateState(Enum):
    """Enumeration of available firmware update states."""

    INSTALLATION = "INSTALLATION"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    ABORTED = "ABORTED"


@unique
class FirmwareUpdateErrorCode(Enum):
    """Enumeration of possible firmware update errors."""

    UNSPECIFIED_ERROR = 0
    FILE_NOT_PRESENT = 1
    FILE_SYSTEM_ERROR = 2
    INSTALLATION_FAILED = 3
    DEVICE_NOT_PRESENT = 4


@dataclass
class FirmwareUpdateStatus:
    """Holds information about current firmware update status."""

    status: FirmwareUpdateState
    error_code: FirmwareUpdateErrorCode = field(default=None)
