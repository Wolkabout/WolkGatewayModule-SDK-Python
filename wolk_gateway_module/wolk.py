"""This module contains the Wolk class that ties together the whole package."""
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
from inspect import signature
from typing import Callable, Dict, Optional, Tuple, Union


from wolk_gateway_module.json_data_protocol import JsonDataProtocol
from wolk_gateway_module.json_firmware_update_protocol import (
    JsonFirmwareUpdateProtocol,
)
from wolk_gateway_module.json_registration_protocol import (
    JsonRegistrationProtocol,
)
from wolk_gateway_module.json_status_protocol import JsonStatusProtocol
from wolk_gateway_module.mqtt_connectivity_service import (
    MQTTConnectivityService,
)
from wolk_gateway_module.outbound_message_deque import OutboundMessageDeque
from wolk_gateway_module.model.device_status import DeviceStatus
from wolk_gateway_module.model.actuator_state import ActuatorState
from wolk_gateway_module.model.actuator_status import ActuatorStatus
from wolk_gateway_module.model.alarm import Alarm
from wolk_gateway_module.model.sensor_reading import SensorReading

from wolk_gateway_module.protocol.data_protocol import DataProtocol
from wolk_gateway_module.protocol.firmware_update_protocol import (
    FirmwareUpdateProtocol,
)
from wolk_gateway_module.protocol.registration_protocol import (
    RegistrationProtocol,
)
from wolk_gateway_module.protocol.status_protocol import StatusProtocol
from wolk_gateway_module.persistance.outbound_message_queue import (
    OutboundMessageQueue,
)
from wolk_gateway_module.connectivity.connectivity_service import (
    ConnectivityService,
)
from wolk_gateway_module.model.message import Message


class Wolk:
    """This class is the core of this package, tying together all features."""

    def __init__(
        self,
        host: str,
        port: int,
        module_name: str,
        device_status_provider: Callable[[str], DeviceStatus],
        actuation_handler: Optional[Callable[[str, str, str], None]] = None,
        acutator_status_provider: Optional[
            Callable[
                [str, str], Tuple[ActuatorState, Union[bool, int, float, str]]
            ]
        ] = None,
        configuration_handler: Optional[
            Callable[[str, Dict[str, str]], None]
        ] = None,
        configuration_provider: Optional[
            Callable[
                [str],
                Dict[
                    str,
                    Union[
                        int,
                        float,
                        bool,
                        str,
                        Tuple[int, int],
                        Tuple[int, int, int],
                        Tuple[float, float],
                        Tuple[float, float, float],
                        Tuple[str, str],
                        Tuple[str, str, str],
                    ],
                ],
            ]
        ] = None,
        firmware_installer: Optional[Callable[[str, str], None]] = None,
        firmware_version_provider: Optional[Callable[[str], str]] = None,
        connectivity_service: Optional[ConnectivityService] = None,
        data_protocol: Optional[DataProtocol] = None,
        firmware_update_protocol: Optional[FirmwareUpdateProtocol] = None,
        registration_protocol: Optional[RegistrationProtocol] = None,
        status_protocol: Optional[StatusProtocol] = None,
        outbound_message_queue: Optional[OutboundMessageQueue] = None,
    ):
        """Construct an instance ready to communicate with WolkGateway.

        :param host: Host address of WolkGateway
        :type host: str
        :param port: TCP/IP port of WolkGateway
        :type port: int
        :param module_name: Module identifier used when connecting to gateway
        :type module_name: str
        :param device_status_provider: Provider of device's current status
        :type device_status_provider: Callable[[str], DeviceStatus]
        :param actuation_handler: Setter of new device actuator values
        :type actuation_handler: Optional[Callable[[str, str, str], None]]
        :param acutator_status_provider: Provider of device's current actuator status
        :type acutator_status_provider: Optional[Callable[[str, str], Tuple[ActuatorState, Union[bool, int, float, str]]]]
        :param configuration_handler: Setter of new device configuration values
        :type configuration_handler: Optional[Callable[[str, Dict[str, str]], None]]
        :param configuration_provider: Provider of device's configuration options
        :type configuration_provider: Optional[Callable[[str], Dict[str, Union[int, float, bool, str, Tuple[int, int], Tuple[int, int, int], Tuple[float, float], Tuple[float, float, float], Tuple[str, str], Tuple[str, str, str], ], ], ]]
        :param firmware_installer: Handling of firmware installation
        :type firmware_installer: Optional[Callable[[str, str], None]]
        :param firmware_version_provider: Provider of device's current firmware version
        :type firmware_version_provider: Optional[Callable[[str], str]]
        :param connectivity_service: Custom connectivity service implementation
        :type connectivity_service: Optional[ConnectivityService]
        :param data_protocol: Custom data protocol implementation
        :type data_protocol: Optional[DataProtocol]
        :param firmware_update_protocol: Custom firmware update protocol implementation
        :type firmware_update_protocol: Optional[FirmwareUpdateProtocol]
        :param registration_protocol: Custom registration protocol implementation
        :type registration_protocol: Optional[RegistrationProtocol]
        :param status_protocol: Custom device status protocol implementation
        :type status_protocol: Optional[StatusProtocol]
        :param outbound_message_queue: Custom persistent storage implementation
        :type outbound_message_queue: Optional[OutboundMessageQueue]
        """
        self.host = host
        self.port = port
        self.module_name = module_name

        if not callable(device_status_provider):
            raise RuntimeError(f"{device_status_provider} is not a callable!")
        if len(signature(device_status_provider).parameters) != 1:
            raise RuntimeError(f"{device_status_provider} invalid signature!")
        self.device_status_provider = device_status_provider

        if actuation_handler is not None:
            if not callable(actuation_handler):
                raise RuntimeError(f"{actuation_handler} is not a callable!")
            if len(signature(actuation_handler).parameters) != 3:
                raise RuntimeError(f"{actuation_handler} invalid signature!")
            self.actuation_handler = actuation_handler
        else:
            self.actuation_handler = None

        if acutator_status_provider is not None:
            if not callable(acutator_status_provider):
                raise RuntimeError(
                    f"{acutator_status_provider} is not a callable!"
                )
            if len(signature(acutator_status_provider).parameters) != 2:
                raise RuntimeError(
                    f"{acutator_status_provider} invalid signature!"
                )
            self.acutator_status_provider = acutator_status_provider
        else:
            self.acutator_status_provider = None

        if not (self.actuation_handler and self.acutator_status_provider):
            raise RuntimeError(
                "Provide actuation_handler and acutator_status_provider"
                " to enable actuators on your devices!"
            )

        if configuration_handler is not None:
            if not callable(configuration_handler):
                raise RuntimeError(
                    f"{configuration_handler} is not a callable!"
                )
            if len(signature(configuration_handler).parameters) != 2:
                raise RuntimeError(
                    f"{configuration_handler} invalid signature!"
                )
            self.configuration_handler = configuration_handler
        else:
            self.configuration_handler = None

        if configuration_provider is not None:
            if not callable(configuration_provider):
                raise RuntimeError(
                    f"{configuration_provider} is not a callable!"
                )
            if len(signature(configuration_provider).parameters) != 1:
                raise RuntimeError(
                    f"{configuration_provider} invalid signature!"
                )
            self.configuration_provider = configuration_provider
        else:
            self.configuration_provider = None

        if not (self.configuration_handler and self.configuration_provider):
            raise RuntimeError(
                "Provide configuration_handler and configuration_provider"
                " to enable configuration options on your devices!"
            )

        if firmware_installer is not None:
            if not callable(firmware_installer):
                raise RuntimeError(f"{firmware_installer} is not a callable!")
            if len(signature(firmware_installer).parameters) != 2:
                raise RuntimeError(f"{firmware_installer} invalid signature!")
            self.firmware_installer = firmware_installer
        else:
            self.firmware_installer = None

        if firmware_version_provider is not None:
            if not callable(firmware_version_provider):
                raise RuntimeError(
                    f"{firmware_version_provider} is not a callable!"
                )
            if len(signature(firmware_version_provider).parameters) != 1:
                raise RuntimeError(
                    f"{firmware_version_provider} invalid signature!"
                )
            self.firmware_version_provider = firmware_version_provider
        else:
            self.firmware_version_provider = None

        if not (self.firmware_installer and self.firmware_version_provider):
            raise RuntimeError(
                "Provide firmware_installer and firmware_version_provider"
                " to enable firmware update on your devices!"
            )

        if data_protocol is not None:
            if not isinstance(data_protocol, DataProtocol):
                raise RuntimeError(
                    f"{data_protocol} is not a valid instance of DataProtocol!"
                )
            self.data_protocol = data_protocol
        else:
            self.data_protocol = JsonDataProtocol()

        if firmware_update_protocol is not None:
            if not isinstance(
                firmware_update_protocol, FirmwareUpdateProtocol
            ):
                raise RuntimeError(
                    f"{firmware_update_protocol} is not a valid instance of"
                    " FirmwareUpdateProtocol!"
                )
            self.firmware_update_protocol = firmware_update_protocol
        else:
            self.firmware_update_protocol = JsonFirmwareUpdateProtocol()

        if status_protocol is not None:
            if not isinstance(status_protocol, StatusProtocol):
                raise RuntimeError(
                    f"{status_protocol} is not a valid instance of "
                    "StatusProtocol!"
                )
            self.status_protocol = status_protocol
        else:
            self.status_protocol = JsonStatusProtocol()

        if registration_protocol is not None:
            if not isinstance(registration_protocol, RegistrationProtocol):
                raise RuntimeError(
                    f"{registration_protocol} is not a valid instance of "
                    "RegistrationProtocol!"
                )
            self.registration_protocol = registration_protocol
        else:
            self.registration_protocol = JsonRegistrationProtocol()

        if outbound_message_queue is not None:
            if not isinstance(outbound_message_queue, OutboundMessageQueue):
                raise RuntimeError(
                    f"{outbound_message_queue} is not a valid instance of "
                    "OutboundMessageQueue!"
                )
            self.outbound_message_queue = outbound_message_queue
        else:
            self.outbound_message_queue = OutboundMessageDeque()

        self.device_keys = []

        last_will_message = self.status_protocol.make_last_will_message(
            self.device_keys
        )

        if connectivity_service is not None:
            if not isinstance(connectivity_service, ConnectivityService):
                raise RuntimeError(
                    f"{connectivity_service} is not a valid instance of "
                    "ConnectivityService!"
                )
            self.connectivity_service = connectivity_service
        else:
            self.connectivity_service = MQTTConnectivityService(
                host, port, module_name, 0, last_will_message, []
            )

        self.connectivity_service.set_inbound_message_listener(
            self._on_inbound_message
        )

    def __repr__(self) -> str:
        """Make string representation or Wolk.

        :returns: representation
        :rtype: str
        """
        return (
            f"Wolk(host='{self.host}', "
            f"port='{self.port}', "
            f"module_name='{self.module_name}', "
            f"device_status_provider='{self.device_status_provider}', "
            f"actuation_handler='{self.actuation_handler}', "
            f"acutator_status_provider='{self.acutator_status_provider}', "
            f"configuration_handler='{self.configuration_handler}', "
            f"configuration_provider='{self.configuration_provider}', "
            f"firmware_installer='{self.firmware_installer}', "
            f"firmware_version_provider='{self.firmware_version_provider}', "
            f"data_protocol='{self.data_protocol}', "
            f"firmware_update_protocol='{self.firmware_update_protocol}', "
            f"status_protocol='{self.status_protocol}', "
            f"registration_protocol='{self.registration_protocol}', "
            f"outbound_message_queue='{self.outbound_message_queue}', "
            f"connectivity_service='{self.connectivity_service}', "
            f"device_keys='{self.device_keys}')"
        )

    def _on_inbound_message(self, message: Message) -> None:
        """Handle messages received from WolkGateway.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message
        """
        pass

    def add_sensor_reading(
        self,
        device_key: str,
        reference: str,
        value: Union[
            bool,
            int,
            float,
            str,
            Tuple[int, int],
            Tuple[int, int, int],
            Tuple[float, float],
            Tuple[float, float, float],
            Tuple[str, str],
            Tuple[str, str, str],
        ],
        timestamp: Optional[int],
    ) -> None:
        """Serialize sensor reading and put into storage.

        Storing readings without Unix timestamp will result
        in all sent messages being treated as live readings and
        will be assigned a timestamp upon reception, so for a valid
        history add timestamps to readings via `int(round(time.time() * 1000))`

        :param device_key: Device on which the sensor reading occurred
        :type device_key: str
        :param reference: Sensor reference (unique per device)
        :type reference: str
        :param value: Value(s) that the reading yielded
        :type value: Union[bool,int,float,str,Tuple[int, int],Tuple[int, int, int],Tuple[float, float],Tuple[float, float, float],Tuple[str, str],Tuple[str, str, str],]
        :param timestamp: Unix time
        :type timestamp: Optional[int]

        :raises RuntimeError: Unable to place in storage
        """
        reading = SensorReading(reference, value, timestamp)
        message = self.data_protocol.make_sensor_reading_message(
            device_key, reading
        )
        if not self.outbound_message_queue.put(message):
            raise RuntimeError(f"Unable to store message: {message}")

    def add_alarm(
        self,
        device_key: str,
        reference: str,
        active: bool,
        timestamp: Optional[int],
    ) -> None:
        """Serialize alarm event and put into storage.

        Storing alarms without Unix timestamp will result
        in all sent messages being treated as live and
        will be assigned a timestamp upon reception, so for a valid
        history add timestamps to alarms via `int(round(time.time() * 1000))`

        :param device_key: Device on which the sensor reading occurred
        :type device_key: str
        :param reference: Alarm reference (unique per device)
        :type reference: str
        :param value: Current state of alarm
        :type active: bool
        :param timestamp: Unix time
        :type timestamp: Optional[int]

        :raises RuntimeError: Unable to place in storage
        """
        alarm = Alarm(reference, active, timestamp)
        message = self.data_protocol.make_alarm_message(device_key, alarm)
        if not self.outbound_message_queue.put(message):
            raise RuntimeError(f"Unable to store message: {message}")

    def publish_acutator_status(self, device_key: str, reference: str) -> None:
        """Publish device actuator status to WolkGateway.

        If message is unable to be sent, it will be placed in storage.

        Getting the actuator status is achieved by calling the user's
        implementation of acutator_status_provider.

        If no acutator_status_provider is present, will raise exception.

        :param device_key: Device on which the sensor reading occurred
        :type device_key: str
        :param reference: Alarm reference (unique per device)
        :type reference: str

        :raises RuntimeError: Unable to place in storage or no status provider
        """
        if not (self.acutator_status_provider and self.actuation_handler):
            raise RuntimeError(
                "Unable to publish actuator status because "
                "acutator_status_provider and actuation_handler "
                "were not provided!"
            )
        state, value = self.acutator_status_provider(device_key, reference)

        if None in (state, value):
            raise RuntimeError(
                f"{self.acutator_status_provider} did not return anything"
                f" for device '{device_key}' with reference '{reference}'"
            )

        if not isinstance(state, ActuatorState):
            raise RuntimeError(f"{state} is not a member of ActuatorState!")

        status = ActuatorStatus(reference, state, value)
        message = self.data_protocol.make_actuator_status_message(
            device_key, status
        )
        if self.connectivity_service.connected:
            if not self.connectivity_service.publish(message):
                if not self.outbound_message_queue.put(message):
                    raise RuntimeError(
                        f"Unable to publish and failed "
                        f"to store message: {message}"
                    )
        else:
            if not self.outbound_message_queue.put(message):
                raise RuntimeError(f"Unable to store message: {message}")

    def add_device_status(self, device_key: str, status: DeviceStatus) -> None:
        """Serialize device status and place into storage.

        :param device_key: Device to which the status belongs to
        :type device_key: str
        :param status: Current device status
        :type status: wolk_gateway_module.model.device_status.DeviceStatus
        :raises ValueError: status is not of DeviceStatus
        """
        if not isinstance(status, DeviceStatus):
            raise ValueError(f"{status} is not an instance of DeviceStatus")

        message = self.status_protocol.make_device_status_update_message(
            device_key, status
        )

        if not self.outbound_message_queue.put(message):
            raise RuntimeError(f"Unable to store message: {message}")

    def publish_configuration(self, device_key: str) -> None:
        """Publish device configuration options to WolkGateway.

        If message is unable to be sent, it will be placed in storage.

        Getting the current configuration is achieved by calling the user's
        implementation of configuration_provider.

        If no configuration_provider is present, will raise exception.

        :param device_key: Device to which the configuration belongs to
        :type device_key: str

        :raises RuntimeError: No configuration provider present
        """
        if not (self.configuration_handler and self.configuration_provider):
            raise RuntimeError(
                "Unable to publish configuration because "
                "configuration_provider and configuration_handler "
                "were not provided!"
            )

        configuration = self.configuration_provider(device_key)

        if configuration is None:
            raise RuntimeError(
                f"{self.configuration_provider} did not return"
                f"anything for device '{device_key}'"
            )

        message = self.data_protocol.make_configuration_message(
            device_key, configuration
        )
        if self.connectivity_service.connected:
            if not self.connectivity_service.publish(message):
                if not self.outbound_message_queue.put(message):
                    raise RuntimeError(
                        f"Unable to publish and failed "
                        f"to store message: {message}"
                    )
        else:
            if not self.outbound_message_queue.put(message):
                raise RuntimeError(f"Unable to store message: {message}")
