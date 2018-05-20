"""nvidia-power-manager package setup script"""

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
