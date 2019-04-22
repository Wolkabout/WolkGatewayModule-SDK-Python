"""Configuration template for registering device on WolkAbout IoT Platform."""
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

from data_type import DataType


class ConfigurationTemplate:
    """Configuration template for registering device on Platform.

    :ivar data_type: Configuration data type
    :vartype data_type: wolk_gateway_module.model.data_type.DataType
    :ivar default_value: Default value of configuration
    :vartype default_value: str
    :ivar description: Description of configuration
    :vartype description: str
    :ivar labels: Labels of fields when data size > 1
    :vartype labels: str
    :ivar maximum: Maximum configuration value
    :vartype maximum: int
    :ivar minimum: Minimum configuration value
    :vartype minimum: int
    :ivar name: Configuration name
    :vartype name: str
    :ivar reference: Configuration reference
    :vartype reference: str
    :ivar size: Data size
    :vartype size: int
    """

    def __init__(
        self,
        name,
        reference,
        data_type,
        description=None,
        size=1,
        labels=None,
        default_value=None,
        minimum=None,
        maximum=None,
    ):
        """Configuration template for device registration request.

        :param name: Configuration name
        :type name: str
        :param reference: Configuration reference
        :type reference: str
        :param data_type: Configuration data type
        :type data_type: wolk_gateway_module.model.data_type.DataType
        :param description: Configuration description
        :type description: str or None
        :param size: Configuration data size
        :type size: int
        :param labels: Comma separated data labels when data size > 1
        :type labels: str or None
        :param default_value: Default configuration value
        :type default_value: str or None
        :param minimum: Minimum configuration value
        :type minimum: int or None
        :param maximum: Maximum configuration value
        :type maximum: int or None
        """
        self.name = name
        self.reference = reference
        self.description = description
        self.minimum = minimum
        self.maximum = maximum
        self.default_value = default_value
        if size < 1 or size > 3:
            raise ValueError("Size can only be 1, 2 or 3")
        if size == 1:
            self.size = 1
            self.labels = None
        else:
            self.size = size
            if not labels:
                raise ValueError("Lables must be provided for size > 1")
            self.labels = labels
        if not isinstance(data_type, DataType):
            raise ValueError("Invalid data type given")
        self.data_type = data_type

    def __repr__(self):
        """Make string representation of configuration template.

        :returns: representation
        :rtype: str
        """
        return (
            f"ConfigurationTemplate(name='{self.name}', "
            f"reference='{self.reference}', description='{self.description}', "
            f"data_type='{self.data_type}', "
            f"minimum='{self.minimum}', maximum='{self.maximum}')"
            f"default_value='{self.default_value}', "
            f"size='{self.size}', "
            f"labels='{self.labels}')"
        )
