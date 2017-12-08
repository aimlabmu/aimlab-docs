# Elderly Robot Setup

This is a short guide to make robot for elderly operate properly.

## Clone the project

```sh
cd _projects

# this is a private repo, you will need to have permission to clone it
git clone https://<authenticated_user>@bitbucket.org/otalbs/elderly-robot-server.git
```

## Run the setup script

This will install as many components as possible automatically. It might take some time because of `FFmpeg` installation.

Here is a list of what to be installed:

- FFmpeg (build from source)
- Add ffmpeg to PATH
- All dependencies libs
- Mqtt Backend dependencies (node-ghk included)
- Python servo controller
- Go's libraries

```sh
cd elderly-robot-server/bashScripts

./installRequirements.sh
```

## [Config sound](http://blog.scphillips.com/posts/2013/01/sound-configuration-on-raspberry-pi-with-alsa/)

The newly installed OS usually limits the default volume of the attached audio device. To fix this we need to set default volume at the maximum. 

Get start with the `amixer` command by determining the audio device first. Try running `amixer controls`.

```sh
# determine the device first
$ amixer controls

# output
numid=3,iface=MIXER,name='PCM Playback Route'
numid=2,iface=MIXER,name='PCM Playback Switch'
**numid=1,iface=MIXER,name='PCM Playback Volume'**
numid=5,iface=PCM,name='IEC958 Playback Con Mask'
numid=4,iface=PCM,name='IEC958 Playback Default'
```

To get information of our attached device, run `amixer cget numid=1`.

```sh
# check current volume - this shows mono values = -2000
$ amixer cget numid=1

# output
numid=1,iface=MIXER,name='PCM Playback Volume'
  ; type=INTEGER,access=rw---R--,values=1,min=-10239,max=400,step=0
  : values=-2000
  | dBscale-min=-102.39dB,step=0.01dB,mute=1
```

Set the default value to max.

```sh
# set to 100% - values 400 is max
$ amixer cset numid=1 100%

# output
numid=1,iface=MIXER,name='PCM Playback Volume'
  ; type=INTEGER,access=rw---R--,values=1,min=-10239,max=400,step=0
  : values=400
  | dBscale-min=-102.39dB,step=0.01dB,mute=1
```

Save the settings to system.

```sh
# save the set state to system
$ sudo alsactl store
```

Finally, check the saved state, you should see `dbvalue.0 400`.

```sh
# check the state file
$ cat /var/lib/alsa/asound.state

# output
state.ALSA {
        control.1 {
                iface MIXER
                name 'PCM Playback Volume'
                value 400
                comment {
                        access 'read write'
                        type INTEGER
                        count 1
                        range '-10239 - 400'
                        dbmin -9999999
                        dbmax 400
                        dbvalue.0 400
                }
        }
        control.2 {
.
.
.
```

## Manual run

To run robot manually we need to run 3 main components orderly. Those 3 components are:

- MQTT backend (./mqttBackend)
- Python Server (./servocontroller)
- Go GUI (./gui)

It is as easy as typing these lines in separated terminal windows:

```sh
# first window
cd ~/_projects/elderly-robot-server/mqttBackend

# build is needed when source code is changed
npm run build

# serve it and done
npm run serve
```

```sh
# second window
cd ~/_projects/elderly-robot-server/servocontroller

python server_mqtt.py
```

```sh
# third window
cd ~/_projects/elderly-robot-server/gui

#build is needed when source code is changed
go build

# run it and new GUI window will pop up
./gui
```

## Auto run on boot

To run script automatically on boot is actually pretty easy and there are several ways to do. However, not every methods work with our system because of many factors such as environmental paths or order of scripts called on boot.

We used to have operable solution in Robot for Autistic Children which utilized lxsession autostart and crontab altogether. However, that needs LXDE or desktop to be installed. In Raspbian Lite version it is a bit more tricky.

With a long trial and error period, we finally found a way to do this using crontab and some proper delay. Solution is posted first and the explanation will be below.

For now it is pretty easy to do. Just copy `mainScript.sh` to `~/_scripts/` and put the following line to cronjob (`crontab -e`).

```sh
@reboot bash /home/pi/_scripts/mainScript.sh 2>> /home/pi/cronlog.txt
```

Next time the robot boot up, everything will be up and running.

### Explanation

There are some points to be noted here:

**Why do we need to copy `mainScript.sh` to `~/_scripts`?**

- Because somehow cron breaks the git object (`mainScript.sh` itself and related).
- If you happened to deal with this problem, you can still fix the repo following this [thread](https://stackoverflow.com/a/31647691/4010864) on SO. 

**What does `2>>` mean in the cron command?**

- `>>` is called redirection and is used to append string to file. `2` is the option to *only* append `stderr` to the file (stdout will be printed to screen) [[1]](http://teaching.idallen.com/cst8207/12w/notes/270_redirection.txt).
- We use this to catch error because every single script is run in background and there is no way else to see output [[2]](https://unix.stackexchange.com/a/118020/137764).
- There is also `>` which also write to file but it does not preserve old content (not append but overwrite).

**What does `&` do in `bash $SCRIPT_ROOT/mqttBackend.sh &`?**

- When bash script is run in the background and that bash script call another script which work indefinitely, there is no way that the following lines will be called because it stuck in the first script process. To avoid this, `&` forks the process to run separately and makes another process in following lines can be called. 