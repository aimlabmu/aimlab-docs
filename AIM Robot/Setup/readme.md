# AIM Robot for Elderly Setup From Scratch

This is a note on how to set up a robot from blank SD card. We use Raspbian Stretch Lite version in this instruction. [Installation guide can be found on Raspberry Pi official site](https://www.raspberrypi.org/documentation/installation/installing-images/README.md). This doc is written orderly and it is recommended to follow orderly unless you know exactly what you are doing.

## Install OS

- Go to [Raspbian official download site](https://www.raspberrypi.org/downloads/raspbian/).
- Download Raspbian image file.
- Follow [installation instruction](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).

----

## Raspberry Pi config

For some reasons, the screen attached to the robot will not display correctly on newly OS installed SD card. Thus we will have to used upside down until we can connect to the robot with SSH. Almost all steps require reboot, each round would take not more than a minute.

Run `sudo raspi-config` and make changes as follow:

- Interfacing Options
  - Disable Serial
  - Enable SSH, I2C
- Advanced Options
  - Expand Filesystem
- Localisation Options
  - [Change keyboard layout](https://thepihut.com/blogs/raspberry-pi-tutorials/25556740-changing-the-raspberry-pi-keyboard-layout) 
    - Keyboard Layout > Other > en-US > en-US > OK
    - Will have to reboot to see change.

----

## WPA config (For WiFi connection)

Run following command to open WiFi setup file in editor called nano.

```sh
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Then add these lines at the bottom of the files.

```sh
network={
    ssid="AIMLAB_2.4G"
    psk="lab_internet_pw"
}
```

To connect run `wpa_cli -i wlan0 reconfigure`, this should output as `OK`. You can check ip by running `ifconfig`.

----

## Connect to the robot using SSH

With ip from last step, we can now access the robot using SSH by running this command.

```sh
ssh pi@<ip>
```

Default password of Raspberry Pi is used.

----

## Fix screen rotation

Go to edit boot config file by running `sudo nano /boot/config.txt` and fill in these lines at the bottom of the file then reboot the system.

```sh
### Custom Settings
# display
hdmi_group=2
hdmi_mode=87
hdmi_cvt 800 480 60 6 0 0 0
display_rotate=2
```

----

## Proxy settings

If we have to use `AIMLAB_2.4G` to update and install package, proxy should be set for `apt-get`, to set it do as follow:

```sh
sudo nano /etc/apt/apt.conf.d/10proxy

# 10proxy file
Acquire::http::proxy "http://<usr>:<pw>@proxy-sa.mahidol:8080/";
```

----

## Install fundamental packages

### Git

```sh
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install git-core
```

> **NOTE!**
>
> At this point you may notice something like:
>
> ```
> apt-listchanges: Can't set locale; make sure $LC_* and $LANG are > correct!
> perl: warning: Setting locale failed.
> perl: warning: Please check that your locale settings:
>         LANGUAGE = (unset),
>         LC_ALL = (unset),
>         LC_TIME = "th_TH.UTF-8",
>         LC_MONETARY = "th_TH.UTF-8",
>         LC_CTYPE = "en_US.UTF-8",
>         LC_ADDRESS = "th_TH.UTF-8",
>         LC_TELEPHONE = "th_TH.UTF-8",
>         LC_NAME = "th_TH.UTF-8",
>         LC_MEASUREMENT = "th_TH.UTF-8",
>         LC_IDENTIFICATION = "th_TH.UTF-8",
>         LC_NUMERIC = "th_TH.UTF-8",
>         LC_PAPER = "th_TH.UTF-8",
>         LANG = "C.UTF-8"
>     are supported and installed on your system.
> perl: warning: Falling back to a fallback locale ("C.UTF-8").
> locale: Cannot set LC_CTYPE to default locale: No such file or directory
> locale: Cannot set LC_ALL to default locale: No such file or directory
> ```
>
> Just leave it as it is, don't worry about it. For more information check these stackoverflow threads [trying to fix [1]](https://askubuntu.com/questions/162391/how-do-i-fix-my-locale-issue), [failed and why it's failed [2]](https://stackoverflow.com/questions/2499794/how-to-fix-a-locale-setting-warning-from-perl).

### [GPIO](http://wiringpi.com/download-and-install/)

```sh
mkdir ~/_installations
cd ~/_installations

git clone git://git.drogon.net/wiringPi

cd ~/wiringPi
./build
```

----

## Install Python

Get Miniconda installation script and check its checksum by running

```sh
cd ~/_installations

wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh

md5sum Miniconda3-latest-Linux-armv7l.sh
```

Install by running

```sh
/bin/bash Miniconda3-latest-Linux-armv7l.sh
```

> For future version of miniconda please check at the [continuum repository](http://repo.continuum.io/miniconda/) and search for `Miniconda3-latest-Linux-armv7l.sh`.

Finally update conda and install `ipython`

```sh
source ~/.bashrc

conda update conda
conda install ipython
```

----

## Install I2C

Check I2C port

``` sh
$ lsmod | grep i2c

# output
i2c_bcm2835             7167  0
i2c_dev                 6913  0
```

Check if this line `dtparam=i2c_arm=on` is uncommented

```sh
sudo cat /boot/config.txt | grep dtparam

# output
dtparam=i2c_arm=on
#dtparam=i2s=on
dtparam=spi=on
dtparam=audio=on
```

Add `i2c-dev` and `snd-bcm2835` to `/etc/modules`

```sh
sudo nano /etc/modules

# should look like this
# /etc/modules: kernel modules to load at boot time.
#
# This file contains the names of kernel modules that should be loaded
# at boot time, one per line. Lines beginning with "#" are ignored.

i2c-dev
snd-bcm2835
```

Check i2c connections

- `0x20` = Chest circle lights
- `0x21` = Servo motors switch
- `0x4d` = Voltage level

```sh
# install tools and test with this command
sudo apt-get install i2c-tools
sudo apt-get install python3-smbus

# check i2c connections
sudo i2cdetect –y 1

# output
pi@raspberrypi:~ $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: 20 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- 4d -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

----

## [Install LIRC](https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b)

### Installation and pre-test

Install packages

```sh
sudo apt-get install lirc
# sudo apt-get install python3-lirc # is NOT in raspbian stretch repo yet
wget https://github.com/tompreston/python-lirc/releases/download/v1.2.1/python3-lirc_1.2.1-1_armhf.deb

sudo dpkg -i python3-lirc_1.2.1-1_armhf.deb
```

Add the following lines to `/etc/modules`

```sh
lirc_dev
lirc_rpi gpio_in_pin=4
```

Add the following lines to `/etc/lirc/hardware.conf`

```sh
# Arguments which will be used when launching lircd
LIRCD_ARGS="--uinput --listen"

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

Add the following lines to `/boot/config.txt`, then save and reboot with `sudo reboot`.

```sh
# lirc
dtoverlay=lirc-rpi:gpio_in_pin=4
```

Update the following lines to `/etc/lirc/lirc_options.conf`

```sh
driver    = default
device    = /dev/lirc0
```

Try these commands before testing remote

```sh
sudo /etc/init.d/lircd stop
sudo /etc/init.d/lircd start
sudo /etc/init.d/lircd status

# then reboot
sudo reboot
```

Run these commands to test

```sh
sudo /etc/init.d/lircd stop

# sudo modprobe lirc_rpi # may not need in stretch, if not work try doing it

sudo mode2 -d /dev/lirc0

# try pressing a key on remote, there should be some output like below
pulse 560
space 1706
pulse 535
```

> REF.
>
> - [Setting up LIRC on the Raspberry Pi](http://alexba.in/blog/2013/01/06/setting-up-lirc-on-the-raspberrypi/)
> - [Controlling your Pi with an infrared remote](http://www.raspberry-pi-geek.com/Archive/2014/03/Controlling-your-Pi-with-an-infrared-remote/(offset)/2)
> - [Lesson 23: IR remote control sensor kit v2.0 for B+](https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/lesson-23-ir-remote-control-sensor-kit-v2-0-for-b-plus.html)

### Set up IR keys

To set IR remote manually you will have to follow these commands. However, we already have recorded config files and what we have to do is just to copy.

#### Manually set commands

```sh
# stop service and run recorder
sudo /etc/init.d/lircd stop
irrecord -d /dev/lirc0 ~/lircd.conf

# when finish the lircd.cond will be saved to ~
# thus backup the original in /etc/lirc and copy there
sudo cp /etc/lirc/lircd.conf /etc/lirc/lircd_original.conf
sudo cp ~/lircd.conf /etc/lirc/lircd.conf
```

> REF.
>
> - [Setting up LIRC on the Raspberry Pi](http://alexba.in/blog/2013/01/06/setting-up-lirc-on-the-raspberrypi/)
> - [Linux IR: irrecord guide](http://www.ocinside.de/html/modding/linux_ir_irrecord_guide.html)

#### Copy commands

First, download and unzip

```sh
# Download files with wget
cd ~/_installations

wget "https://www.dropbox.com/s/08xttu8vaad2qn0/lirc_configs.zip"
# or
wget "https://drive.google.com/uc?authuser=0&id=1xWDpv7yny6_F8lTQMugeYN8l8fheBPwF&export=download" -O lirc_configs.zip

# unzip to lirc_configs folder
unzip lirc_configs.zip -d lirc_configs
```

Then, copy `lircd.conf` to `/etc/lirc/` and `lircrc` to `~` as dotfile and to `/etc/lirc/` as normal file.

```sh
# still in ~/_installations
cd lirc_configs

# copy conf file
sudo cp lircd.conf /etc/lirc/lircd.conf

# copy lircrc file
sudo cp lircrc ~/.lircrc # for local
sudo cp lircrc /etc/lirc/lircrc # for global
```

**Test remote configs**

```sh
# restart service
sudo /etc/init.d/lircd restart

# run this and test remote
irw
```

### Troubleshooting

If you follow all steps but it still doesn't work, try fix file permission as follow:

```sh
sudo chmod 777 ~/.lircrc
sudo chmod 777 /etc/lirc/lircrc
sudo chmod 777 /etc/lirc/lircd.conf
```

### Python sample code

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
>
> - [python-lirc](https://pypi.python.org/pypi/python-lirc)
> - [LIRC no output from irw](http://raspberrypi.stackexchange.com/questions/37579/lirc-no-output-from-irw)
> - [github.com/tompreston/python-lirc/blob/master/lirc/lirc.pyx](https://github.com/tompreston/python-lirc/blob/master/lirc/lirc.pyx)

----

## [Config tty serial port](https://raspberrypi.stackexchange.com/questions/47671/why-my-program-wont-communicate-through-ttyama0-on-raspbian-jessie/47851#47851)

As we have already disabled SSH in `raspi-config`, what we have to do next is to ensure that `/boot/cmdline.txt` has no ttyAMA0.

```sh
sudo cat /boot/cmdline.txt | grep ttyAMA0

# there should be no output
```

Then set the UART pins (15 and 16 wPi) state to ALT0.

```sh
gpio mode 15 ALT0; gpio mode 16 ALT0

# then check by gpio readall
gpio readall

# output (the format may not correct on narrow screen)
 +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 | ALT0 | 1 |  3 || 4  |   |      | 5v      |     |     |
 |   3 |   9 |   SCL.1 | ALT0 | 1 |  5 || 6  |   |      | 0v      |     |     |
 |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |
 |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |
 |  17 |   0 | GPIO. 0 |  OUT | 0 | 11 || 12 | 0 | OUT  | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI | ALT0 | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO |  OUT | 1 | 21 || 22 | 1 | IN   | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK | ALT0 | 0 | 23 || 24 | 0 | OUT  | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 1 | OUT  | CE1     | 11  | 7   |
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
 |   5 |  21 | GPIO.21 |  OUT | 0 | 29 || 30 |   |      | 0v      |     |     |
 |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
 |  13 |  23 | GPIO.23 |   IN | 1 | 33 || 34 |   |      | 0v      |     |     |
 |  19 |  24 | GPIO.24 |   IN | 1 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
 |  26 |  25 | GPIO.25 |   IN | 1 | 37 || 38 | 1 | IN   | GPIO.28 | 28  | 20  |
 |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+
```

Finally, add these lines to `/boot/config.txt`. Those commented lines were needed in Raspbian Jessie, so we put it here in case we happen to need it again.

```sh
# Set uart clock
enable_uart=1
#init_uart_clock=16000000
#sudo stty -F /dev/ttyAMA0 1000000

# Workaround for uart on RPi3
#core_freq=250
```

After rebooting, motors should be seen.

----

## Test Motor Control

Clone branch `rpi` from [dxl-cli](github.com/aimlabmu/dxl-cli.git) repo.

```sh
mkdir _testing
cd _testing

git clone -b rpi --single-branch https://github.com/aimlabmu/dxl-cli.git
```

Install dependencies using provided script.

```sh
cd dxl-cli
./install-dependencies.sh
```

When installation is finished, run these commands to set and test motors.

```sh
python change_servo_mode.py

ipython

# in ipython
Python 3.4.3 |Continuum Analytics, Inc.| (default, Aug 21 2015, 00:53:08)
Type "copyright", "credits" or "license" for more information.

IPython 4.0.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: from dxlcli import BasicController

In [2]: s = BasicController()

In [3]: s.getConnectIds()
Available ids are [1, 2, 3, 4]
```

This shows that all motors (id 1-4) are connected and ready to work.

----

## FAQ

1. if cannot connect to `/dev/ttyS0` due to **no port found** or **permission denied**, solve by 1. disable serial then reboot 2. run `sudo systemctl mask serial-getty@ttyAMA0.service` and `gpio mode 15 ALT0; gpio mode 16 ALT0` 3. change `enable_uart=0` to `enable_uart=1` in `/boot/config.txt` and reboot this should solve.


