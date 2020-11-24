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
import logging
import sys
import unittest
from unittest.mock import MagicMock

sys.path.append("..")  # noqa

from wolk_gateway_module.mqtt_connectivity_service import (
    MQTTConnectivityService,
)
from wolk_gateway_module.model.message import Message


class MQTTConnectivityServiceTests(unittest.TestCase):
    """MQTTConnectivityService Tests."""

    def mock_listener(self, message):
        """Mock function for inbound message listener."""
        self.message = message

    def setUp(self):
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
        self.mqttcs.log.setLevel(logging.CRITICAL)

    def tearDown(self):
        """Clean context from completed test."""
        self.mqttcs.disconnect()
        for handler in self.mqttcs.log.handlers:
            handler.close()
        self.mqttcs = None

    def test_set_inbound_message_listener(self):
        """Test that inbound message listener is set correctly."""
        self.mqttcs.set_inbound_message_listener(self.mock_listener)

        self.assertEqual(
            self.mock_listener, self.mqttcs.inbound_message_listener
        )

    def test_set_lastwill_message(self):
        """Test that lastwill message is set correctly."""
        message = Message("lastwill")

        self.mqttcs.set_lastwill_message(message)

        self.assertEqual(message, self.mqttcs.lastwill_message)

    def test_set_lastwill_message_when_connected(self):
        """Test that lastwill message is set correctly when connected."""
        message = Message("lastwill")
        self.mqttcs.disconnect = MagicMock()
        self.mqttcs.connect = MagicMock()
        self.mqttcs._connected = True

        self.mqttcs.set_lastwill_message(message)

        self.assertEqual(message, self.mqttcs.lastwill_message)

    def test_add_subscription_topics(self):
        """Test adding subscription topics."""
        topics = ["topic1", "topic2", "topic3"]

        self.mqttcs.add_subscription_topics(topics)

        self.assertEqual(3, len(self.mqttcs.topics))

    def test_remove_topics_for_device(self):
        """Test removing topics from subscription topics."""
        self.mqttcs.topics = ["key1", "key2", "key3", "key1"]

        device_key = "key1"

        self.mqttcs.remove_topics_for_device(device_key)

        self.assertEqual(2, len(self.mqttcs.topics))

    def test_remove_topics_when_no_topics(self):
        """Test removing topics from subscription topics."""
        self.mqttcs.topics = []

        device_key = "key1"

        self.mqttcs.remove_topics_for_device(device_key)

        self.assertEqual(0, len(self.mqttcs.topics))

    def test_inbound_message_listener(self):
        """Test that inbound message listener is called correctly."""
        self.mqttcs.set_inbound_message_listener(self.mock_listener)

        expected = Message("test_message")

        self.mqttcs._on_mqtt_message(None, None, expected)

        self.assertEqual(expected, self.message)

    def test_connected(self):
        """Test connected returns false."""
        self.mqttcs.client.is_connected = MagicMock(return_value=False)
        self.assertFalse(self.mqttcs.connected())

    def test_reconnect(self):
        """Test that reconnection method will call connect."""
        self.mqttcs.connected_rc = 0

        self.mqttcs.connect = MagicMock(return_value=True)

        self.assertTrue(self.mqttcs.reconnect())

    def test_publish_fails(self):
        """Test that publishing fails when not connected."""
        message = Message("test")

        self.assertFalse(self.mqttcs.publish(message))


if __name__ == "__main__":
    unittest.main()
