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

from setuptools import setup, find_packages

setup(
    name='nvidia-power-manager',
    use_scm_version=True,
    install_requires=[
        'py3nvml'
    ],
    setup_requires=[
        'setuptools_scm'
    ],
    description='Indicator applet to turn On / Off nvidia GPU on laptops',
    author='Dmitri Lapin',
    author_email='lapin@cvisionlab.com',
    url='https://github.com/dm0/nvidia-power-manager',
    license='GPLv3',
    packages=find_packages(exclude=['tests.*']),
    package_data={'nvidia_power_manager': ['icons/*.svg', 'sbin/gpuswitcher']},
    entry_points={
        'console_scripts': [
            'nvidia-power-manager=nvidia_power_manager.app:main'
        ]
    },
    data_files=[
        ('/etc/xdg/autostart', [
            'nvidia_power_manager/etc/xdg/autostart/'
            'nvidia-power-manager.desktop'
        ]),
        ('/etc/sudoers.d', [
            'nvidia_power_manager/etc/sudoers.d/'
            '99-nvidia-power-manager-sudoers'
        ]),
        ('share/icons', [
            'nvidia_power_manager/icons/nvidia-power-manager-active.svg'
        ]),
        ('/usr/lib/nvidia-power-manager', [
            'nvidia_power_manager/sbin/gpuswitcher'
        ])
    ],
    dependency_links=[
        'git+https://github.com/fbcotter/py3nvml#egg=py3nvml'
    ],
    zip_safe=False
)
