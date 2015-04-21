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

import os
import tempfile

import logging
log = logging.getLogger(__name__)


class PacketCapture:

    """This class manage packet capture, it's a singleton"""

    def __init__(self):
        self._capture_files = {}

    def startCapture(self, vm, port, file_path):
        """
        Start the packet capture reader on this port

        :param vm: Instance of the virtual machine
        :param port: Instance of port where capture should be executed
        :param file_path: capture file path on server
        """
        log.info("{} has successfully started capturing packets on {}".format(vm.name(), port.name()))

        if vm.server().isLocal():
            try:
                port.startPacketCapture(file_path)
            except OSError as e:
                vm.error_signal.emit(vm.id(), "could not start the packet capture reader: {}: {}".format(e, e.filename))
        else:
            (fd, temp_capture_file_path) = tempfile.mkstemp()
            os.close(fd)
            port.startPacketCapture(temp_capture_file_path)
            self._capture_files[port] = temp_capture_file_path

            vm.server().get("/files/stream",
                            None,
                            body={"location": file_path},
                            context={"pcap_file": temp_capture_file_path, "vm": vm},
                            downloadProgressCallback=self._processDownloadPcapProgress,
                            showProgress=False)
        vm.updated_signal.emit()

    def _processDownloadPcapProgress(self, content, context={}, **kwargs):
        try:
            with open(context["pcap_file"], 'ab+') as f:
                f.write(content)
        except OSError as e:
            vm = context["vm"]
            vm.error_signal.emit(vm.id(), "could not write packet capture: {}: {}".format(e, context["pcap_file"]))

    def stopCapture(self, vm, port):
        """
        Stop the packet capture reader on this port

        :param vm: Instance of the virtual machine
        :param port: Instance of port where capture should be executed
        """
        log.info("{} has successfully stopped capturing packets on {}".format(vm.name(), port.name()))
        port.stopPacketCapture()
        if port in self._capture_files:
            try:
                os.remove(self._capture_files[port])
            except OSError as e:
                vm.error_signal.emit(vm.id(), "could not remove packet capture: {}: {}".format(e, self._capture_files[port]))
            self._capture_files[port] = None

    @staticmethod
    def instance():
        """
        Singleton to return only on instance of Servers.

        :returns: instance of Servers
        """

        if not hasattr(PacketCapture, "_instance"):
            PacketCapture._instance = PacketCapture()
        return PacketCapture._instance
