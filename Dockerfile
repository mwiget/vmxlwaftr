FROM ubuntu:14.04.4
MAINTAINER Marcel Wiget

# install tools required in the running container
RUN apt-get -o Acquire::ForceIPv4=true update \
  && apt-get -o Acquire::ForceIPv4=true install -y --no-install-recommends \
  net-tools iproute2 dosfstools tcpdump bridge-utils numactl genisoimage \
  libaio1 libspice-server1 libncurses5 openssh-client libjson-xs-perl python-twisted

# fix usr/sbin/tcpdump by moving it into /sbin: 
#  error while loading shared libraries: libcrypto.so.1.0.0: 
#  cannot open shared object file: Permission denied
RUN mv /usr/sbin/tcpdump /sbin/

COPY build/snabb /usr/local/bin/

COPY build/qemu-v2.4.0-snabb.tgz /
#COPY build/qemu-v2.5.1.1-snabb.tgz /
RUN tar zxf /qemu-v*-snabb.tgz -C /usr/local/

RUN mkdir /yang /jetapp /jetapp/op /jetapp/utils

COPY yang/ietf-inet-types.yang yang/ietf-softwire.yang \
  yang/jnx-softwire.yang yang/jnx-softwire-dev.yang \
  jetapp/yang/op/junos-extension-odl.yang \
  jetapp/yang/op/junos-extension.yang \
  jetapp/yang/op/rpc-get-lwaftr.yang \
  jetapp/yang/op/rpc_get_lwaftr_state.py \
  jetapp/yang/op/rpc_get_lwaftr_statistics.py yang/

COPY jetapp/src/main.py jetapp/src/version.py jetapp/src/__init__.py /jetapp/
COPY jetapp/src/op/opglobals.py jetapp/src/op/opserver.py jetapp/src/op/__init__.py /jetapp/op/
COPY jetapp/src/utils/jetapplog.py jetapp/src/utils/__init__.py /jetapp/utils/

COPY launch.sh launch_snabb.sh launch_jetapp.sh top.sh topl.sh README.md VERSION \
  launch_snabbvmx_manager.sh snabbvmx_manager.pl show_affinity.sh nexthop.sh monitor.sh /

RUN date >> /VERSION

EXPOSE 8700 

ENTRYPOINT ["/launch.sh"]

CMD ["-h"]
