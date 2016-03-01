#!/usr/bin/env bash
INT=$1
VMXTAP=$2

DEV=$(cat pci_$INT)
CORE=${DEV#*/}
PCI=${DEV%/*}

SLEEP=${INT:2:1}

while :
do
  # check if there is a snabb binary available in the mounted directory.
  # use that one if yes
  SNABB=/usr/local/bin/snabb
  if [ -f /u/snabb ]; then
    cp /u/snabb / 2>/dev/null
    SNABB=/snabb
  fi
  echo "launch snabbvmx for $INT on cpu $CORE after $SLEEP seconds ..."
  if [ -z "$VMXTAP" ]; then
    CMD="taskset -c $CORE $SNABB snabbvmx lwaftr --conf snabbvmx-lwaftr-${INT}.cfg --id $INT --pci $PCI --mac `cat mac_$INT` --sock %s.socket"
  else
    CMD="taskset -c $CORE $SNABB snabbvmx lwaftr --conf snabbvmx-lwaftr-${INT}.cfg --id $INT --pci $PCI --mac `cat mac_$INT` --tap ${INT}_snabb"
  fi
  echo $CMD
  sleep $SLEEP
  $CMD
  $SNABB gc # removing stale runtime files created by Snabb
  sleep 4
done
