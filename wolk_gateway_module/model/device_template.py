"""Device template used for registering device on WolkAbout IoT Platform."""
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

from dataclasses import dataclass, field
from typing import Dict, List

from actuator_template import ActuatorTemplate
from alarm_template import AlarmTemplate
from configuration_template import ConfigurationTemplate
from sensor_template import SensorTemplate


@dataclass
class DeviceTemplate:
    """Contains information required for registering device on Platform.

    :ivar actuators: List of actuators on device
    :vartype actuators: list(wolk_gateway_module.model.actuator_template.ActuatorTemplate)
    :ivar alarms: List of alarms on device
    :vartype alarms: list(wolk_gateway_module.model.alarm_template.AlarmTemplate)
    :ivar configurations: List of configurations on device
    :vartype configurations: list(wolk_gateway_module.model.configuration_template.ConfigurationTemplate)
    :ivar connectivity_parameters: Device's connectivity parameters
    :vartype connectivity_parameters: dict
    :ivar firmware_update_type: Device's firmware update type
    :vartype firmware_update_type: str
    :ivar sensors: List of sensors on device
    :vartype sensors: list(wolk_gateway_module.model.sensor_template.SensorTemplate)
    :ivar type_parameters: Device's type parameters
    :vartype type_parameters: dict
    :ivar firmware_update_parameters: Device's firmware update parameters
    :vartype firmware_update_parameters: dict
    """

    actuators: List[ActuatorTemplate] = field(default_factory=list)
    alarms: List[AlarmTemplate] = field(default_factory=list)
    configurations: List[ConfigurationTemplate] = field(default_factory=list)
    sensors: List[SensorTemplate] = field(default_factory=list)
    firmware_update_type: str = field(default="")
    type_parameters: Dict = field(default_factory=dict)
    connectivity_parameters: Dict = field(default_factory=dict)
    firmware_update_parameters: Dict = field(default_factory=dict)
