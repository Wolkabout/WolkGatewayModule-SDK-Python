"""Handling of outbound and inbound messages related to device data."""
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
from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from wolk_gateway_module.model.actuator_command import ActuatorCommand
from wolk_gateway_module.model.actuator_status import ActuatorStatus
from wolk_gateway_module.model.alarm import Alarm
from wolk_gateway_module.model.configuration_command import (
    ConfigurationCommand,
)
from wolk_gateway_module.model.message import Message
from wolk_gateway_module.model.sensor_reading import SensorReading

Configuration = Dict[
    str,
    Union[
        int,
        float,
        bool,
        str,
        Tuple[int, int],
        Tuple[int, int, int],
        Tuple[float, float],
        Tuple[float, float, float],
        Tuple[str, str],
        Tuple[str, str, str],
    ],
]


class DataProtocol(ABC):
    """Parse inbound messages and serialize outbound messages."""

    @abstractmethod
    def get_inbound_topics_for_device(self, device_key: str) -> List[str]:
        """
        Return list of inbound topics for given device key.

        :param device_key: Device key for which to create topics
        :type device_key: str

        :returns: inbound_topics
        :rtype: list
        """
        pass

    @abstractmethod
    def is_actuator_get_message(self, message: Message) -> bool:
        """
        Check if message is actuator get command.

        :param message: Message received
        :type message: Message

        :returns: is_actuator_get_message
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_actuator_set_message(self, message: Message) -> bool:
        """
        Check if message is actuator set command.

        :param message: Message received
        :type message: Message

        :returns: is_actuator_set_message
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_configuration_get_message(self, message: Message) -> bool:
        """
        Check if message is configuration get command.

        :param message: Message received
        :type message: Message

        :returns: is_configuration_get_message
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_configuration_set_message(self, message: Message) -> bool:
        """
        Check if message is configuration set command.

        :param message: Message received
        :type message: Message

        :returns: is_configuration_set_message
        :rtype: bool
        """
        pass

    @abstractmethod
    def extract_key_from_message(self, message: Message) -> str:
        """
        Extract device key from message.

        :param message: Message received
        :type message: Message

        :returns: device_key
        :rtype: str
        """
        pass

    @abstractmethod
    def make_actuator_command(self, message: Message) -> ActuatorCommand:
        """
        Make actuator command from message.

        :param message: Message received
        :type message: Message

        :returns: actuator_command
        :rtype: ActuatorCommand
        """
        pass

    @abstractmethod
    def make_configuration_command(
        self, message: Message
    ) -> ConfigurationCommand:
        """
        Make configuration command from message.

        :param message: Message received
        :type message: Message

        :returns: configuration_command
        :rtype: ConfigurationCommand
        """
        pass

    @abstractmethod
    def make_sensor_reading_message(
        self, device_key: str, sensor_reading: SensorReading
    ) -> Message:
        """
        Make message from sensor reading for device key.

        :param device_key: Device on which the sensor reading occurred
        :type device_key: str
        :param sensor_reading: Sensor reading data
        :type sensor_reading: SensorReading

        :returns: message
        :rtype: Message
        """
        pass

    @abstractmethod
    def make_sensor_readings_message(
        self,
        device_key: str,
        sensor_readings: List[SensorReading],
        timestamp=None,
    ) -> Message:
        """
        Make message from multiple sensor readings for device key.

        :param device_key: Device on which the sensor reading occurred
        :type device_key: str
        :param sensor_readings: List of sensor readings data
        :type sensor_readings: List[SensorReading]
        :param timestamp: Timestamp
        :type timestamp: Optional[int]

        :returns: message
        :rtype: Message
        """
        pass

    @abstractmethod
    def make_alarm_message(self, device_key: str, alarm: Alarm) -> Message:
        """
        Make message from alarm for device key.

        :param device_key: Device on which the alarm occurred
        :type device_key: str
        :param alarm: Alarm data
        :type alarm: Alarm

        :returns: message
        :rtype: Message
        """
        pass

    @abstractmethod
    def make_actuator_status_message(
        self, device_key: str, actuator_status: ActuatorStatus
    ) -> Message:
        """
        Make message from actuator status for device key.

        :param device_key: Device on which the actuator status occurred
        :type device_key: str
        :param actuator_status: Actuator status data
        :type actuator_status: ActuatorStatus

        :returns: message
        :rtype: Message
        """
        pass

    @abstractmethod
    def make_configuration_message(
        self, device_key: str, configuration: Configuration
    ) -> Message:
        """
        Make message from configuration for device key.

        :param device_key: Device to which the configuration belongs to.
        :type device_key: str
        :param configuration: Current configuration data
        :type configuration: dict

        :returns: message
        :rtype: Message
        """
        pass
