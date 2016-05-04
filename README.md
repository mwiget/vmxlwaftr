## Juniper Networks vMX lwaftr Docker Container

Usage:

```
docker run --name <name> --rm -v \$PWD:/u:ro \\
   --privileged -i -t marcelwiget/vmxlwaftr[:version] \\
   -c <junos_config_file> -i identity [-l license_file] \\
   [-m <kbytes>] [-M <kBytes>] [-V <cores>] [-W <cores>] \\
   <image> <pci-address/core> [<pci-address/core> ...]

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

 -d  launch debug shell before launching vMX

 -X  cpu list for vPFE and vRE

<pci-address/core>  PCI Address of the Intel 825999 based 10GE port with core to pin snabb on.  Multiple ports can be specified, space separated
```

Example:

```
docker run --name lwaftr1 --rm --privileged -v \$PWD:/u:ro \\
  -i -t marcelwiget/vmxlwaftr -c lwaftr1.txt -i snabbvmx.key \\
  jinstall64-vrr-14.2R5.8-domestic.img 0000:05:00.0/7 0000:05:00.0/8
```

## Release v0.7

- Use config drive to load license keys

- Cirros test image for CI instead of vMX
  wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img

- Improve logging and displaying of cached next_hop_mac for v4 and v6:
  From within the container, use 'snabb snabbvmx nexthop' to display
  the cached next hops per snabb process and protocol:
  # snabb snabbvmx nexthop
  1354: next_hop_mac for IPv4 is 00:00:00:00:00:00
  1354: next_hop_mac for IPv6 is 00:00:00:00:00:00
  1351: next_hop_mac for IPv4 is 02:44:44:44:44:44
  1351: next_hop_mac for IPv6 is 02:66:66:66:66:66

- Fix vlan support: Set vlan id under settings instead of ipv4_interface or
  ipv6_interfaces, because that vlan id is used for both

```
  groups {
    snabbvmx-lwaftr-xe0 {
      apply-macro settings {
        ring_buffer_size 1024;
        discard_threshold 100000;
        discard_check_timer 1;
        discard_wait 15;
        vlan 100;
      }
    ....
```

## Release v0.6

- Add "discard_wait <seconds>" to config to wait until jit.flush triggers again

```
  groups {
    snabbvmx-lwaftr-xe0 {
      apply-macro settings {
        discard_threshold 100000;
        discard_check_timer 1;
        discard_wait 20;
      }
      ...
   ```
     

- Add ingress/egress filter (ACL) support via PcapFilter:
[ https://github.com/SnabbCo/snabbswitch/tree/master/src/apps/packet_filter]()
  for ingress and egress and IPv4 and IPv6. The filter syntax is according
    to pcap-filter: [http://www.tcpdump.org/manpages/pcap-filter.7.html]()
    
```
    apply-macro ipv6_interface {
      ipv6_address 2001:db7:1::1;
      ipv6_mtu 9500;
      policy_icmpv6_incoming drop;
      policy_icmpv6_outgoing drop;
      icmpv6_rate_limiter_n_packets 6e5;
      icmpv6_rate_limiter_n_seconds 2;
      cache_refresh_interval 1;
      no_hairpinning;
      ipv6_ingress_filter "ip6";
      ipv6_egress_filter "ip6";
    }
      apply-macro ipv4_interface {
        ipv4_address 172.20.1.16;
        ipv4_mtu 9500;
        policy_icmpv4_incoming drop;
        policy_icmpv4_outgoing drop;
        cache_refresh_interval 1;
        ipv4_ingress_filter "ip";
        ipv4_egress_filter "ip";
        no_hairpinning;
      }
```

- Fix panic in passthru mode due to undefined discard_threshold

## Release v0.5

- fix mtu and display its setting at startup on console

## Release v0.4

- make discard_check_timer and threshold configurable
- change config knob to no_hairpinning
- fix error handling when files aren't available.
- Fix calculation of numanode

## Release v0.3

- Bug fixes in snabb with fragmentation and packets not matching binding table
- Fix linkup detection on some Intel 82599 card/cable combination 

## Release v0.2

- Monitor QPRDC and run jit.flush() if threshold exceeded
- remove snmp
- added info on mlock=on
- pass all traffic thru vmx if refresh interval set to 0
- show help if run without arguments
- options to define CPU list for vRE/vPFE, auto-calculate numa node

[https://github.com/mwiget/vmxlwaftr/tree/vmxlwaftr_v0.2]()

[https://github.com/mwiget/snabbswitch/tree/vmxlwaftr_v0.2]()

## Release v0.1

[https://github.com/mwiget/vmxlwaftr/tree/vmxlwaftr_v0.1]()

[https://github.com/mwiget/snabbswitch/tree/vmxlwaftr_v0.1]()

```
$ cat run-lwaftr1.sh
#!/usr/bin/env bash
NAME="lwaftr1"
#DEBUG="-d"
OPTIONS="-X 5 -m 2000"
CFG="lwaftr1-double.txt"
IMG="vmx-15.1F4.15.tgz"
IDENTITY="snabbvmx.key"
INTERFACES="0000:05:00.0/6 0000:05:00.1/7"
#LICENSE="license-eval.txt"
LICENSE="license-unlimited.txt"
echo "Launching vMX with $INTERFACES and options $DEBUG $OPTIONS ..."
docker pull marcelwiget/vmxlwaftr:v0.1
docker run --name $NAME -ti --privileged -v $PWD:/u:ro marcelwiget/vmxlwaftr:v0.1 -t -i $IDENTITY -c $CFG -l $LICENSE $DEBUG $OPTIONS $IMG $INTERFACES

```


IMIX bi-directional line rate over 10GE IPv4 <-> IPv6 mixed:
rx: 3.148 MPPS, 9.395 Gbps.

vMX config lwaftr1-double-v0.1.txt

Generator:

```
sudo taskset -c 6 ./snabbvmx generator --pci 0000:04:00.0 --mtu 9600 --mac 02:cf:69:15:05:00 --ipv4 10.10.0.0 --ipv6 2a02:587:f710::40 --lwaftr 2a02:587:f700::100 --count 2000000 --port 1024 --size 508  --rate 10 &

sudo taskset -c 7 ./snabbvmx generator --pci 0000:04:00.1 --mtu 9600 --mac 02:cf:69:15:05:01 --ipv4 10.10.0.0 --ipv6 2a02:587:f710::40 --lwaftr 2a02:587:f700::100 --count 2000000 --port 1024 --size 508  --rate 10 &
```

