"""Tests for Wolk."""
#   Copyright 2020 WolkAbout Technology s.r.o.
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
from typing import List

sys.path.append("..")  # noqa

from wolk_gateway_module.connectivity.connectivity_service import (
    ConnectivityService,
)
from wolk_gateway_module.wolk import Wolk
from wolk_gateway_module.model.actuator_state import ActuatorState
from wolk_gateway_module.model.device import Device
from wolk_gateway_module.model.device_template import DeviceTemplate
from wolk_gateway_module.model.message import Message
from wolk_gateway_module.model.device_status import DeviceStatus
from wolk_gateway_module.interface.firmware_handler import FirmwareHandler
from wolk_gateway_module.model.firmware_update_status import (
    FirmwareUpdateStatus,
    FirmwareUpdateState,
)
from wolk_gateway_module.model.sensor_template import SensorTemplate
from wolk_gateway_module.model.data_type import DataType
from wolk_gateway_module.json_data_protocol import JsonDataProtocol
from wolk_gateway_module.json_status_protocol import JsonStatusProtocol
from wolk_gateway_module.json_firmware_update_protocol import (
    JsonFirmwareUpdateProtocol,
)
from wolk_gateway_module.json_registration_protocol import (
    JsonRegistrationProtocol,
)
from wolk_gateway_module.outbound_message_deque import OutboundMessageDeque


class MockConnectivityService(ConnectivityService):

    _connected = False
    _topics: List[str] = []

    def set_inbound_message_listener(self, on_inbound_message):
        pass

    def set_lastwill_message(self, message):
        self._lastwill = message

    def add_subscription_topics(self, topics):
        self._topics.extend(topics)

    def remove_topics_for_device(self, device_key):
        pass

    def connected(self):
        return self._connected

    def connect(self):
        return self._connected

    def reconnect(self):
        return self._connected

    def disconnect(self):
        pass

    def publish(self, message):
        return self._connected


actuator_1 = False
actuator_2 = 0
actuator_3 = "default"


def mock_actuator_handler(device_key, reference, value):
    if device_key == "key1":
        if reference == "REF1":
            global actuator_1
            actuator_1 = value
        elif reference == "REF2":
            global actuator_2
            actuator_2 = value
    elif device_key == "key2":
        if reference == "REF3":
            global actuator_3
            actuator_3 = value


def mock_actuator_status_provider(device_key, reference):
    if device_key == "key1":
        if reference == "REF1":
            global actuator_1
            return ActuatorState.READY, actuator_1
        elif reference == "REF2":
            global actuator_2
            return ActuatorState.READY, actuator_2
    elif device_key == "key2":
        if reference == "REF3":
            global actuator_3
            return ActuatorState.READY, actuator_3


configuration_1 = False
configuration_2 = 3.14
configuration_3 = ("string1", "string2")


def mock_configuration_provider(device_key):
    if device_key == "key1":
        global configuration_1
        global configuration_2
        return {
            "configuration_1": configuration_1,
            "configuration_2": configuration_2,
        }
    elif device_key == "key2":
        global configuration_3
        return {"configuration_3": configuration_3}


def mock_configuration_handler(device_key, configuration):
    if device_key == "key1":
        global configuration_1
        global configuration_2
        for key, value in configuration.items():
            if key == "configuration_1":
                configuration_1 = value
            elif key == "configuration_2":
                configuration_2 = value
    elif device_key == "key2":
        global configuration_3
        for key, value in configuration.items():
            if key == "configuration_3":
                configuration_3 = value


class MockFirmwareHandler(FirmwareHandler):
    def install_firmware(
        self, device_key: str, firmware_file_path: str
    ) -> None:
        if device_key == "key1":
            self.on_install_success(device_key)

    def abort_installation(self, device_key: str) -> None:
        if device_key == "key1":
            status = FirmwareUpdateStatus(FirmwareUpdateState.ABORTED)
            self.on_install_fail(device_key, status)

    def get_firmware_version(self, device_key: str) -> str:
        if device_key == "key1":
            return "v1.0"
        elif device_key == "key2":
            return "v0.1"


class WolkTests(unittest.TestCase):
    """Wolk Tests."""

    def test_bad_status_provider_callable(self):
        """Test that exception is raised for bad device status provider."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host", 1883, "module_name", lambda a, b: a * b
            )

    def test_bad_status_provider_not_callable(self):
        """Test that exception is raised for bad device status provider."""
        with self.assertRaises(ValueError):
            wolk = Wolk("host", 1883, "module_name", False)  # noqa

    def test_add_sensor_reading(self):
        """Test adding a sensor reading to storage and then publish."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            connectivity_service=MockConnectivityService(),
        )
        wolk.add_sensor_reading("device_key", "REF", 13)
        self.assertEqual(1, wolk.outbound_message_queue.queue_size())
        wolk.connectivity_service._connected = True
        wolk.publish()
        self.assertEqual(0, wolk.outbound_message_queue.queue_size())

    def test_add_alarm(self):
        """Test adding a alarm event to storage and then publish."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            connectivity_service=MockConnectivityService(),
        )
        wolk.add_alarm("device_key", "REF", False)
        self.assertEqual(1, wolk.outbound_message_queue.queue_size())
        wolk.connectivity_service._connected = True
        wolk.publish()
        self.assertEqual(0, wolk.outbound_message_queue.queue_size())

    def test_publish_actuator(self):
        """Test publishing actuator status."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            connectivity_service=MockConnectivityService(),
            actuation_handler=mock_actuator_handler,
            actuator_status_provider=mock_actuator_status_provider,
        )
        wolk.log.setLevel(logging.CRITICAL)
        wolk.publish_actuator_status("key1", "REF1")
        self.assertEqual(1, wolk.outbound_message_queue.queue_size())
        wolk.connectivity_service._connected = True
        wolk.publish()
        self.assertEqual(0, wolk.outbound_message_queue.queue_size())

    def test_publish_actuator_explicit(self):
        """Test publishing explicit actuator status."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            connectivity_service=MockConnectivityService(),
            actuation_handler=mock_actuator_handler,
            actuator_status_provider=mock_actuator_status_provider,
        )
        wolk.log.setLevel(logging.CRITICAL)
        wolk.publish_actuator_status("key1", "REF1", ActuatorState.READY, True)
        self.assertEqual(1, wolk.outbound_message_queue.queue_size())
        wolk.connectivity_service._connected = True
        wolk.publish()
        self.assertEqual(0, wolk.outbound_message_queue.queue_size())

    def test_receive_actuation(self):
        """Test receiving actuator set command."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: DeviceStatus.CONNECTED,
            connectivity_service=MockConnectivityService(),
            actuation_handler=mock_actuator_handler,
            actuator_status_provider=mock_actuator_status_provider,
        )
        wolk.log.setLevel(logging.CRITICAL)
        wolk.connectivity_service._connected = True
        message = Message("p2d/actuator_set/d/key1/r/REF2", '{"value": "3"}')
        wolk._on_inbound_message(message)

        global actuator_2
        self.assertEqual(3, actuator_2)

    def test_publish_configuration(self):
        """Test publishing configuration."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            connectivity_service=MockConnectivityService(),
            configuration_handler=mock_configuration_handler,
            configuration_provider=mock_configuration_provider,
        )
        wolk.log.setLevel(logging.CRITICAL)
        wolk.publish_configuration("key1")
        self.assertEqual(1, wolk.outbound_message_queue.queue_size())
        wolk.connectivity_service._connected = True
        wolk.publish()
        self.assertEqual(0, wolk.outbound_message_queue.queue_size())

    def test_receive_configuration(self):
        """Test receiving configuration set command."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: DeviceStatus.CONNECTED,
            connectivity_service=MockConnectivityService(),
            configuration_handler=mock_configuration_handler,
            configuration_provider=mock_configuration_provider,
        )
        wolk.log.setLevel(logging.CRITICAL)
        wolk.connectivity_service._connected = True
        message = Message(
            "p2d/configuration_set/d/key1",
            '{"configuration_1": "true", "configuration_2": "4.2"}',
        )
        wolk._on_inbound_message(message)

        self.assertEqual(True, configuration_1)
        self.assertEqual(4.2, configuration_2)

        message = Message(
            "p2d/configuration_set/d/key2",
            '{"configuration_3": "newstring1,newstring2"}',
        )
        wolk._on_inbound_message(message)

        self.assertEqual(("newstring1", "newstring2"), configuration_3)

    def test_publish_device_status(self):
        """Test sending device status."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda device_key: DeviceStatus.CONNECTED,
            connectivity_service=MockConnectivityService(),
        )
        wolk.log.setLevel(logging.CRITICAL)
        wolk.publish_device_status("key1")
        self.assertEqual(1, wolk.outbound_message_queue.queue_size())
        wolk.connectivity_service._connected = True
        wolk.publish()
        self.assertEqual(0, wolk.outbound_message_queue.queue_size())

    def test_publish_device_status_explicit(self):
        """Test sending explicit device status."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda device_key: DeviceStatus.CONNECTED,
            connectivity_service=MockConnectivityService(),
        )
        wolk.log.setLevel(logging.CRITICAL)
        wolk.publish_device_status("key1", DeviceStatus.OFFLINE)
        self.assertEqual(1, wolk.outbound_message_queue.queue_size())
        wolk.connectivity_service._connected = True
        wolk.publish()
        self.assertEqual(0, wolk.outbound_message_queue.queue_size())

    def test_on_status_request(self):
        """Test receiving device status request."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda device_key: DeviceStatus.CONNECTED,
            connectivity_service=MockConnectivityService(),
        )
        wolk.log.setLevel(logging.CRITICAL)
        message = Message("p2d/subdevice_status_request/d/key1")
        wolk._on_inbound_message(message)

        self.assertEqual(1, wolk.outbound_message_queue.queue_size())

    def test_firmware_update(self):
        """Test receiving firmware installation command."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda device_key: DeviceStatus.CONNECTED,
            connectivity_service=MockConnectivityService(),
            firmware_handler=MockFirmwareHandler(),
        )
        wolk.log.setLevel(logging.CRITICAL)

        message = Message(
            "p2d/firmware_update_install/d/key1", '{ "fileName": "some_path"}'
        )

        wolk._on_inbound_message(message)
        self.assertEqual(3, wolk.outbound_message_queue.queue_size())

    def test_firmware_abort(self):
        """Test receiving firmware abort command."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda device_key: DeviceStatus.CONNECTED,
            connectivity_service=MockConnectivityService(),
            firmware_handler=MockFirmwareHandler(),
        )
        wolk.log.setLevel(logging.CRITICAL)

        message = Message("p2d/firmware_update_abort/d/key1")

        wolk._on_inbound_message(message)
        self.assertEqual(1, wolk.outbound_message_queue.queue_size())

    def test_add_simple_device(self):
        """Test adding a simple device."""
        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda device_key: DeviceStatus.CONNECTED,
            connectivity_service=MockConnectivityService(),
        )
        wolk.log.setLevel(logging.CRITICAL)

        sensor1 = SensorTemplate("sensor1", "s1", DataType.NUMERIC)

        device_template = DeviceTemplate(sensors=[sensor1])

        device = Device("device1", "key1", device_template)

        wolk.add_device(device)

        self.assertEqual(1, wolk.outbound_message_queue.queue_size())

    def test_bad_actuation_handler_not_callable(self):
        """Test passing something that isn't callable raises ValueError."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda device_key: DeviceStatus.CONNECTED,
                actuation_handler=False,
            )

    def test_bad_actuation_handler_callable(self):
        """Test passing something that isn't callable raises ValueError."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda device_key: DeviceStatus.CONNECTED,
                actuation_handler=lambda a: a,
            )

    def test_bad_actuation_provider_not_callable(self):
        """Test passing something that isn't callable raises ValueError."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda device_key: DeviceStatus.CONNECTED,
                actuator_status_provider=False,
            )

    def test_bad_actuation_provider_callable(self):
        """Test passing something that isn't callable raises ValueError."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda device_key: DeviceStatus.CONNECTED,
                actuator_status_provider=lambda a: a,
            )

    def test_missing_actuator_status_provider(self):
        """Test passing an actuator handler but no provider raises an exception."""
        with self.assertRaises(RuntimeError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda a: a,
                connectivity_service=MockConnectivityService(),
                actuation_handler=mock_actuator_handler,
            )

    def test_bad_configuration_handler_not_callable(self):
        """Test passing something that isn't callable raises ValueError."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda device_key: DeviceStatus.CONNECTED,
                configuration_handler=False,
            )

    def test_bad_configuration_handler_callable(self):
        """Test passing something that isn't callable raises ValueError."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda device_key: DeviceStatus.CONNECTED,
                configuration_handler=lambda a: a,
            )

    def test_bad_configuration_provider_not_callable(self):
        """Test passing something that isn't callable raises ValueError."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda device_key: DeviceStatus.CONNECTED,
                configuration_provider=False,
            )

    def test_bad_configuration_provider_callable(self):
        """Test passing something that isn't callable raises ValueError."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda device_key: DeviceStatus.CONNECTED,
                configuration_provider=lambda a, b: a,
            )

    def test_missing_configuration_provider(self):
        """Test passing an config handler but no provider raises an exception."""
        with self.assertRaises(RuntimeError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda a: a,
                connectivity_service=MockConnectivityService(),
                configuration_handler=mock_configuration_handler,
            )

    def test_bad_firmware_handler(self):
        """Test passing a bad firmware handler raises an exception."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda a: a,
                firmware_handler=False,
            )

    def test_bad_data_protocol(self):
        """Test passing a bad data protocol raises an exception."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda a: a,
                data_protocol=False,
            )

    def test_good_data_protocol(self):
        """Test passing a good data protocol doesn't raise an exception."""
        data_protocol = JsonDataProtocol()

        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            data_protocol=data_protocol,
        )

        self.assertEqual(data_protocol, wolk.data_protocol)

    def test_bad_firmware_update_protocol(self):
        """Test passing a bad firmware update protocol raises an exception."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda a: a,
                firmware_update_protocol=False,
            )

    def test_good_firmware_update_protocol(self):
        """Test passing a good firmware update protocol doesn't raise an exception."""
        firmware_update_protocol = JsonFirmwareUpdateProtocol()

        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            firmware_update_protocol=firmware_update_protocol,
        )

        self.assertEqual(
            firmware_update_protocol, wolk.firmware_update_protocol
        )

    def test_bad_status_protocol(self):
        """Test passing a bad status protocol raises an exception."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda a: a,
                status_protocol=False,
            )

    def test_good_status_protocol(self):
        """Test passing a good status protocol doesn't raise an exception."""
        status_protocol = JsonStatusProtocol()

        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            status_protocol=status_protocol,
        )

        self.assertEqual(status_protocol, wolk.status_protocol)

    def test_bad_registration_protocol(self):
        """Test passing a bad registration protocol raises an exception."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda a: a,
                registration_protocol=False,
            )

    def test_good_registration_protocol(self):
        """Test passing a good registration protocol doesn't raise an exception."""
        registration_protocol = JsonRegistrationProtocol()

        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            registration_protocol=registration_protocol,
        )

        self.assertEqual(registration_protocol, wolk.registration_protocol)

    def test_bad_outbound_message_queue(self):
        """Test passing a bad outbound message queue raises an exception."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda a: a,
                outbound_message_queue=False,
            )

    def test_good_outbound_message_queue(self):
        """Test passing a good outbound message queue doesn't raise an exception."""
        outbound_message_queue = OutboundMessageDeque()

        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            outbound_message_queue=outbound_message_queue,
        )

        self.assertEqual(outbound_message_queue, wolk.outbound_message_queue)

    def test_bad_connectivity_service(self):
        """Test passing a bad connectivity service raises an exception."""
        with self.assertRaises(ValueError):
            wolk = Wolk(  # noqa
                "host",
                1883,
                "module_name",
                lambda a: a,
                connectivity_service=False,
            )

    def test_good_connectivity_service(self):
        """Test passing a good connectivity service doesn't raise an exception."""
        connectivity_service = MockConnectivityService()

        wolk = Wolk(
            "host",
            1883,
            "module_name",
            lambda a: a,
            connectivity_service=connectivity_service,
        )

        self.assertEqual(connectivity_service, wolk.connectivity_service)


if __name__ == "__main__":
    unittest.main()
