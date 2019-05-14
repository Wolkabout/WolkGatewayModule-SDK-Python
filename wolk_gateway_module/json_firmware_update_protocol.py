"""Handling of messages related to device firmware update."""
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

from wolk_gateway_module.protocol.firmware_update_protocol import (
    FirmwareUpdateProtocol,
)
from wolk_gateway_module.model.firmware_update_status import (
    FirmwareUpdateStatus,
    FirmwareUpdateState,
    FirmwareUpdateErrorCode,
)
from wolk_gateway_module.model.message import Message


class JsonFirmwareUpdateProtocol(FirmwareUpdateProtocol):
    """Parse inbound messages and serialize outbound firmware messages."""

    DEVICE_PATH_PREFIX = "d/"
    FIRMWARE_UPDATE_INSTALL_TOPIC_ROOT = "p2d/firmware_update_install/"
    FIRMWARE_UPDATE_ABORT_TOPIC_ROOT = "p2d/firmware_update_abort/"
    FIRMWARE_UPDATE_STATUS_TOPIC_ROOT = "d2p/firmware_update_status/"
    FIRMWARE_VERSION_UPDATE_TOPIC_ROOT = "d2p/firmware_version_update/"

    def __repr__(self) -> str:
        """Make string representation of JsonFirmwareUpdateProtocol.

        :returns: representation
        :rtype: str
        """
        return "JsonFirmwareUpdateProtocol()"

    def get_inbound_topics_for_device(self, device_key: str) -> list:
        """Return list of inbound topics for given device key.

        :param device_key: Device key for which to create topics
        :type device_key: str

        :returns: inbound_topics
        :rtype: list
        """
        return [
            self.FIRMWARE_UPDATE_INSTALL_TOPIC_ROOT
            + self.DEVICE_PATH_PREFIX
            + device_key,
            self.FIRMWARE_UPDATE_ABORT_TOPIC_ROOT
            + self.DEVICE_PATH_PREFIX
            + device_key,
        ]

    def make_firmware_update_status_message(
        self, device_key: str, status: FirmwareUpdateStatus
    ) -> Message:
        """Make message from device firmware update status.

        :param device_key: Device key to which the firmware update status belongs to
        :type device_key: str
        :param status: Device firmware update status
        :type status: wolk_gateway_module.model.firmware_update_status.FirmwareUpdateStatus

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        topic = (
            self.FIRMWARE_UPDATE_STATUS_TOPIC_ROOT
            + self.DEVICE_PATH_PREFIX
            + device_key
        )
        payload = {"status": status.status.value}
        if status.error_code:
            payload["error"] = status.error_code.value

        return Message(topic, json.dumps(payload))

    def make_firmware_version_message(
        self, device_key: str, firmware_verison: str
    ) -> Message:
        """Make message from device firmware update version.

        :param device_key: Device key to which the firmware update belongs to
        :type device_key: str
        :param firmware_verison: Current firmware version
        :type firmware_verison: str

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        topic = (
            self.FIRMWARE_VERSION_UPDATE_TOPIC_ROOT
            + self.DEVICE_PATH_PREFIX
            + device_key
        )
        payload = str(firmware_verison)

        return Message(topic, payload)

    def is_firmware_install_command(self, message: Message) -> bool:
        """Check if received message is firmware install command.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: is_firmware_install_command
        :rtype: bool
        """
        return message.topic.startswith(
            self.FIRMWARE_UPDATE_INSTALL_TOPIC_ROOT
        )

    def is_firmware_abort_command(self, message: Message) -> bool:
        """Check if received message is firmware abort command.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: is_firmware_abort_command
        :rtype: bool
        """
        return message.topic.startswith(self.FIRMWARE_UPDATE_ABORT_TOPIC_ROOT)

    def make_firmware_file_path(self, message: Message) -> str:
        """Extract file path from firmware install message.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: firmware_file_path
        :rtype: str
        """
        payload = json.loads(message.payload)
        return payload["fileName"]

    def extract_device_key_from_message(self, message: Message) -> str:
        """Return device key from message.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: device_key
        :rtype: str
        """
        return message.topic.split("/")[-1]
