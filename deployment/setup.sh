#!/bin/bash

PROOT="/home/sniffer/dot11sniffer"

if [ -d $PROOT ]; then
  echo "Project root found, updating environment..."
  pushd $PROOT

  git pull origin master
  echo "Pulling project dir: $?"

  puppet apply "$PROOT/deployment/sniffer.pp"
  echo "Applying puppet file: $?"

  popd
  exit 0
fi

echo "Project root not found, performing initial setup"

# apply rereq programs
pacman -S --noconfirm puppet git
echo "Installing prereq programs: $?"

# create the home directory for the user
mkdir "/home/sniffer"

# clone the dot11 sniffer repo
git clone "https://github.com/DepthDeluxe/dot11sniffer" "$PROOT"
echo "Cloning project dir: $?"

# apply the puppet file
puppet apply "$PROOT/deployment/sniffer.pp"
echo "Applying puppet file: $?"

exit 0
