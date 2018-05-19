#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of NVIDIA Power Manager - indicator applet for NVIDIA
# laptops.
# Copyright (C) 2018 Dmitri Lapin
#
# This work is based on the NVIDIA Power Indicator applet by
# André Brait Carneiro Fabotti
#
# NVIDIA Power Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NVIDIA Power Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NVIDIA Power Manager. If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import signal
import subprocess

from py3nvml import py3nvml

import gi.repository

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import AppIndicator3

from threading import Timer

from typing import Optional, List
from collections import namedtuple

ProcInfo = namedtuple('ProcInfo', ['name', 'pid', 'mem'])


class Indicator:
    APP_NAME = 'NVIDIA Power Manager'
    LIB_PATH = '/usr/lib/nvidia-power-manager/'
    SCRIPT_CMD = 'sudo ' + LIB_PATH + 'gpuswitcher'
    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    ACTIVE_ICON = os.path.join(BASEDIR, 'icons', 'active.svg')
    INACTIVE_ICON = os.path.join(BASEDIR, 'icons', 'inactive.svg')

    def __init__(self):
        self.menu = Gtk.Menu()

        self.switch_power_management = Gtk.MenuItem()
        self.switch_power_management.connect('activate', self.switch_nv_power)
        self.menu.append(self.switch_power_management)

        self.set_nv_pm_labels()

        item = Gtk.SeparatorMenuItem()
        item.show()
        self.menu.append(item)

        item = Gtk.MenuItem('Quit')
        item.connect('activate', self.terminate)
        item.show()
        self.menu.append(item)

        self.icon = AppIndicator3.Indicator.new(
            Indicator.APP_NAME,
            '',
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.icon.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.icon.set_menu(self.menu)

        self.t = None
        self.refresh()

    def terminate(self, window=None, data=None) -> None:
        self.t.cancel()
        Gtk.main_quit()

    def execute(self):
        Gtk.main()

    def nv_power_switch_string(self, nvidia_on) -> str:
        if nvidia_on is None:
            nvidia_on = self.is_nvidia_on()
        return 'Power {state} GPU'.format(
            state=('Off' if nvidia_on else 'On'))

    def is_nvidia_on(self) -> bool:
        with open('/proc/acpi/bbswitch', 'r') as fh:
            out = fh.readline()
        return out.strip().lower().endswith('on')

    def switch_nv_power(self, dude) -> None:
        if self.is_nvidia_on():
            self.turn_nv_off()
        else:
            self.turn_nv_on()

    def turn_nv_on(self) -> None:
        os.system(Indicator.SCRIPT_CMD + ' on')
        self.set_nv_pm_labels()

    def get_device_procs(self, device_id: int) -> Optional[List[ProcInfo]]:
        py3nvml.nvmlInit()
        dev_count = py3nvml.nvmlDeviceGetCount()  # type: int
        if not (0 <= device_id < dev_count):
            raise RuntimeError('Failed to query GPU with nvml')
        handle = py3nvml.nvmlDeviceGetHandleByIndex(device_id)
        result = []
        try:
            for proc in py3nvml.nvmlDeviceGetComputeRunningProcesses(handle):
                try:
                    name = str(py3nvml.nvmlSystemGetProcessName(proc.pid))
                except py3nvml.NVMLError as err:
                    if (err.value == py3nvml.NVML_ERROR_NOT_FOUND):
                        # exited?
                        continue
                    raise
                mem = proc.usedGpuMemory / 1024 / 1024
                result.append(ProcInfo(name, proc.pid, mem))
        finally:
            py3nvml.nvmlShutdown()

        return result

    def turn_nv_off(self) -> None:
        message = None
        try:
            procs = self.get_device_procs(0)
        except Exception as e:
            procs = None
            message = 'Failed to query device: {error}'.format(error=e)
        else:
            if len(procs) > 0:
                proc_info = [
                    ('{proc.name} (pid: {proc.pid}, mem: '
                     '{proc.mem:0.1}MB').format(proc=p) for p in procs
                ]
                message = (
                    'It seems there are programs using the NVIDIA GPU. '
                    'They need to be stopped before turning the GPU off:\n'
                ) + proc_info.join('\n')
        if message is not None:
            dialog = Gtk.MessageDialog(None,
                                       Gtk.DialogFlags.MODAL,
                                       Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.OK,
                                       message)
            dialog.set_deletable(False)
            dialog.run()
        else:
            os.system(Indicator.SCRIPT_CMD + ' off')
            self.set_nv_pm_labels()

    def set_nv_pm_labels(self, nvidia_on=None) -> None:
        self.switch_power_management.set_label(
            self.nv_power_switch_string(nvidia_on))
        self.switch_power_management.show()

    def ignore(self, *args):
        return Gtk.ResponseType.CANCEL

    def refresh(self) -> None:
        self.t = Timer(2, self.refresh)
        self.t.start()

        nvidia_on = self.is_nvidia_on()
        self.icon.set_icon(
            Indicator.ACTIVE_ICON if nvidia_on else Indicator.INACTIVE_ICON)
        self.icon.set_title(
            'GPU powered ON' if nvidia_on else 'GPU powered OFF')
        self.set_nv_pm_labels(nvidia_on)


def kill_other_instances() -> None:
    otherpid = subprocess.run(['pgrep', '-f', 'nvidia-power-manager'])
    if otherpid.returncode == 0:
        otherpid = str(otherpid.stdout)  # type:str
        pidlist = otherpid.splitlines()  # type:List[str]
        for pid in pidlist:
            if pid and pid.isnumeric():
                pid = int(pid)  # type:int
                if pid != os.getpid():
                    try:
                        os.kill(pid, signal.SIGTERM)
                        os.kill(pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass


if __name__ == '__main__':

    # If bbswitch isn't installed or isn't supported, exit cleanly
    if not os.path.isfile('/proc/acpi/bbswitch'):
        sys.exit(0)

    kill_other_instances()
    Indicator().execute()
