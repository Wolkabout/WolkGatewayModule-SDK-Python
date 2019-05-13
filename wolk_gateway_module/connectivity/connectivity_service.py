"""Service for exchanging data with WolkGateway."""
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


class ConnectivityService(ABC):
    """Responsible for exchanging data with WolkGateway."""

    @abstractmethod
    def set_inbound_message_listener(self, on_inbound_message):
        """Set the callback function to handle inbound messages.

        :param on_inbound_message: Callable that handles inbound messages
        :type on_inbound_message: callable[str]
        """
        pass

    @abstractmethod
    def connect(self):
        """Establish connection with WolkGateway."""
        pass

    @abstractmethod
    def reconnect(self):
        """Reestablish connection with WolkGateway."""
        pass

    @abstractmethod
    def disconnect(self):
        """Terminate connection with WolkGateway."""
        pass

    @abstractmethod
    def publish(self, message):
        """Publish serialized data to WolkGateway.

        :param message: Message to be published
        :type message: wolk_gateway_module.model.message.Message
        :returns: result
        :rtype: bool
        """