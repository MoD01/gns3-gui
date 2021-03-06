# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Default Docker settings.
"""

import sys
from gns3.node import Node

DOCKER_SETTINGS = {
    "use_local_server": sys.platform.startswith("linux"),  # Docker only supported on Linux
    "containers": []
}

DOCKER_CONTAINER_SETTINGS = {
    "default_name_format": "{name}-{0}",
    "symbol": ":/symbols/docker_guest.svg",
    "category": Node.end_devices,
    "start_command": "",
    "name": "",
    "image": "",
    "adapters": 1,
    "environment": "",
    "console_type": "telnet",
    "console_resolution": "1024x768",
    "console_http_port": 80,
    "console_http_path": "/"
}
