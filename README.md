# Dot11Sniffer
The 802.11 device counting script for CSCI379.  This counts the number of active devices in an 802.11
network by using a network card in monitor mode.

# Initial Configuration
To configure your computer, you must do three things: (1) install `aircrack-ng` program and `scapy`
packet sniffing library, (2) configure NetworkManager or your chosen Linux network management utility
to ignore your wireless device, and (3) use Aircrack to enable monitor mode on your card.

## Install Aircrack and Scapy
```bash
apt-get install aircrack-ng scapy
```

## Configure NetworkManager
To tell NetworkManager to ignore your wireless card, first find the device's MAC address.  The `ip addr`
program will tell you the mac address of your device.  On my computer, the wireless device I use is
called `wlp0s20u2`.  Under that device, look for the string just to the right of the line that says
"link/ether".  It is a series of six hex number separated by colons.

Once you have your MAC address, modify `/etc/NetworkManager/NetworkManager.conf`.  In this file, add the
following.  If there is already a [keyfile] section, add it to that section.

```
[keyfile]
unmanaged-devices=mac:$MAC_ADDR
```

Where $MAC_ADDR is your MAC address **with** colons between them.  When added, make sure you restart
NetworkManager.  If you aren't sure how to do this, just restart your computer.  When NetworkManager is
brought back up and you plug your device in, NetworkManager should say "unmanaged" next to the device.

## Use Aircrack
Once the device is no longer managed by NetworkManager, use the `airmon-ng` utility to bring up a monitor
network interface.  This is done by typing:

```bash
airmon-ng start $DEVICE $CHANNEL
```

Where $DEVICE is the name of your device and $CHANNEL is the wireless channel you wish to listen on.  For
our CSCI379 project, use channel 6.  This application should create a virtual network device called `mon0`.
When using scapy, make sure you listen to this device and not on the hardware device.  This python script currently implicitly attempts to connect to the `mon0` interface although this may change in the future.
