"""Tests for MQTTConnectivityService."""
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

import sys
import unittest

sys.path.append("..")  # noqa

from paho.mqtt import client as mqtt

from wolk_gateway_module.mqtt_connectivity_service import (
    MQTTConnectivityService,
)
from wolk_gateway_module.model.message import Message


class MQTTConnectivityServiceTests(unittest.TestCase):
    """MQTTConnectivityService Tests."""

    def mock_listener(self, message):
        """Mock function for inbound message listener."""
        self.message = message

    def set_up(self):
        """Prepare context for testing."""
        self.host = "localhost"
        self.port = 1883
        self.client_id = "WolkGatewayModule-SDK-Python"
        self.qos = 0
        self.lastwill_message = Message("lastwill")
        self.topics = []
        self.listener = self.mock_listener
        self.message = None
        self.mqttcs = MQTTConnectivityService(
            self.host,
            self.port,
            self.client_id,
            self.qos,
            self.lastwill_message,
            self.topics,
        )

    def tear_down(self):
        """Clean context from completed test."""
        self.host = None
        self.port = None
        self.client_id = None
        self.qos = None
        self.lastwill_message = None
        self.topics = None
        self.listener = None
        self.mqttcs = None
        self.message = None

    def test_set_inbound_message_listener(self):
        """Test that inbound message listener is set correctly."""
        self.set_up()

        self.mqttcs.set_inbound_message_listener(self.mock_listener)

        self.assertEqual(
            self.mock_listener, self.mqttcs.inbound_message_listener
        )

        self.tear_down()

    def test_inbound_message_listener(self):
        """Test that inbound message listener is called correctly."""
        self.set_up()

        self.mqttcs.set_inbound_message_listener(self.mock_listener)

        expected = Message("test_message")

        self.mqttcs._on_mqtt_message(None, None, expected)

        self.assertEqual(expected, self.message)

        self.tear_down()

    def test_connect(self):
        """Test that connect is called correctly."""
        self.set_up()

        self.mqttcs.set_inbound_message_listener(self.mock_listener)

        self.tear_down()


if __name__ == "__main__":
    unittest.main()