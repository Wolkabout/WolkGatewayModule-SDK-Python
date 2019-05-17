"""Handling of device registration using JSON_PROTOCOL."""
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

from wolk_gateway_module.logger_factory import logger_factory
from wolk_gateway_module.model.device_registration_request import (
    DeviceRegistrationRequest,
)
from wolk_gateway_module.model.device_registration_response import (
    DeviceRegistrationResponse,
)
from wolk_gateway_module.model.device_registration_response_result import (
    DeviceRegistrationResponseResult,
)
from wolk_gateway_module.model.message import Message
from wolk_gateway_module.model.reading_type_measurement_unit import (
    ReadingTypeMeasurementUnit,
)
from wolk_gateway_module.model.reading_type_name import ReadingTypeName
from wolk_gateway_module.protocol.registration_protocol import (
    RegistrationProtocol,
)


class JsonRegistrationProtocol(RegistrationProtocol):
    """Send device registration requests and handle their responses.

    :ivar CHANNEL_WILDCARD: Wildcard for subscribing to inbound messages
    :vartype CHANNEL_WILDCARD: str
    :ivar DEVICE_PATH_PREFIX: Indicator that the message is for a device
    :vartype DEVICE_PATH_PREFIX: str
    :ivar DEVICE_REGISTRATION_REQUEST_TOPIC_ROOT: Device registration request topic
    :vartype DEVICE_REGISTRATION_REQUEST_TOPIC_ROOT: str
    :ivar DEVICE_REGISTRATION_RESPONSE_TOPIC_ROOT: Device registration response topic
    :vartype DEVICE_REGISTRATION_RESPONSE_TOPIC_ROOT: str
    """

    DEVICE_PATH_PREFIX = "d/"
    CHANNEL_WILDCARD = "#"
    DEVICE_REGISTRATION_REQUEST_TOPIC_ROOT = "d2p/register_subdevice_request/"
    DEVICE_REGISTRATION_RESPONSE_TOPIC_ROOT = (
        "p2d/register_subdevice_response/"
    )

    def __init__(self) -> None:
        """Create object."""
        self.log = logger_factory.get_logger(str(self.__class__.__name__))

    def __repr__(self) -> str:
        """Make string representation of JsonRegistrationProtocol.

        :returns: representation
        :rtype: str
        """
        return "JsonRegistrationProtocol()"

    def get_inbound_topics_for_device(self, device_key: str) -> list:
        """Return list of inbound topics for given device key.

        :param device_key: Device key for which to create topics
        :type device_key: str

        :returns: inbound_topics
        :rtype: list
        """
        inbound_topics = [
            self.DEVICE_REGISTRATION_RESPONSE_TOPIC_ROOT
            + self.DEVICE_PATH_PREFIX
            + device_key
        ]
        self.log.debug(f"Inbound topics for {device_key} : {inbound_topics}")

        return inbound_topics

    def extract_key_from_message(self, message: Message) -> str:
        """Return device key from message.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: device_key
        :rtype: str
        """
        device_key = message.topic.split("/")[-1]
        self.log.debug(f"Made {device_key} from {message}")

        return device_key

    def is_registration_response_message(self, message: Message) -> bool:
        """Check if message is device registration response.

        :param message: Message received
        :type message: wolk_gateway_module.model.message.Message

        :returns: is_device_registration_response
        :rtype: bool
        """
        is_device_registration_response = message.topic.startswith(
            self.DEVICE_REGISTRATION_RESPONSE_TOPIC_ROOT
        )
        self.log.debug(
            f"Is {message} device registration response "
            f"message: {is_device_registration_response}"
        )

        return is_device_registration_response

    def make_registration_message(
        self, request: DeviceRegistrationRequest
    ) -> Message:
        """Make message from device registration request.

        :param request: Device registration request
        :type request: wolk_gateway_module.model.device_registration_request.DeviceRegistrationRequest

        :returns: message
        :rtype: wolk_gateway_module.model.message.Message
        """
        request_dict = {
            "name": request.name,
            "deviceKey": request.key,
            "defaultBinding": request.default_binding,
            "typeParameters": request.template.type_parameters,
            "connectivityParameters": request.template.connectivity_parameters,
        }

        request_dict["sensors"] = []
        for sensor in request.template.sensors:
            sensor_dict = {
                "name": sensor.name,
                "reference": sensor.reference,
                "description": sensor.description,
                "minimum": sensor.minimum,
                "maximum": sensor.maximum,
            }
            sensor_dict["unit"] = (
                {
                    "readingTypeName": sensor.unit.name.value,
                    "symbol": sensor.unit.unit.value,
                }
                if (
                    isinstance(sensor.unit.name, ReadingTypeName)
                    and isinstance(
                        sensor.unit.unit, ReadingTypeMeasurementUnit
                    )
                )
                else {
                    "readingTypeName": sensor.unit.name,
                    "symbol": sensor.unit.unit,
                }
            )
            request_dict["sensors"].append(sensor_dict)

        request_dict["actuators"] = [
            actuator.__dict__ for actuator in request.template.actuators
        ]

        request_dict["alarms"] = [
            alarm.__dict__ for alarm in request.template.alarms
        ]

        request_dict["configurations"] = [
            {
                "name": configuration.name,
                "reference": configuration.reference,
                "description": configuration.description,
                "defaultValue": configuration.default_value,
                "size": configuration.size,
                "labels": configuration.labels,
                "minimum": configuration.minimum,
                "maximum": configuration.maximum,
                "dataType": configuration.data_type.name,
            }
            for configuration in request.template.configurations
        ]

        if (
            "supportsFirmwareUpdate"
            not in request.template.firmware_update_parameters
        ):
            request.template.firmware_update_parameters[
                "supportsFirmwareUpdate"
            ] = request.template.supports_firmware_update

        request_dict[
            "firmwareUpdateParameters"
        ] = request.template.firmware_update_parameters

        message = Message(
            self.DEVICE_REGISTRATION_REQUEST_TOPIC_ROOT,
            json.dumps(request_dict, ensure_ascii=False)
            .encode("utf-8")
            .decode("utf-8"),
        )
        self.log.debug(f"Made {message} from {request}")

        return message

    def make_registration_response(
        self, message: Message
    ) -> DeviceRegistrationResponse:
        """Make device registration response from message.

        :param message: Message received
        :rtype message: wolk_gateway_module.model.message.Message

        :returns: device_registration_response
        :rtype: wolk_gateway_module.model.device_registration_response.DeviceRegistrationResponse
        """
        response = json.loads(message.payload)

        result = DeviceRegistrationResponseResult.ERROR_UNKNOWN

        for enumeration in DeviceRegistrationResponseResult:
            if response["result"] == enumeration.value:
                result = enumeration
                break

        description = (
            response["description"] if "description" in response else ""
        )

        device_registration_response = DeviceRegistrationResponse(
            response["payload"]["deviceKey"], result, description
        )
        self.log.debug(f"Made {device_registration_response} from {message}")

        return device_registration_response
