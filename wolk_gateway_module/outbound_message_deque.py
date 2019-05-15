"""Store data before publishing."""
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

from collections import deque
from typing import Optional, List

from wolk_gateway_module.persistance.outbound_message_queue import (
    OutboundMessageQueue,
)
from wolk_gateway_module.model.message import Message


class OutboundMessageDeque(OutboundMessageQueue):
    """
    Responsible for storing messages before being sent to WolkGateway.

    Messages are sent in the order they were added to the queue.

    Storing readings and alarms without Unix timestamp will result
    in all sent messages being treated as live readings and
    will be assigned a timestamp upon reception, so for a valid
    history add timestamps to readings via `int(round(time.time() * 1000))`
    """

    def __repr__(self) -> str:
        """Make string representation of OutboundMessageDeque.

        :returns: representation
        :rtype: str
        """
        return "OutboundMessageDeque()"

    def __init__(self):
        """Initialize a double ended queue for storing messages."""
        self.queue = deque()

    def put(self, message: Message) -> bool:
        """
        Place a message in storage.

        :param message: Message to be stored
        :type message: wolk_gateway_module.model.message.Message

        :returns: result
        :rtype: bool
        """
        self.queue.append(message)
        return True

    def remove(self, message: Message) -> bool:
        """
        Remove specific message from storage.

        :returns: result
        :rtype: bool
        """
        if message in self.queue:
            self.queue.remove(message)
            return True
        return True

    def get_messages_for_device(self, device_key: str) -> List[Message]:
        """
        Return a list of messages that belong to a certain device.

        Does not remove from storage.

        :param device_key: Device identifier
        :type device_key: str

        :returns: messages
        :rtype: List[Message]
        """
        if self.queue_size() == 0:
            return []
        messages = []
        for message in self.queue:
            if device_key in message.topic:
                messages.append(message)
        return messages

    def get(self) -> Optional[Message]:
        """
        Get the first message from storage.

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message, None
        """
        try:
            return self.queue.popleft()
        except IndexError:
            return None

    def queue_size(self) -> int:
        """
        Return current number of messages in storage.

        :returns: size
        :rtype: int
        """
        return len(self.queue)
