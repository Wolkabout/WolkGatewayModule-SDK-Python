Protocol & connectivity
=======================

The ``Wolk`` class is modular, in the sense that it relies on implementation
of certain abstract base classes that each handle a certain aspect of the package:

- **Data protocol** - Parses messages related to device data (actuators, alarms, sensors & configurations)
- **Firmware update protocol** - Parses messages related to firmware update (sending current firmware version, handling installation commands, reporting current firmware installation status)
- **Registration protocol** - Parses messages related to device registration (sending registration requests, handling registration responses)
- **Status protocol** - Parses messages related to device status(send current device status, respond to device status requests)
- **Outbound message queue** - Store serialized messages before publishing them to the gateway/platform
- **Connectivity service** - Means of establishing connection to WolkGateway and exchanging messages

All listed items have already been implemented to work over MQTT using WolkAbout's JSON_PROTOCOL
for serializing messages and they will be listed in the remainder of this page.

If you are interested in implementing a different means of storing messages, or want to use
a different MQTT client, or even implement a custom message formatting protocol
you can do so by implementing these :ref:`Abstract base classes`.


JSON Data Protocol
------------------

.. autoclass:: wolk_gateway_module.json_data_protocol.JsonDataProtocol
    :members:


JSON Firmware Update Protocol
-----------------------------

.. autoclass:: wolk_gateway_module.json_firmware_update_protocol.JsonFirmwareUpdateProtocol
    :members:


JSON Registration Protocol
--------------------------

.. autoclass:: wolk_gateway_module.json_registration_protocol.JsonRegistrationProtocol
    :members:


JSON Status Protocol
--------------------

.. autoclass:: wolk_gateway_module.json_status_protocol.JsonStatusProtocol
    :members:


Outbound Message Deque
----------------------

.. autoclass:: wolk_gateway_module.outbound_message_deque.OutboundMessageDeque
    :members:


MQTT Connectivity Service
-------------------------

.. autoclass:: wolk_gateway_module.mqtt_connectivity_service.MQTTConnectivityService
    :members:
