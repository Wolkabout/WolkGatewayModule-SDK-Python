"""Example usage of gateway module."""
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
from time import sleep, time
from random import randint

import wolk_gateway_module as wolk

# # uncommenct to enable debug logging to file
# wolk.logging_config("debug", "wolk_gateway_module.log")

with open("configuration.json", encoding="utf-8") as file:
    configuration = json.load(file)


temperature_sensor = wolk.SensorTemplate(
    name="Temperature",
    reference="T",
    reading_type_name=wolk.ReadingTypeName.TEMPERATURE,
    unit=wolk.ReadingTypeMeasurementUnit.CELSIUS,
    minimum=-20,
    maximum=85,
    description="Temperature sensor with range -20 to 85 Celsius",
)

device_template = wolk.DeviceTemplate(sensors=[temperature_sensor])

device = wolk.Device("Device1", "module_device_1", device_template)


def get_device_status(device_key: str) -> wolk.DeviceStatus:
    """Return current device status."""
    if device_key == "module_device_1":
        return wolk.DeviceStatus.CONNECTED


wolk_module = wolk.Wolk(
    configuration["host"],
    configuration["port"],
    configuration["module_name"],
    get_device_status,
)


wolk_module.add_device(device)

wolk_module.connect()

wolk_module.publish()

while True:
    try:
        sleep(3)
        wolk_module.add_sensor_reading(
            "module_device_1", "T", randint(-20, 85), int(round(time() * 1000))
        )
        wolk_module.publish()
    except KeyboardInterrupt:
        break
