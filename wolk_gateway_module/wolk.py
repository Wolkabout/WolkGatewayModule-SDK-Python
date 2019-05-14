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


from json_data_protocol import JsonDataProtocol
from json_firmware_update_protocol import JsonFirmwareUpdateProtocol
from json_registration_protocol import JsonRegistrationProtocol
from json_status_protocol import JsonStatusProtocol
from mqtt_connectivity_service import MQTTConnectivityService
from outbound_message_deque import OutboundMessageDeque


class Wolk:
    def __init__(
        self,
        host,
        port,
        device_status_provider,
        actuation_handler=None,
        acutator_status_provider=None,
        configuration_handler=None,
        configuration_provider=None,
        firmware_installer=None,
        firmware_version_provider=None,
        connectivity_service=None,
        data_protocol=None,
        firmware_update_protocol=None,
        registration_protocol=None,
        status_protocol=None,
        outbound_message_queue=None,
    ):
        pass
