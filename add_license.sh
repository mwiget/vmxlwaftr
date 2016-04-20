#!/usr/bin/env bash

# no longer needed. 15.1F4 has limited config_drive support
# that allows placing license.lic files on it and load them at genesis

MGMTIP=$1
IDENTITY=$2
LICENSE=$3

if [ ! -f "$LICENSE" ]; then
  echo "no license file found at $LICENSE"
  echo "Usage: $0 mgmt-ip-adress identity license-file"
  exit 1
fi

# With IPv6 addresses, use square brackets for scp
if [[ $MGMTIP == *":"* ]]; then
  MGMTIPSCP="[$MGMTIP]"
else
  MGMTIPSCP=$MGMTIP
fi

# vRE might not be up for a while, so keep trying to upload the license file ...
while true; do
  scp -o StrictHostKeyChecking=no -i $IDENTITY $LICENSE snabbvmx@$MGMTIPSCP:
  if [ $? == 0 ]; then
    echo "transfer successful"
    break;
  fi
  echo "license upload failed ($?), sleeping 5 seconds ..."
  sleep 5
done

FILE=`basename $LICENSE`
echo "loading license file $FILE ..."
ssh -o StrictHostKeyChecking=no -i $IDENTITY snabbvmx@$MGMTIP "request system license add $FILE"
if [ ! $? == 0 ]; then
  echo "ssh snabbvmx@MGMTIP failed"
  exit 1
fi
