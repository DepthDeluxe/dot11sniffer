#!/bin/bash
IMG_PATH="/home/colin/downloads/ArchLinuxARM-rpi-latest.tar.gz"

DISK="/dev/mmcblk0"
BOOT_PART="${DISK}p1"
ROOT_PART="${DISK}p2"

# run sfdisk to create partition table entries
echo "Writing partition table"
sfdisk "$DISK" < sfdisk.txt

echo "Writing filesystems"
mkfs.ext4 "$ROOT_PART"
mkfs.vfat "$BOOT_PART"

# mount directory structure
mount "$ROOT_PART" /mnt
mkdir -p /mnt/boot
mount "$BOOT_PART" /mnt/boot

# copy over disk image
echo "Copying over disk image"
bsdtar -xpf "$IMG_PATH" -C /mnt

# copy over setup files
echo "Copying over node initialization files"
cp dot11setup.sh /mnt/root
cp dot11setup.service /mnt/etc/systemd/system/
ln -sf /etc/systemd/system/dot11setup.service /mnt/etc/systemd/system/multi-user.target.wants

# write hostname
echo "Enter hostname"
read hostname
echo "$hostname" > /mnt/etc/hostname

# unmount everything
echo "Unmounting"
umount -R /mnt
