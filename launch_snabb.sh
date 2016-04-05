#!/usr/bin/env bash
INT0=$1
VMXTAP=$2

# e.g. INT0="xe0" -> INT1="xe1"
INT1="${INT0:0:2}$((${INT0:2:1} + 1))"
DEV=$(cat pci_$INT0)
CORE=${DEV#*/}
PCI=${DEV%/*}
SLEEP=${INT0:2:1}

CPU=$(cat /sys/class/pci_bus/${PCI%:*}/cpulistaffinity | cut -d'-' -f1 | cut -d',' -f1)
NODE=$(numactl -H | grep "cpus: $CPU" | cut -d " " -f 2)
NUMACTL="numactl --membind=$NODE --physcpubind=$CORE"

while :
do
  # check if there is a snabb binary available in the mounted directory.
  # use that one if yes
  SNABB=/usr/local/bin/snabb
  if [ -f /u/snabb ]; then
    cp /u/snabb / 2>/dev/null
    SNABB=/snabb
  fi

  echo "launch snabbvmx for $INT0 on cpu $CORE (node $NODE) after $SLEEP seconds ..."
  if [ -z "$VMXTAP" ]; then
    CMD="$NUMACTL $SNABB snabbvmx lwaftr --conf snabbvmx-lwaftr-${INT0}.cfg --pci $PCI --id1 $INT0 --mac1 `cat mac_$INT0` --id2 $INT1 --mac2 `cat mac_$INT1` --sock %s.socket"
  else
    CMD="$NUMACTL $SNABB snabbvmx lwaftr --conf snabbvmx-lwaftr-${INT0}.cfg --pci $PCI --id1 $INT0 --mac1 `cat mac_$INT0` --id2 $INT1 --mac2 `cat mac_$INT1` --tap ${INT0}_snabb"
  fi
  echo $CMD
  sleep $SLEEP
  $CMD
  $SNABB gc # removing stale runtime files created by Snabb
  sleep 4
done
