# AIM Robot for Elderly Setup From Scratch

- Install Raspbian to new card
- sudo raspi-config > disable serial, enable SSH, I2C, expand filesystem (in advanced options), [change keyboard layout](https://thepihut.com/blogs/raspberry-pi-tutorials/25556740-changing-the-raspberry-pi-keyboard-layout) (localization option > keyboard layout > other > en-us > en-us > ok > sudo reboot)
- connect to internet by adding these line in `/etc/wpa_supplicant/wpa_supplicant.conf

```sh
network={
    ssid="AIMLAB_2.4G"
    psk="lab_internet_pw"
}
```
then run `wpa_cli -i wlan0 reconfigure` should output as `OK`. You can check ip by running `ifconfig`.

- connect to rpi via SSH with `ssh pi@<ip>` using default pw of rpi.

- fix screen rotation `sudo nano /boot/config.txt` and fill in 

```sh
# Custom Settings
display_rotate=2
sudo reboot
```

### Install fundamental packages

#### Git

```sh
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install git-core
```

#### gpio

```sh
cd
git clone git://git.drogon.net/wiringPi
```

### Config tty serial port ([ref](https://raspberrypi.stackexchange.com/questions/47671/why-my-program-wont-communicate-through-ttyama0-on-raspbian-jessie/47851#47851))


### Install I2C

``` sh
// check I2C port
$ lsmod | grep i2c

// output
i2c_bcm2835             7167  0
i2c_dev                 6913  0

// check dtparam=i2c_arm=on
sudo cat /boot/config.txt | grep dtparam

// output
dtparam=i2c_arm=on
#dtparam=i2s=on
dtparam=spi=on
dtparam=audio=on

// add i2c-dev and snd-bcm2835 to /etc/modules
sudo nano /etc/modules

// should look like this
# /etc/modules: kernel modules to load at boot time.
#
# This file contains the names of kernel modules that should be loaded
# at boot time, one per line. Lines beginning with "#" are ignored.

i2c-dev
snd-bcm2835
```

This may not need. (note from before)

```sh
// install i2c-tools and test with this command
sudo apt-get install i2c-tools
sudo i2cdetect –y 1
```

### Install Python



### Install LIRC

```sh
// install packages
sudo apt-get install lirc
sudo apt-get install python3-lirc # or python-lirc
sudo nano /etc/modules

// add
lirc_dev
lirc_rpi gpio_in_pin=4
```

```sh
sudo nano /etc/lirc/hardware.conf

// add
# Arguments which will be used when launching lircd
LIRCD_ARGS="--uinput"
# Don't start lircmd even if there seems to be a good config file
# START_LIRCMD=false
# Don't start irexec, even if a good config file seems to exist.
# START_IREXEC=false
# Try to load appropriate kernel modules
LOAD_MODULES=true
# Run "lircd --driver=help" for a list of supported drivers.
DRIVER="default"
# usually /dev/lirc0 is the correct setting for systems using udev
DEVICE="/dev/lirc0"
MODULES="lirc_rpi"
# Default configuration files for your hardware if any
LIRCD_CONF=""
LIRCMD_CONF=""
```

```sh
sudo nano /boot/config.txt

// add
dtoverlay=lirc-rpi:gpio_in_pin=4
```

```sh
sudo modprobe lirc_rpi
sudo /etc/init.d/lirc stop
sudo mode2 -d /dev/lirc0
```

> REF.
> - http://alexba.in/blog/2013/01/06/setting-up-lirc-on-the-raspberrypi/
> - http://www.raspberry-pi-geek.com/Archive/2014/03/Controlling-your-Pi-with-an-infrared-remote/(offset)/2
> - https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/lesson-23-ir-remote-control-sensor-kit-v2-0-for-b-plus.html

```sh
sudo /etc/init.d/lirc stop
irrecord -d /dev/lirc0 ~/lircd.conf
# FOLLOW
sudo cp /etc/lirc/lircd.conf /etc/lirc/lircd_original.conf
sudo cp ~/lircd.conf /etc/lirc/lircd.conf
sudo /etc/init.d/lirc restart
irw
```

> REF.
> - http://alexba.in/blog/2013/01/06/setting-up-lirc-on-the-raspberrypi/
> - http://www.ocinside.de/html/modding/linux_ir_irrecord_guide.html

```sh
Path tsudoo lirc configuration file
sudo cp ~/lircrc ~/.lircrc
sudo cp ~/lircrc /etc/lirc/lircrc

sudo nano ~/.lircrc #local
sudo nano /etc/lirc/lircrc #global

begin
  button = BTN_1
  prog = myprogram
  config = one
end

begin
  button = BTN_2
  prog = myprogram
  config = two
end

begin
  button = BTN_3
  prog = myprogram
  config = three
end

begin
  button = BTN_4
  prog = myprogram
  config = four
end

begin
  button = BTN_5
  prog = myprogram
  config = five
end

begin
  button = BTN_6
  prog = myprogram
  config = six
end

begin
  button = BTN_7
  prog = myprogram
  config = seven
end

begin
  button = BTN_8
  prog = myprogram
  config = eight
end

begin
  button = BTN_9
  prog = myprogram
  config = nine
end

begin
  button = BTN_0
  prog = myprogram
  config = zero
end

begin
  button = BTN_LEFT
  prog = myprogram
  config = left
end

begin
  button = BTN_RIGHT
  prog = myprogram
  config = right
end
```

**Python sample code**

```py
import lirc
import time

lastR = ""
thisR = ""

while True:
  sockid = lirc.init("myprogram", blocking=False)
  codeIR = lirc.nextcode()

  thisR = codeIR
   
  if thisR != lastR and thisR != []:

    print(codeIR)
    lastR = thisR
```

> REF. 
> - https://pypi.python.org/pypi/python-lirc
> - http://raspberrypi.stackexchange.com/questions/37579/lirc-no-output-from-irw
> - https://github.com/tompreston/python-lirc/blob/master/lirc/lirc.pyx

# FAQ

1. if cannot connect to `/dev/ttyS0` due to **no port found** or **permission denied**, solve by 1. disable serial then reboot 2. run `sudo systemctl mask serial-getty@ttyAMA0.service` and `gpio mode 15 ALT0; gpio mode 16 ALT0` 3. change `enable_uart=0` to `enable_uart=1` in `/boot/config.txt` and reboot this should solve.


