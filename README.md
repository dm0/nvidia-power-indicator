# NVIDIA Power Manager

Indicator applet for laptop users with NVIDIA/Intel hybrid GPUs, allowing one
to manually turn the discrete GPU on or off when needed.

It should work on any Linux distribution that includes the minimum
dependencies listed in the Prerequisites section.

This version uses `bbswitch` to power the NVIDIA GPU off. It doesn't use 
`prime-select` or any other utilities so the primary idea of this applet is
to make it possible to manually turn discrete GPU ON or OFF. It assumes
specific setup when discrete GPU is only used for things like GPGPU and X
server runs on integrated GPU.

This implementation is based on the [NVIDIA Power Indicator](
https://github.com/andrebrait/nvidia-power-indicator) applet by
André Brait Carneiro Fabotti with the following changes:

* Organized as a `python3` package and can be installed using `pip`.
* Indicator icon displays only nVidia icon either color or symbolic -
  corresponds to enabled / disabled GPU.
* Indicator menu simplified and doesn't have option to turn management off.
* Using `py3nvml` module to query list of processes that use GPU (instead of
  invoking `pgrep`)
* Message box displaying information about GPU in use displays list of 
  processes that use GPU.

## Prerequisites

Make sure you have installed and enabled:

* NVIDIA driver, version 331.20 or higher
* `mesa-utils` package
* `python3` package
* `gir1.2-appindicator3` package
* `bbswitch-dkms` or equivalent package

Or simply run the following, which will install all dependencies and the latest NVIDIA driver for your GPU (if it's supported by NVIDIA's latest drivers).

```bash
sudo apt-get install python3 mesa-utils bbswitch-dkms gir1.2-appindicator3
sudo apt-get install $(sudo ubuntu-drivers devices | grep -o nvidia-[[:digit:]]*)
```

## Installation

There are two main ways to install this package: using pip or from Ubuntu PPA.

The first way is more pythonic but may fail to setup package properly. The package needs to install a file in `sudoers.d` and also XDG autostart file. Both are inside of `/etc` directory.  
Depending on the environment and pip version installation to `/etc` may silently fail in install those files to for example `/usr/local/lib/etc`.
This will result in application not starting with graphical session and also failing to switch GPU state if started manually.

The second way installs application as a `.deb` package. The downside is that application depends on `py3nvml` python package and that package is not available in Ubuntu repositories. So the PPA archive includes `python3-py3nvml`
package made from the published PyPI version.

### Install from PPA

Add PPA and update list of available packages:

```bash
sudo add-apt-repository ppa:dm0/nvidia-power-manager
sudo apt-get update
```

Install 

```bash
sudo apt-get install nvidia-power-manager
```

### Install using pip

Use `pip` to install package. This package installs XDG autostart file and 
`sudoers.d` file so `pip install` must be invoked with `sudo`.

```bash
sudo pip3 install git+https://github.com/dm0/nvidia-power-manager#egg=nvidia-power-manager
```

Applet will start on next reboot. Use the following command to start in current session:

```bash
nvidia-power-manager & disown
```

## Troubleshooting

### `appindicator` module missing
Install the `gir1.2-appindicator3` package.

### Couldn't find RGB GLX visual or fbconfig
Install the `mesa-utils` package.

### Installing from root session
Installing from root session in Ubuntu doesn't work. Use `sudo` to install package. 

### Application doesn't auto start when installed with pip
Use `pip3 show -f nvidia-power-manager` to view installed files.  
There should be files installed to `/etc`.

For example (not that path are shown relative to "Location"):
```
$ pip3 show -f nvidia-power-manager
Name: nvidia-power-manager
...
Location: /usr/local/lib/python3.6/dist-packages
Requires: py3nvml
Required-by: 
Files:
  ../../../../../etc/sudoers.d/99-nvidia-power-manager-sudoers
  ../../../../../etc/xdg/autostart/nvidia-power-manager.desktop
  ../../../../lib/nvidia-power-manager/gpuswitcher
  ../../../bin/nvidia-power-manager
  ../../../share/icons/nvidia-power-manager-active.svg
...
```

If files are installed to a wrong location you man fix it manually or install package from PPA.