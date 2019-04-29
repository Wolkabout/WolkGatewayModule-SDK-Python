"""Tests for JsonRegistrationProtocol."""
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

import unittest

import sys

sys.path.append("..")  # noqa

from wolk_gateway_module.json_registration_protocol import (
    JsonRegistrationProtocol,
)


class JsonRegistrationProtocolTests(unittest.TestCase):
    """JsonRegistrationProtocol Tests."""

    DEVICE_PATH_PREFIX = "d/"
    CHANNEL_WILDCARD = "#"
    DEVICE_REGISTRATION_REQUEST_TOPIC_ROOT = "d2p/register_subdevice_request/"
    DEVICE_REGISTRATION_RESPONSE_TOPIC_ROOT = (
        "p2d/register_subdevice_response/"
    )

    def test_get_inbound_topics(self):
        """Test that returned list is correct."""

        # set up
        json_registration_protocol = JsonRegistrationProtocol()

        self.assertEqual(
            json_registration_protocol.get_inbound_topics(),
            [
                self.DEVICE_REGISTRATION_RESPONSE_TOPIC_ROOT
                + self.DEVICE_PATH_PREFIX
                + self.CHANNEL_WILDCARD
            ],
        )
