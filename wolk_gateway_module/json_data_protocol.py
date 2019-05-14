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

import json

from wolk_gateway_module.model.actuator_command import (
    ActuatorCommand,
    ActuatorCommandType,
)
from wolk_gateway_module.model.actuator_state import ActuatorState
from wolk_gateway_module.model.actuator_status import ActuatorStatus
from wolk_gateway_module.model.alarm import Alarm
from wolk_gateway_module.model.configuration_command import (
    ConfigurationCommand,
    ConfigurationCommandType,
)
from wolk_gateway_module.model.message import Message
from wolk_gateway_module.model.sensor_reading import SensorReading
from wolk_gateway_module.protocol.data_protocol import DataProtocol


class JsonDataProtocol(DataProtocol):
    """Parse inbound messages and serialize outbound messages."""

    DEVICE_PATH_PREFIX = "d/"
    REFERENCE_PATH_PREFIX = "r/"
    CHANNEL_WILDCARD = "#"
    SENSOR_READING = "d2p/sensor_reading/"
    AlARM = "d2p/events/"
    ACTUATOR_SET = "p2d/actuator_set/"
    ACTUATOR_GET = "p2d/actuator_get/"
    ACTUATOR_STATUS = "d2p/actuator_status/"
    CONFIGURATION_SET = "p2d/configuration_set/"
    CONFIGURATION_GET = "p2d/configuration_get/"
    CONFIGURATION_STATUS = "d2p/configuration_get/"

    def __repr__(self):
        """Make string representation of JsonDataProtocol.

        :returns: representation
        :rtype: str
        """
        return "JsonDataProtocol()"

    def get_inbound_topics_for_device(self, device_key: str) -> list:
        """Return list of inbound topics for given device key.

        :param device_key: Device key for which to create topics
        :type device_key: str

        :returns: inbound_topics
        :rtype: list
        """
        return [
            self.ACTUATOR_SET
            + self.DEVICE_PATH_PREFIX
            + device_key
            + self.REFERENCE_PATH_PREFIX
            + self.CHANNEL_WILDCARD,
            self.ACTUATOR_GET
            + self.DEVICE_PATH_PREFIX
            + device_key
            + self.REFERENCE_PATH_PREFIX
            + self.CHANNEL_WILDCARD,
            self.CONFIGURATION_SET + self.DEVICE_PATH_PREFIX + device_key,
            self.CONFIGURATION_GET + self.DEVICE_PATH_PREFIX + device_key,
        ]

    def is_actuator_get_message(self, message: Message) -> bool:
        """Check if message is actuator get command.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: is_actuator_get_message
        :rtype: bool
        """
        return message.topic.startswith(self.ACTUATOR_GET)

    def is_actuator_set_message(self, message: Message) -> bool:
        """Check if message is actuator set command.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: is_actuator_set_message
        :rtype: bool
        """
        return message.topic.startswith(self.ACTUATOR_SET)

    def is_configuration_get_message(self, message: Message) -> bool:
        """Check if message is configuration get command.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: is_configuration_get_message
        :rtype: bool
        """
        return message.topic.startswith(self.CONFIGURATION_GET)

    def is_configuration_set_message(self, message: Message) -> bool:
        """Check if message is configuration set command.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: is_configuration_set_message
        :rtype: bool
        """
        return message.topic.startswith(self.CONFIGURATION_SET)

    def make_actuator_command(self, message: Message) -> ActuatorCommand:
        """Make actuator command from message.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: actuator_command
        :rtype: wolk_gateway_module.model.actuator_command.ActuatorCommand
        """
        reference = message.topic.split("/")[-1]
        if self.is_actuator_set_message(message):
            command = ActuatorCommandType.SET
            payload = json.loads(message.payload)
            value = payload["value"]
        elif self.is_actuator_get_message(message):
            command = ActuatorCommandType.GET
            value = None

        return ActuatorCommand(reference, command, value)

    def make_configuration_command(
        self, message: Message
    ) -> ConfigurationCommand:
        """Make configuration command from message.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: configuration_command
        :rtype: wolk_gateway_module.model.configuration_command.ConfigurationCommand
        """
        if self.is_configuration_set_message(message):
            command = ConfigurationCommandType.SET
            payload = json.loads(message.payload)
            values = payload["values"]
            for reference, value in values.items():
                if "\n" in str(value):
                    value = value.replace("\n", "\\n")
                    value = value.replace("\r", "")

                if isinstance(value, bool):
                    pass
                else:
                    if "," in value:
                        values_list = value.split(",")
                        try:
                            if any("." in value for value in values_list):
                                values_list = [
                                    float(value) for value in values_list
                                ]
                            else:
                                values_list = [
                                    int(value) for value in values_list
                                ]
                        except ValueError:
                            pass
                        values[reference] = tuple(values_list)
        elif self.is_configuration_get_message(message):
            command = ConfigurationCommandType.GET
            values = None

        return ConfigurationCommand(command, values)

    def make_sensor_reading_message(
        self, device_key: str, sensor_reading: SensorReading
    ) -> Message:
        """Make message from sensor reading for device key.

        :param device_key: Device on which the sensor reading occurred
        :type device_key: str
        :param sensor_reading: Sensor reading data
        :type sensor_reading: wolk_gateway_module.model.sensor_reading.SensorReading

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        topic = (
            self.SENSOR_READING
            + self.DEVICE_PATH_PREFIX
            + device_key
            + self.REFERENCE_PATH_PREFIX
            + sensor_reading.reference
        )

        if isinstance(sensor_reading.value, tuple):
            delimiter = ","
            values_list = list()
            for value in sensor_reading.value:
                values_list.append(value)
                values_list.append(delimiter)
            values_list.pop()
            sensor_reading.value = "".join(map(str, values_list))

        payload = json.dumps(
            {
                "data": str(sensor_reading.value),
                "utc": sensor_reading.timestamp,
            }
        )

        return Message(topic, payload)

    def make_alarm_message(self, device_key: str, alarm: Alarm) -> Message:
        """Make message from alarm for device key.

        :param device_key: Device on which the alarm occurred
        :type device_key: str
        :param alarm: Alarm data
        :type alarm: wolk_gateway_module.model.alarm.Alarm

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        topic = (
            self.AlARM
            + self.DEVICE_PATH_PREFIX
            + device_key
            + self.REFERENCE_PATH_PREFIX
            + alarm.reference
        )
        payload = json.dumps({"data": alarm.active, "utc": alarm.timestamp})

        return Message(topic, payload)

    def make_actuator_status_message(
        self, device_key: str, actuator_status: ActuatorStatus
    ) -> Message:
        """Make message from actuator status for device key.

        :param device_key: Device on which the actuator status occurred
        :type device_key: str
        :param actuator_status: Actuator status data
        :type actuator_status: wolk_gateway_module.model.actuator_status.ActuatorStatus

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        topic = (
            self.ACTUATOR_STATUS
            + self.DEVICE_PATH_PREFIX
            + device_key
            + self.REFERENCE_PATH_PREFIX
            + actuator_status.reference
        )

        if isinstance(actuator_status.value, tuple):
            delimiter = ","
            values_list = list()
            for value in actuator_status.value:
                values_list.append(value)
                values_list.append(delimiter)
            values_list.pop()
            actuator_status.value = "".join(map(str, values_list))

        payload = json.dumps(
            {
                "status": actuator_status.state.value,
                "value": str(actuator_status.value),
            }
        )

        return Message(topic, payload)

    def make_configuration_message(
        self, device_key: str, configuration: dict
    ) -> Message:
        """Make message from configuration for device key.

        :param device_key: Device to which the configuration belongs to.
        :type device_key: str
        :param configuration: Current configuration data
        :type configuration: dict

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        topic = (
            self.CONFIGURATION_STATUS + self.DEVICE_PATH_PREFIX + device_key
        )

        for reference, config_value in configuration.items():
            if isinstance(config_value, tuple):
                delimiter = ","
                values_list = list()
                for value in config_value:
                    if value is True:
                        value = "true"
                    elif value is False:
                        value = "false"
                    if "\n" in str(value):
                        value = value.replace("\n", "\\n")
                        value = value.replace("\r", "")
                    if '"' in str(value):
                        value = value.replace('"', '\\"')
                    values_list.append(value)
                    values_list.append(delimiter)
                values_list.pop()
                configuration[reference] = "".join(map(str, values_list))
            else:
                if config_value is True:
                    config_value = "true"
                elif config_value is False:
                    config_value = "false"
                configuration[reference] = str(config_value)

        payload = json.dumps({"values": configuration})

        return Message(topic, payload)
