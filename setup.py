"""Run this module to install package on your machine."""
#   Copyright 2020 WolkAbout Technology s.r.o.
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
from os import path

import setuptools

from wolk_gateway_module import __version__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="wolk-gateway-module",
    version=__version__,
    install_requires=["paho_mqtt==1.4.0"],
    include_package_data=True,
    license="Apache License 2.0",
    author="WolkAbout",
    author_email="info@wolkabout.com",
    description=(
        "SDK for gateway communication modules "
        "that connect to WolkAbout IoT Platform"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["IoT", "WolkAbout", "Internet of Things"],
    url="https://github.com/Wolkabout/WolkGatewayModule-SDK-Python",
    packages=setuptools.find_packages(exclude=("test",)),
    test_suite="unittest",
    python_requires=">=3.7.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Software Development :: Embedded Systems",
    ],
)
