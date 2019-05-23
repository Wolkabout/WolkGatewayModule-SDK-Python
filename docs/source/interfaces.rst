User implemented functions
==========================

In order to enable some functionalities like actuators, configurations and
firmware update, certain functions or classes must be implemented.

This page will explain the mechanisms behind each of these functionalities.


Device status provider
----------------------

In order to know what devices are currently available to receive commands,
the Platform and gateway need to be notified of all of the device's current status.
Whether they are connected, offline, in sleep mode or in service mode.
Once the connection to the gateway is terminated, the module will automatically publish
offline states for all devices that have been added to it.

*Note:* This function is **required** in order to create a ``Wolk`` object.

.. automethod:: wolk_gateway_module.interface.device_status_provider.get_device_status

An stub implementation would look something like this:

.. code-block:: python
    
    def get_device_status(device_key: str) -> wolk_gateway_module.DeviceStatus:
    """Return current device status."""
        if device_key == "DEVICE_KEY":
            # Handle getting current device status here
            return wolk_gateway_module.DeviceStatus.CONNECTED  # OFFLINE, SLEEP, SERVICE_MODE


Actuator functions
------------------

Actuators enable remote control over a device peripheral that can change between predefined states,
like turning a switch on or off, or setting a light dimmer to 20%. In order to enable remote control,
the Platform first needs to be notified about the actuators current state - is it ready to receive a command, is it busy changing its position
or perhaps something has gone wrong with the actuator and it is unable to perform at that moment.
This information about the actuator's current state and value is obtained through an actuator status provider function.

.. automethod:: wolk_gateway_module.interface.actuator_status_provider.get_actuator_status

An stub implementation would look something like this:

.. code-block:: python
    
    def get_actuator_status(
    device_key: str, reference: str
    ) -> Tuple[wolk_gateway_module.ActuatorState, Union[bool, int, float, str]]:
    """
    Get current actuator status identified by device key and reference.

    Reads the status of actuator from the device
    and returns it as a tuple containing the actuator state and current value.

    Must be implemented as non blocking.
    Must be implemented as thread safe.
    """
    if device_key == "DEVICE_KEY":
        if reference == "SW":
            # Handle getting current actuator value here
            return wolk_gateway_module.ActuatorState.READY, switch.value  # BUSY, ERROR
