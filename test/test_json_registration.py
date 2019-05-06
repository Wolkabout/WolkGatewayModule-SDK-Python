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

import json
import unittest

import sys

sys.path.append("..")  # noqa

from wolk_gateway_module.json_registration_protocol import (
    JsonRegistrationProtocol,
)
from wolk_gateway_module.model.message import Message
from wolk_gateway_module.protocol.registration_protocol import (
    RegistrationProtocol,
)
from wolk_gateway_module.model.device_registration_request import (
    DeviceRegistrationRequest,
)
from wolk_gateway_module.model.device_registration_response import (
    DeviceRegistrationResponse,
)
from wolk_gateway_module.model.device_registration_response_result import (
    DeviceRegistrationResponseResult,
)
from wolk_gateway_module.model.device_template import DeviceTemplate
from wolk_gateway_module.model.reading_type_name import ReadingTypeName
from wolk_gateway_module.model.reading_type_measurement_unit import (
    ReadingTypeMeasurementUnit,
)
from wolk_gateway_module.model.actuator_template import ActuatorTemplate
from wolk_gateway_module.model.alarm_template import AlarmTemplate
from wolk_gateway_module.model.configuration_template import (
    ConfigurationTemplate,
)
from wolk_gateway_module.model.sensor_template import SensorTemplate


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
        json_registration_protocol = JsonRegistrationProtocol()

        self.assertEqual(
            json_registration_protocol.get_inbound_topics(),
            [
                self.DEVICE_REGISTRATION_RESPONSE_TOPIC_ROOT
                + self.DEVICE_PATH_PREFIX
                + self.CHANNEL_WILDCARD
            ],
        )

    def test_extract_device_key_from_message(self):
        """Test that device key is extracted."""
        json_registration_protocol = JsonRegistrationProtocol()
        device_key = "some_device_key"

        message = Message(
            self.DEVICE_REGISTRATION_RESPONSE_TOPIC_ROOT
            + self.DEVICE_PATH_PREFIX
            + device_key
        )

        self.assertEqual(
            json_registration_protocol.extract_device_key_from_message(
                message
            ),
            device_key,
        )

    def test_is_device_registration_response_message(self):
        """Test that message is device registration response."""
        json_registration_protocol = JsonRegistrationProtocol()

        message = Message(self.DEVICE_REGISTRATION_RESPONSE_TOPIC_ROOT)

        self.assertEqual(
            json_registration_protocol.is_device_registration_response_message(
                message
            ),
            True,
        )

    def test_make_device_registration_request_message(self):
        """Test registration request for empty device template."""
        json_registration_protocol = JsonRegistrationProtocol()

        device_template = DeviceTemplate()
        device_name = "device_name"
        device_key = "device_key"

        device_registration_request = DeviceRegistrationRequest(
            device_name, device_key, device_template
        )

        expected_payload = json.loads(
            "{"
            + '"name": "device_name",'
            + '"deviceKey": "device_key",'
            + '"defaultBinding": true,'
            + '"sensors": [],'
            + '"actuators": [],'
            + '"alarms": [],'
            + '"configurations": [],'
            + '"typeParameters": {},'
            + '"connectivityParameters": {},'
            + '"firmwareUpdateParameters": {"supportsFirmwareUpdate": false}'
            + "}"
        )

        message = json_registration_protocol.make_device_registration_request_message(
            device_registration_request
        )

        self.assertEqual(expected_payload, json.loads(message.payload))


if __name__ == "__main__":
    unittest.main()
