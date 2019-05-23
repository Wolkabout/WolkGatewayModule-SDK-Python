Creating devices
================

Creating devices consists of defining individual templates for each device's
sensor, alarm, actuator and configuration option. All these templates are joined together
to create a device template that will contain information about all data
the device will yield and will be used to register the device on WolkAbout IoT Platform.

All of these templates have a field named *reference* that is used to identify
that particular source of information. This field needs to be **unique per device**.

On this page, each of these templates will be disambiguated and finally a device will be created.

The concept behind device templates is similar to classes in object-oriented programming,
so it helps to think about them like this:


    class -> object == device_template -> device

Where at the end of the process of creating a device, there is an uniquely identifiable object
that is then registered on WolkAbout IoT Platform

Sensors
-------
.. autoclass:: wolk_gateway_module.model.sensor_template.SensorTemplate
    :members:

    .. automethod:: wolk_gateway_module.model.sensor_template.SensorTemplate.__init__


Alarms
------

.. autoclass:: wolk_gateway_module.model.alarm_template.AlarmTemplate
    :members:

    .. automethod:: wolk_gateway_module.model.alarm_template.AlarmTemplate.__init__

Actuators
---------

.. autoclass:: wolk_gateway_module.model.actuator_template.ActuatorTemplate
    :members:

    .. automethod:: wolk_gateway_module.model.actuator_template.ActuatorTemplate.__init__


Configurations
--------------

.. autoclass:: wolk_gateway_module.model.configuration_template.ConfigurationTemplate
    :members:


    .. automethod:: wolk_gateway_module.model.configuration_template.ConfigurationTemplate.__init__

Device template
---------------

.. autoclass:: wolk_gateway_module.model.device_template.DeviceTemplate
    :members:

    .. automethod:: wolk_gateway_module.model.device_template.DeviceTemplate.__init__


Device
------

After a device template has been created, now a device can be created from it.

.. autoclass:: wolk_gateway_module.model.device.Device
    :members:

    .. automethod:: wolk_gateway_module.model.device.Device.__init__