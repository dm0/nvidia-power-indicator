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

## Troubleshooting

### `appindicator` module missing
Install the `gir1.2-appindicator3` package.

### Couldn't find RGB GLX visual or fbconfig
Install the `mesa-utils` package.

## Installation

Use `pip` to install package. This package installs XDG autostart file and 
`sudoers.d` file so `pip install` must be invoked with `sudo`.

```bash
sudo pip3 install git+https://github.com/dm0/nvidia-power-manager#egg=nvidia-power-manager
```

Applet will start on next reboot. Use the following command to start in current session:

```bash
nvidia-power-manager & disown
```
