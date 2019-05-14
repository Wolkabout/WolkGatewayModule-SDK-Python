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
