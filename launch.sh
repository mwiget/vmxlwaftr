#!/bin/bash
#
qemu=/usr/local/bin/qemu-system-x86_64
snabb=/usr/local/bin/snabb

VCPMEM="8000"     # default memory for vRE/VCP in kBytes
VFPMEM="8000"     # default memory for vPFE/VFP in kBytes
VCPCPU="1"        # default cpu count for vRE/VCP
VFPCPU="3"        # default cpu count for vPFE/VFP
CPULIST="0-4"     # default cpu-list for taskset snabb

#---------------------------------------------------------------------------
function show_help {
  cat <<EOF
Usage:

docker run --name <name> --rm -v \$PWD:/u:ro \\
   --privileged -i -t marcelwiget/vmxlwaftr[:version] [-C <core>] \\
   -c <junos_config_file> -i identity [-l license_file] \\
   [-m <kbytes>] [-M <kBytes>] [-V <cores>] [-W <cores>] \\
   <image> <pci-address> [<pci-address> ...]

[:version]       Container version. Defaults to :latest

 -v \$PWD:/u:ro   Required to access a file in the current directory
                 docker is executed from (ro forces read-only access)
                 The file will be copied from this location

 -l  license_file to be loaded at startup (requires user snabbvmx with ssh
     private key given via option -i)

 -i  ssh private key for user snabbvmx 
     (required to access lwaftr config via netconf)

 -m  Specify the amount of memory for the vRE/VCP (default $VCPMEM kB)
 -M  Specify the amount of memory for the vPFE/VFP (default $VFPMEM kB)

 -V  number of vCPU's to assign to the vRE/VCP (default $VCPCPU)
 -W  number of vCPU's to assign to vPFE/VFP (default $VFPCPU)

 -C  pin snabb to a specific core(s) (in taskset -c format, defaults to 0)

 -d  Enable debug shell (launched before and after qemu runs)

<pci-address>    PCI Address of the Intel 825999 based 10GE port
                 Multiple ports can be specified, space separated

Example:
docker run --name lwaftr1 --rm --privileged -v \$PWD:/u:ro \\
  -i -t marcelwiget/vmxlwaftr -c lwaftr1.txt -i snabbvmx.key \\
  jinstall64-vrr-14.2R5.8-domestic.img 0000:05:00.0 0000:05:00.0

EOF
}

#---------------------------------------------------------------------------
function cleanup {

  set +e
  trap - EXIT SIGINT SIGTERM

  echo ""
  echo ""
  echo "vMX terminated."

  pkill qemu

  echo "waiting for qemu to terminate ..."
  while  true;
  do
    if [ "1" == "`ps ax|grep qemu|wc -l`" ]; then
      break
    fi
    sleep 5
    echo "force kill of qemu required ..."
    pkill -9 qemu
  done

  exit 0

}
#---------------------------------------------------------------------------

function addif_to_bridge {
  ip link set master $1 dev $2
}

function create_tap_if {
  ip tuntap add dev $1 mode tap
  ip link set $1 up promisc on
}

function create_mgmt_bridge {
# Requires network isolation (without --net=host). 
# Create local bridge br0 for MGMT and place eth0 in it
bridge="br0"
myip=`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`
gateway=`ip -4 route list 0/0 |cut -d' ' -f3`
ip addr flush dev eth0
ip link add name $bridge type bridge
ip link set up $bridge
ip addr add $myip/16 dev $bridge
route add default gw $gateway
ip link set master $bridge dev eth0
echo $bridge
}

function create_int_bridge {
  bridge="brint"
  tap="tapint"
  # need to create a tap interface, so the bridge
  # will use its mac address 
  ip tuntap add dev $tap mode tap
  ip link set $tap up
  ip link add name $bridge type bridge
  ip link set master $bridge dev $tap
  ip link set up $bridge
  ip addr add 128.0.0.100/16 dev $bridge
  echo $bridge
}

function mount_hugetables {
  >&2 echo "mounting hugepages ..."
  # mount hugetables, remove directory if this isn't possible due
  # to lack of privilege level. A check for the diretory is done further down
  mkdir /hugetlbfs && mount -t hugetlbfs none /hugetlbfs || rmdir /hugetlbfs

  # check that we are called with enough privileges and env variables set
  if [ ! -d "/hugetlbfs" ]; then
    >&2 echo "Can't access /hugetlbfs. Did you specify --privileged ?"
    exit 1
  fi

  hugepages=`cat /proc/sys/vm/nr_hugepages`
  if [ "0" -gt "$hugepages" ]; then
    >&2 echo "No hugepages found. Did you specify --privileged ?"
    exit 1
  fi
}

function create_vmxhdd {
  >&2 echo "Creating empty vmxhdd.img for vRE ..."
  qemu-img create -f qcow2 /tmp/vmxhdd.img 2G >/dev/null
  echo "/tmp/vmxhdd.img"
}

function create_config_drive {
  >&2 echo "Creating config drive (metadata.img) ..."
  mkdir config_drive
  mkdir config_drive/boot
  mkdir config_drive/config
  mkdir config_drive/config/license
  cat > config_drive/boot/loader.conf <<EOF
vmchtype="vmx"
vm_retype="RE-VMX"
vm_instance="0"
EOF
  cp /u/$CONFIG config_drive/config/juniper.conf
  # placing license files on the config drive isn't supported yet
  # but it is assumed, this is how it will work.
  if [ -f *.lic ]; then
    for f in *.lic; do
      cp $f config_drive/config/license
    done
  fi
  cd config_drive
  tar zcf vmm-config.tgz *
  rm -rf boot config
  cd ..
  # Create our own metadrive image, so we can use a junos config file
  # 100MB should be enough.
  dd if=/dev/zero of=metadata.img bs=1M count=100 >/dev/null 2>&1
  mkfs.vfat metadata.img >/dev/null 
  mount -o loop metadata.img /mnt
  cp config_drive/vmm-config.tgz /mnt
  umount /mnt
}

function launch_debug_shell {
  echo "Launching shell to troubleshoot. Exit to continue"
  set +e
  bash
  set -e
}

#==================================================================
# main()

echo "Juniper Networks vMX lwaftr Docker Container (unsupported prototype)"
echo ""

while getopts "h?c:m:l:i:C:dV:" opt; do
  case "$opt" in
    h|\?)
      show_help
      exit 1
      ;;
    C)  CPULIST=$OPTARG
      ;;
    V)  VCPCPU=$OPTARG
      ;;
    W)  VFPCPU=$OPTARG
      ;;
    m)  VCPMEM=$OPTARG
      ;;
    M)  VFPMEM=$OPTARG
      ;;
    c)  CONFIG=$OPTARG
      ;;
    l)  LICENSE=$OPTARG
      ;;
    i)  IDENTITY=$OPTARG
      ;;
    d)  DEBUG=$(($DEBUG + 1))
      ;;
  esac
done

shift "$((OPTIND-1))"

# first parameter is the vMX image
image=$1
shift

if [ ! -f "/u/$image" ]; then
  echo "Error: Can't find image $image"
  exit 1
fi 

if [[ "$image" =~ \.tgz$ ]]; then
  echo "extracting VMs from $image ..."
  tar -zxf /u/$image -C /tmp/ --wildcards vmx*/images/*img
  VCPIMAGE="`ls /tmp/vmx*/images/jinstall64-vmx*img`"
  cp $VCPIMAGE .
  VCPIMAGE=$(basename $VCPIMAGE)
  VFPIMAGE="`ls /tmp/vmx*/images/vFPC*img 2>/dev/null`"
  cp $VFPIMAGE .
  VFPIMAGE=$(basename $VFPIMAGE)
else
  echo "Error: $image must be a .tgz file"
  exit 1
fi

if [ ! -f "/u/$IDENTITY" ]; then
  echo "Error: Can't find private key file $identity"
  exit 1
fi

cp /u/$IDENTITY .
IDENTITY=$(basename $IDENTITY)
HDDIMAGE=$(create_vmxhdd)
MGMTIP="128.0.0.1"
$(mount_hugetables)
$(create_config_drive)
BRMGMT=$(create_mgmt_bridge)
BRINT=$(create_int_bridge)
# Create unique 4 digit ID used for this vMX in interface names
ID=$(printf '%02x%02x%02x' $[RANDOM%256] $[RANDOM%256] $[RANDOM%256])
# Create tap interfaces for mgmt
VCPMGMT="vcpm$ID"
VCPINT="vcpi$ID"
VFPMGMT="vfpm$ID"
VFPINT="vfpi$ID"
$(create_tap_if $VCPMGMT)
$(create_tap_if $VFPMGMT)
$(addif_to_bridge $BRMGMT $VCPMGMT)
$(addif_to_bridge $BRMGMT $VFPMGMT)
$(create_tap_if $VCPINT)
$(create_tap_if $VFPINT)
$(addif_to_bridge $BRINT $VCPINT)
$(addif_to_bridge $BRINT $VFPINT)

cat <<EOF

  vRE/VCP $VCPIMAGE with ${VCPMEM}kB and ${VCPCPU} cores
  vPFE/VFP $VFPIMAGE with ${VFPMEM}kB and ${VFPCPU} cores
  mgmt bridge $BRMGMT with interfaces $VCPMGMT and $VFPMGMT
  internal interface $VCPMGMT IP $MGMTIP BRMGMT $BRMGMT
  config=$CONFIG license=$LICENSE identity=$IDENTITY
  snabb: taskset -c $CPULIST 

EOF

set -e	#  Exit immediately if a command exits with a non-zero status.
trap cleanup EXIT SIGINT SIGTERM

echo "Building virtual interfaces and bridges for $@ ..."

INTNR=0	# added to each tap interface to make them unique
INTID="xe"

MACP=$(printf "02:%02X:%02X:%02X:%02X" $[RANDOM%256] $[RANDOM%256] $[RANDOM%256] $[RANDOM%256])

for DEV in $@; do # ============= loop thru interfaces start

  # add $DEV to list
  PCIDEVS="$PCIDEVS $DEV"
#  macaddr=$MACP:$(printf '%02X'  $INTNR)
  # create persistent mac address based on hostid and PCI#
  h=$(hostid)
  macaddr="02:${h:0:2}:${h:2:2}:${h:4:2}:${DEV:5:2}:0${DEV:11:1}"
  echo -n "$PCI" > /sys/bus/pci/drivers/ixgbe/bind 2>/dev/null
  INT="${INTID}${INTNR}"
  INTLIST="$INTLIST $INT"
  echo "$DEV" > pci_$INT
  echo "$macaddr" > mac_$INT

  NETDEVS="$NETDEVS -chardev socket,id=char$INTNR,path=./${INT}.socket,server \
   -netdev type=vhost-user,id=net$INTNR,chardev=char$INTNR \
   -device virtio-net-pci,netdev=net$INTNR,mac=$macaddr"

  TAP="$INTID${INTNR}"    # -> tap/monitor interfaces xe0, xe1 etc
  $(create_tap_if $TAP)

  INTNR=$(($INTNR + 1))

done # ===================================== loop thru interfaces done

# Check config for snabbvmx group entries. If there are any
# run its manager to create an intial set of configs for snabbvmx 
sx="\$(grep ' snabbvmx-' /u/$CONFIG)"
if [ ! -z "\$sx" ] && [ -f ./snabbvmx_manager.pl ]; then
    ./snabbvmx_manager.pl /u/$CONFIG
fi

for INT in $INTLIST; do
  ./launch_snabb.sh $INT $CPULIST &
  sleep 2
done

#if [ ! -z "$DEBUG" ]; then
#  launch_debug_shell
#fi

# launch vPFE/VFP

CMD="$qemu -M pc -smp $VFPCPU --enable-kvm -m $VFPMEM -numa node,memdev=mem \
  -cpu SandyBridge,+rdrand,+fsgsbase,+f16c \
  -object memory-backend-file,id=mem,size=${VFPMEM}M,mem-path=/hugetlbfs,share=on \
  -drive if=ide,file=$VFPIMAGE \
  -netdev tap,id=tf0,ifname=$VFPMGMT,script=no,downscript=no \
  -device virtio-net-pci,netdev=tf0,mac=$MACP:A1 \
  -netdev tap,id=tf1,ifname=$VFPINT,script=no,downscript=no \
  -device virtio-net-pci,netdev=tf1,mac=$MACP:B1 \
  -device isa-serial,chardev=charserial0,id=serial0 \
  -chardev socket,id=charserial0,host=127.0.0.1,port=8700,telnet,server,nowait \
  $NETDEVS -vnc 127.0.0.1:5901 -daemonize"
echo $CMD
$CMD

if [ -f /u/$LICENSE ]; then
  cp /u/$LICENSE .
  LICENSE=$(basename $LICENSE)
  ./add_license.sh $MGMTIP $IDENTITY $LICENSE &
fi

./launch_snabbvmx_manager.sh $MGMTIP $IDENTITY $CPULIST &

CMD="$qemu -M pc --enable-kvm -cpu host -smp $VCPCPU -m $VCPMEM \
  -drive if=ide,file=$VCPIMAGE -drive if=ide,file=$HDDIMAGE \
  -usb -usbdevice disk:format=raw:metadata.img \
  -device cirrus-vga,id=video0,bus=pci.0,addr=0x2 \
  -netdev tap,id=tc0,ifname=$VCPMGMT,script=no,downscript=no \
  -device e1000,netdev=tc0,mac=$MACP:A0 \
  -netdev tap,id=tc1,ifname=$VCPINT,script=no,downscript=no \
  -device virtio-net-pci,netdev=tc1,mac=$MACP:B0 -nographic"
echo $CMD
$CMD

if [ ! -z "$DEBUG" ]; then
  launch_debug_shell
fi

exit  # this will call cleanup, thanks to trap set earlier (hopefully)
