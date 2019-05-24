WolkGatewayModule-SDK-Python documentation
==========================================

.. image:: wolkabout_gateway_module.gif


This package is meant to be used for developing Wolk gateway modules that enable
devices without IP connectivity to send their data to WolkAbout IoT Platform.

The user is responsible for providing the custom implementation that usually contains
the device’s network communication protocol, as well as for providing
the business logic and everything related to the used hardware and
the specifics of their particular use case.

However, all the communication that is directed towards the gateway through
WolkConnect - BUS Handler is already provided with this package, an open source implementation
written in Python 3.7 that uses the MQTT protocol over TCP/IP to communicate with 
`WolkGateway <https://github.com/Wolkabout/WolkGateway>`_.


**Contents:**

.. toctree::
   :maxdepth: 2

   device_creation
   interfaces
   wolk
   protocols
   abcs
   models



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

