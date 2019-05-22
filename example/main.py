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
from typing import Dict, Tuple, Union
from random import randint

import wolk_gateway_module as wolk

# # uncomment to enable debug logging to file
# wolk.logging_config("debug", "wolk_gateway_module.log")

with open("configuration.json", encoding="utf-8") as file:
    configuration = json.load(file)


switch = False
slider = 0
text = "default_text"

device_1_configuration_1 = "default_value"
device_1_configuration_2 = (5, 12, 3)
device_2_configuration_1 = 8.13

temperature_sensor = wolk.SensorTemplate(
    name="Temperature",
    reference="T",
    reading_type_name=wolk.ReadingTypeName.TEMPERATURE,
    unit=wolk.ReadingTypeMeasurementUnit.CELSIUS,
    minimum=-20,
    maximum=85,
    description="Temperature sensor with range -20 to 85 Celsius",
)

pressure_sensor = wolk.SensorTemplate(
    name="Pressure",
    reference="P",
    reading_type_name=wolk.ReadingTypeName.PRESSURE,
    unit=wolk.ReadingTypeMeasurementUnit.MILLIBAR,
    minimum=300,
    maximum=1100,
    description="Pressure sensor with range 300 to 1100 milibars",
)

humidity_sensor = wolk.SensorTemplate(
    name="Humidity",
    reference="H",
    reading_type_name=wolk.ReadingTypeName.HUMIDITY,
    unit=wolk.ReadingTypeMeasurementUnit.HUMIDITY_PERCENT,
    minimum=0,
    maximum=100,
)

acceleration_sensor = wolk.SensorTemplate(
    name="Accelerometer",
    reference="ACCL",
    reading_type_name=wolk.ReadingTypeName.ACCELEROMETER,
    unit=wolk.ReadingTypeMeasurementUnit.METRES_PER_SQUARE_SECOND,
    minimum=0,
    maximum=1000,
)

humidity_alarm = wolk.AlarmTemplate(
    name="High Humidity",
    reference="HH",
    description="Notify about high humidity detected",
)

switch_actuator = wolk.ActuatorTemplate(
    name="Switch",
    reference="SW",
    data_type=wolk.DataType.BOOLEAN,
    description="Light switch",
)

slider_actuator = wolk.ActuatorTemplate(
    name="Slider",
    reference="SL",
    data_type=wolk.DataType.NUMERIC,
    minimum=0,
    maximum=100,
    description="Light dimmer",
)

text_actuator = wolk.ActuatorTemplate(
    name="Message",
    reference="MSG",
    data_type=wolk.DataType.STRING,
    description="Text display",
)

device_1_configuration_1_template = wolk.ConfigurationTemplate(
    name="Configuration_1",
    reference="configuration_1",
    data_type=wolk.DataType.STRING,
    default_value="default_text",
    description="eg. set logging level",
)

device_1_configuration_2_template = wolk.ConfigurationTemplate(
    name="Configuration_2",
    reference="configuration_2",
    data_type=wolk.DataType.NUMERIC,
    size=3,
    labels=["seconds", "minutes", "hours"],
    description="eg. logging intervals",
)

device_2_configuration_1_template = wolk.ConfigurationTemplate(
    name="Configuration_1",
    reference="configuration_1",
    data_type=wolk.DataType.NUMERIC,
    default_value="8.13",
    description="eg. threshold for some event",
)


device_template_1 = wolk.DeviceTemplate(
    sensors=[temperature_sensor, humidity_sensor],
    actuators=[switch_actuator, text_actuator],
    configurations=[
        device_1_configuration_1_template,
        device_1_configuration_2_template,
    ],
    supports_firmware_update=True,
)
device1 = wolk.Device("Device1", "module_device_1", device_template_1)


device_template_2 = wolk.DeviceTemplate(
    sensors=[pressure_sensor, acceleration_sensor],
    actuators=[slider_actuator],
    alarms=[humidity_alarm],
    configurations=[device_2_configuration_1_template],
    supports_firmware_update=False,
)
device2 = wolk.Device("Device2", "module_device_2", device_template_2)


device_1_firmware_version = 1


class FirmwareHandlerImplementation(wolk.FirmwareHandler):
    """Handle firmware installation and abort commands, and report version.

    Once an object of this class is passed to a Wolk object,
    it will set callback methods `on_install_success` and
    `on_install_fail` used for reporting the result of
    the firmware update process. Use these callbacks in `install_firmware`
    and `abort_installation` methods."""

    def install_firmware(
        self, device_key: str, firmware_file_path: str
    ) -> None:
        """
        Handle the installation of the firmware file.

        Call `self.on_install_success(device_key)` to report success.
        Reporting success will also get new firmware version.

        If installation fails, call `self.on_install_fail(device_key, status)`
        where:
        `status = FirmwareUpdateStatus(
            FirmwareUpdateState.ERROR,
            FirmwareUpdateErrorCode.INSTALLATION_FAILED
        )`
        or use other values from `FirmwareUpdateErrorCode` if they fit better.

        :param device_key: Device for which the firmware command is intended
        :type device_key: str
        :param firmware_file_path: Path where the firmware file is located
        :type firmware_file_path: str
        """
        if device_key == "module_device_1":
            print(
                f"Installing firmware: '{firmware_file_path}' "
                f"on device '{device_key}'"
            )

            # Handle the actual installation here

            if True:
                global device_1_firmware_version
                device_1_firmware_version += 1
                self.on_install_success(device_key)
            else:
                status = wolk.FirmwareUpdateStatus(
                    wolk.FirmwareUpdateState.ERROR,
                    wolk.FirmwareUpdateErrorCode.INSTALLATION_FAILED,
                )
                self.on_install_fail(device_key, status)

    def abort_installation(self, device_key: str) -> None:
        """
        Attempt to abort the firmware installation process for device.

        Call `self.on_install_fail(device_key, status)` to report if
        the installation process was able to be aborted with
        `status = FirmwareUpdateStatus(FirmwareUpdateState.ABORTED)`
        If unable to stop the installation process, no action is required.

        :param device_key: Device for which to abort installation
        :type device_key: str
        """
        if device_key == "module_device_1":
            # manage to stop firmware installation
            status = wolk.FirmwareUpdateStatus(
                wolk.FirmwareUpdateState.ABORTED
            )
            self.on_install_fail(device_key, status)

    def get_firmware_version(self, device_key: str) -> str:
        """
        Return device's current firmware version.

        :param device_key: Device identifier
        :type device_key: str
        :returns: version
        :rtype: str
        """
        if device_key == "module_device_1":
            return str(device_1_firmware_version)


def get_device_status(device_key: str) -> wolk.DeviceStatus:
    """Return current device status."""
    if device_key == "module_device_1":
        return wolk.DeviceStatus.CONNECTED
    elif device_key == "module_device_2":
        return wolk.DeviceStatus.CONNECTED


def handle_actuation(
    device_key: str, reference: str, value: Union[bool, int, float, str]
) -> None:
    """
    Set device actuator identified by reference to value.

    Must be implemented as non blocking.
    Must be implemented as thread safe.

    :param device_key: Device identifier
    :type device_key: str
    :param reference: Reference of the actuator
    :type reference: str
    :param value: Value to which to set the actuator
    :type value: Union[bool, int, float, str]
    """
    if device_key == "module_device_1":
        if reference == "SW":
            global switch
            switch = value

        elif reference == "MSG":
            global text
            text = value

    elif device_key == "module_device_2":
        if reference == "SL":
            global slider
            slider = value


def get_actuator_status(
    device_key: str, reference: str
) -> Tuple[wolk.ActuatorState, Union[bool, int, float, str]]:
    """
    Get current actuator status identified by device key and reference.

    Reads the status of actuator from the device
    and returns it as a tuple containing the actuator state and current value.

    Must be implemented as non blocking.
    Must be implemented as thread safe.

    :param device_key: Device key to which the actuator belongs to
    :type device_key: str
    :param reference: Actuator reference
    :type reference: str
    :returns: (state, value)
    :rtype: (ActuatorState, bool or int or float or str)
    """
    if device_key == "module_device_1":
        if reference == "SW":
            global switch
            return wolk.ActuatorState.READY, switch

        elif reference == "MSG":
            global text
            return wolk.ActuatorState.READY, text

    elif device_key == "module_device_2":
        if reference == "SL":
            global slider
            return wolk.ActuatorState.READY, slider


def get_configuration(
    device_key: str
) -> Dict[
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
]:
    """
    Get current configuration options.

    Reads device configuration and returns it as a dictionary
    with device configuration reference as key,
    and device configuration value as value.
    Must be implemented as non blocking.
    Must be implemented as thread safe.

    :param device_key: Device identifier
    :type device_key: str
    :returns: configuration
    :rtype: dict
    """
    if device_key == "module_device_1":
        global device_1_configuration_1
        global device_1_configuration_2
        return {
            "configuration_1": device_1_configuration_1,
            "configuration_2": device_1_configuration_2,
        }

    elif device_key == "module_device_2":
        global device_2_configuration_1
        return {"configuration_1": device_2_configuration_1}


def handle_configuration(
    device_key: str,
    configuration: Dict[
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
) -> None:
    """
    Change device's configuration options.

    Must be implemented as non blocking.
    Must be implemented as thread safe.

    :param device_key: Device identifier
    :type device_key: str
    :param configuration: Configuration option reference:value pairs
    :type configuration: dict
    """
    if device_key == "module_device_1":
        global device_1_configuration_1
        global device_1_configuration_2

        for reference, value in configuration.items():
            if reference == "configuration_1":
                device_1_configuration_1 = value
            elif reference == "configuration_2":
                device_1_configuration_2 = value

    elif device_key == "module_device_2":
        global device_2_configuration_1

        for reference, value in configuration.items():
            if reference == "configuration_1":
                device_2_configuration_1 = value


wolk_module = wolk.Wolk(
    host=configuration["host"],
    port=configuration["port"],
    module_name=configuration["module_name"],
    device_status_provider=get_device_status,
    actuation_handler=handle_actuation,
    acutator_status_provider=get_actuator_status,
    configuration_handler=handle_configuration,
    configuration_provider=get_configuration,
    firmware_handler=FirmwareHandlerImplementation(),
)


wolk_module.add_device(device1)
wolk_module.add_device(device2)

wolk_module.connect()

wolk_module.publish()

wolk_module.publish_configuration("module_device_1")
wolk_module.publish_configuration("module_device_2")

wolk_module.publish_acutator_status("module_device_1", "SW")
wolk_module.publish_acutator_status("module_device_1", "MSG")
wolk_module.publish_acutator_status("module_device_2", "SL")

wolk_module.publish_device_status("module_device_1")
wolk_module.publish_device_status("module_device_2")

while True:
    try:
        sleep(3)
        wolk_module.add_sensor_reading(
            "module_device_1", "T", randint(-20, 85), int(round(time() * 1000))
        )
        wolk_module.publish()
    except KeyboardInterrupt:
        break
