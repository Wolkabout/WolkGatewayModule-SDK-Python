"""Module that provides connectivity for non-IP enabled devices to WolkAbout IoT Platform."""
#   Copyright 2020 WolkAbout Technology s.r.o.
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
__version__ = "1.0.9"

from .connectivity.connectivity_service import ConnectivityService
from .interface.actuation_handler import handle_actuation
from .interface.actuator_status_provider import get_actuator_status
from .interface.configuration_handler import handle_configuration
from .interface.configuration_provider import get_configuration
from .interface.device_status_provider import get_device_status
from .interface.firmware_handler import FirmwareHandler
from .logger_factory import logging_config
from .model.actuator_command import ActuatorCommand
from .model.actuator_state import ActuatorState
from .model.actuator_status import ActuatorStatus
from .model.actuator_template import ActuatorTemplate
from .model.alarm import Alarm
from .model.alarm_template import AlarmTemplate
from .model.configuration_command import ConfigurationCommand
from .model.configuration_template import ConfigurationTemplate
from .model.data_type import DataType
from .model.device import Device
from .model.device_registration_request import DeviceRegistrationRequest
from .model.device_registration_response import DeviceRegistrationResponse
from .model.device_status import DeviceStatus
from .model.device_template import DeviceTemplate
from .model.firmware_update_status import FirmwareUpdateErrorCode
from .model.firmware_update_status import FirmwareUpdateState
from .model.firmware_update_status import FirmwareUpdateStatus
from .model.message import Message
from .model.reading_type import ReadingType
from .model.reading_type_measurement_unit import ReadingTypeMeasurementUnit
from .model.reading_type_name import ReadingTypeName
from .model.sensor_reading import SensorReading
from .model.sensor_template import SensorTemplate
from .persistence.outbound_message_queue import OutboundMessageQueue
from .protocol.data_protocol import DataProtocol
from .protocol.firmware_update_protocol import FirmwareUpdateProtocol
from .protocol.registration_protocol import RegistrationProtocol
from .protocol.status_protocol import StatusProtocol
from .wolk import Wolk

__all__ = [
    "Wolk",
    "logging_config",
    "handle_actuation",
    "get_actuator_status",
    "handle_configuration",
    "get_configuration",
    "get_device_status",
    "ActuatorState",
    "FirmwareHandler",
    "FirmwareUpdateState",
    "FirmwareUpdateStatus",
    "FirmwareUpdateErrorCode",
    "DataType",
    "ReadingType",
    "ReadingTypeMeasurementUnit",
    "ReadingTypeName",
    "SensorTemplate",
    "Device",
    "DeviceTemplate",
    "ActuatorTemplate",
    "AlarmTemplate",
    "ConfigurationTemplate",
    "ConnectivityService",
    "DataProtocol",
    "RegistrationProtocol",
    "StatusProtocol",
    "FirmwareUpdateProtocol",
    "OutboundMessageQueue",
    "Message",
    "ActuatorCommand",
    "ConfigurationCommand",
    "SensorReading",
    "Alarm",
    "ActuatorStatus",
    "DeviceRegistrationRequest",
    "DeviceRegistrationResponse",
    "DeviceStatus",
    "__version__",
]
