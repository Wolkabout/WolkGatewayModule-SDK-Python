"""Handling of inbound and outbound messages related to device status."""
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

from wolk_gateway_module.model.device_status import DeviceStatus
from wolk_gateway_module.model.message import Message
from wolk_gateway_module.protocol.status_protocol import StatusProtocol


class JsonStatusProtocol(StatusProtocol):
    """Parse inbound messages and serialize device status messages."""

    DEVICE_PATH_PREFIX = "d/"
    DEVICE_STATUS_UPDATE_TOPIC_ROOT = "d2p/subdevice_status_update/"
    DEVICE_STATUS_RESPONSE_TOPIC_ROOT = "d2p/subdevice_status_response/"
    DEVICE_STATUS_REQUEST_TOPIC_ROOT = "p2d/subdevice_status_request/"
    LAST_WILL_TOPIC = "lastwill"

    def __repr__(self) -> str:
        """Make string representation of JsonStatusProtocol.

        :returns: representation
        :rtype: str
        """
        return "JsonStatusProtocol()"

    def get_inbound_topics_for_device(self, device_key: str) -> list:
        """Return list of inbound topics for given device key.

        :param device_key: Device key for which to create topics
        :type device_key: str

        :returns: inbound_topics
        :rtype: list
        """
        return [
            self.DEVICE_STATUS_REQUEST_TOPIC_ROOT
            + self.DEVICE_PATH_PREFIX
            + device_key
        ]

    def is_device_status_request_message(self, message: Message) -> bool:
        """Check if message is device status request.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: is_device_status_request
        :rtype: bool
        """
        return message.topic.startswith(self.DEVICE_STATUS_REQUEST_TOPIC_ROOT)

    def make_device_status_response_message(
        self, device_key: str, device_status: DeviceStatus
    ) -> Message:
        """Make message from device status response.

        :param device_status: Device's current status
        :type device_status: wolk_gateway_module.model.device_status.DeviceStatus
        :param device_key: Device to which the status belongs to
        :type device_key: str

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        return Message(
            self.DEVICE_STATUS_RESPONSE_TOPIC_ROOT
            + self.DEVICE_PATH_PREFIX
            + device_key,
            json.dumps({"state": device_status.value}),
        )

    def make_device_status_update_message(
        self, device_key: str, device_status: DeviceStatus
    ) -> Message:
        """Make message from device status update.

        :param device_status: Device's current status
        :type device_status: wolk_gateway_module.model.device_status.DeviceStatus
        :param device_key: Device to which the status belongs to
        :type device_key: str

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        return Message(
            self.DEVICE_STATUS_UPDATE_TOPIC_ROOT
            + self.DEVICE_PATH_PREFIX
            + device_key,
            json.dumps({"state": device_status.value}),
        )

    def make_last_will_message(self, device_keys: list) -> Message:
        """Make last will message from list of device keys.

        :param device_keys: List of device keys
        :type device_keys: list(str)

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        return Message(self.LAST_WILL_TOPIC, json.dumps(device_keys))
