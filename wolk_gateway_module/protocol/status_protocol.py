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

from abc import ABC, abstractmethod


class StatusProtocol(ABC):
    """Parse inbound messages and serialize outbound messages."""

    @abstractmethod
    def is_device_status_request_message(self, message):
        """Check if message is device status request.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: is_device_status_request
        :rtype: bool
        """
        pass

    @abstractmethod
    def make_device_status_response_message(self, device_status):
        """Make message from device status response.

        :param device_status: Device's current status
        :type device_status: wolk_gateway_module.model.device_status.DeviceStatus
        """
        pass

    @abstractmethod
    def make_last_will_message(self, device_keys):
        """Make last will message from list of device keys.

        :param device_keys: List of device keys
        :type device_keys: list(str)

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        pass

    @abstractmethod
    def make_ping_request_message(self, device_key):
        """Make message for ping request for device key.

        :param device_key: Device requesting ping
        :type device_key: str

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        pass
