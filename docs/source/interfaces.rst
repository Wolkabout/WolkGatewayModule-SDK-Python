User implemented functions
==========================

In order to enable some functionalities like actuators, configurations and
firmware update, certain functions or classes must be implemented.

This page will explain the mechanisms behind each of these functionalities.


Device status provider
----------------------

In order to know what devices are currently available to receive commands,
the Platform and gateway need to be notified of all of the modules' device's current status.
Whether they are connected, offline, in sleep mode or in service mode.
Once the connection to the gateway is terminated, the module will automatically publish
offline states for all devices that have been added to it.

*Note:* This function is **required** in order to create a ``Wolk`` object.

.. automethod:: wolk_gateway_module.interface.device_status_provider.get_device_status

Available device states:

.. autoclass:: wolk_gateway_module.model.device_status.DeviceStatus
    :members:

An stub implementation would look something like this:

.. code-block:: python
    
    def get_device_status(device_key):
        if device_key == "DEVICE_KEY":
            # Handle getting current device status here
            return wolk_gateway_module.DeviceStatus.CONNECTED  # OFFLINE, SLEEP, SERVICE_MODE


Actuator functions
------------------

Actuators enable remote control over a device peripheral that can change between predefined states,
like turning a switch on or off, or setting a light dimmer to 20% intensity. 

In order to enable remote control, the Platform first needs to be notified
about the actuators current state - is it ready to receive a command, is it busy changing its position
or perhaps something has gone wrong with the actuator and it is unable to perform at that moment.
This information about the actuator's current state and value is obtained through an *actuator status provider* function.

.. automethod:: wolk_gateway_module.interface.actuator_status_provider.get_actuator_status

Available actuator states:

.. autoclass:: wolk_gateway_module.model.actuator_state.ActuatorState
    :members:


A stub implementation would look something like this:

.. code-block:: python
    
    def get_actuator_status(device_key, reference):
        if device_key == "DEVICE_KEY":
            if reference == "SW":
                # Handle getting current actuator value here
                return wolk_gateway_module.ActuatorState.READY, switch.value  # BUSY, ERROR


Now that the Platform and gateway are able to get information about the actuator's current value and state,
it should also be able to send commands to the actuator.
This is achieved through another function called *actuation handler*.

.. automethod:: wolk_gateway_module.interface.actuation_handler.handle_actuation

A stub implementation would look something like this:

.. code-block:: python

    def handle_actuation(device_key, reference, value):
        if device_key == "DEVICE_KEY":
            if reference == "SW":
                # Handle setting the actuator value here
                switch.value = value

Finally, these two functions are passed as arguments to the ``Wolk`` class
as ``actuation_handler`` and ``actuator_status_provider``

.. code-block:: python

    wolk_module = wolk.Wolk(
        host=configuration["host"],
        port=configuration["port"],
        module_name=configuration["module_name"],
        device_status_provider=get_device_status,
        actuation_handler=handle_actuation,
        actuator_status_provider=get_actuator_status,
    )

Once ``Wolk.connect()`` has been called, it will call ``actuator_status_provider`` 
to get the current actuator status for each actuator of all added device. 
However, publishing actuator statuses can be done explicitly by calling:

..  code-block:: python

    wolk_module.publish_actuator_status("DEVICE_KEY" ,"ACTUATOR_REFERENCE")



Configuration option functions
------------------------------

Configuration options enable modification of device properties from WolkAbout IoT Platform
with the goal to change device behavior, eg. measurement heartbeat,
enabling/disabling device interfaces, increase/decrease device logging level etc.

Configuration options require a similar way of handling messages as actuators.
When a configuration command is issued from WolkAbout IoT Platform, it will be passed
to a ``configuration_handler`` that will attempt to execute the command.
Then the ``configuration_provider`` will report back to WolkAbout IoT Platform
with the current values of the device's configuration options.

Configuration options are always sent as a whole, even when only one value changes.
They are sent as a dictionary, where the key represents the configuration's reference
and the value is the current value.

.. automethod:: wolk_gateway_module.interface.configuration_provider.get_configuration


Stub implementation:

.. code-block:: python

    def get_configuration(device_key):
        if device_key == "DEVICE_KEY":
            # Handle getting configuration values here
            return {
                "configuration_1": configuration_1.value,
                "configuration_2": configuration_2.value,
            }

After implementing how to get current configuration option values, another function for setting new values
is required

.. automethod:: wolk_gateway_module.interface.configuration_handler.handle_configuration


.. code-block:: python

    def handle_configuration(device_key,configuration):
        if device_key == "DEVICE_KEY":
            # Handle setting configuration values here
            for reference, value in configuration.items():
                if reference == "configuration_1":
                    configuration_1.value = value
                elif reference == "configuration_2":
                    configuration_2.value = value


Finally, these two functions are passed as arguments to the ``Wolk`` class
as ``configuration_handler`` and ``configuration_provider``

.. code-block:: python

    wolk_module = wolk.Wolk(
        host=configuration["host"],
        port=configuration["port"],
        module_name=configuration["module_name"],
        device_status_provider=get_device_status,
        configuration_handler=handle_configuration,
        configuration_provider=get_configuration,
    )

Once ``Wolk.connect()`` has been called, it will call ``configuration_provider`` 
to get the current configuration options for each added device with configurations. 
However, publishing configurations can be done explicitly by calling:

..  code-block:: python

    wolk_module.publish_configuration("DEVICE_KEY")


Enabling firmware update
------------------------

WolkAbout IoT Platform has the option of updating device software/firmware.
In order to enable this functionality on a device, the user has to implement
the ``FirmwareHandler`` abstract base class and pass it to ``Wolk``.

.. autoclass:: wolk_gateway_module.interface.firmware_handler.FirmwareHandler
    :members:

The enumerations used to report current firmware update states are listed below:

.. automodule:: wolk_gateway_module.model.firmware_update_status
    :members:


.. code-block:: python

    class FirmwareHandlerImplementation(wolk_gateway_module.FirmwareHandler):

        def install_firmware(self, device_key, firmware_file_path):
            if device_key == "DEVICE_KEY":
                print(
                    f"Installing firmware: '{firmware_file_path}' "
                    f"on device '{device_key}'"
                )
                # Handle the actual installation here

                if True:
                    # If installation was successful
                    self.on_install_success(device_key)
                else:
                    # If installation failed
                    status = wolk_gateway_module.FirmwareUpdateStatus(
                        wolk_gateway_module.FirmwareUpdateState.ERROR,
                        wolk_gateway_module.FirmwareUpdateErrorCode.INSTALLATION_FAILED,
                    )
                    self.on_install_fail(device_key, status)

        def abort_installation(self, device_key):
            if device_key == "DEVICE_KEY":
                # Manage to stop firmware installation
                status = wolk_gateway_module.FirmwareUpdateStatus(
                    wolk_gateway_module.FirmwareUpdateState.ABORTED
                )
                self.on_install_fail(device_key, status)

        def get_firmware_version(self, device_key):
            if device_key == "DEVICE_KEY":
                return device.firmware_version



An object of this class needs to be passed to ``Wolk`` like so:

.. code-block:: python

    wolk_module = wolk.Wolk(
        host=configuration["host"],
        port=configuration["port"],
        module_name=configuration["module_name"],
        device_status_provider=get_device_status,
        firmware_handler=FirmwareHandlerImplementation(),
    )

When ``Wolk.connect()`` is called it will use ``firmware_handler.get_firmware_version()`` for
each added device that has support for firmware update and report to WolkAbout IoT Platform.