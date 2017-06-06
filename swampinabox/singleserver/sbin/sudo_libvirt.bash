#!/bin/bash

# This file is subject to the terms and conditions defined in
# 'LICENSE.txt', which is part of this source code distribution.
#
# Copyright 2012-2017 Software Assurance Marketplace

BINDIR=`dirname "$0"`

. "$BINDIR"/swampinabox_install_util.functions

cp $BINDIR/../config_templates/10_slotusers /etc/sudoers.d/.
groupadd -f slotusers
groupmems -g slotusers -a swa-daemon
install -m 755 $BINDIR/../config_templates/qemu-kvm-us /usr/libexec/qemu-kvm-us
service libvirtd restart

#
# CSA-2693: Destroy the old "swamponabox" network before adding "swampinabox".
#

virsh net-uuid swamponabox 1>/dev/null 2>/dev/null
if [ $? -eq 0 ]; then
    virsh net-destroy swamponabox
    virsh net-undefine swamponabox
fi

virsh net-uuid swampinabox 1>/dev/null 2>/dev/null
if [ $? -ne 0 ]; then
    virsh net-define $BINDIR/../config_templates/swampinabox.xml
    virsh net-autostart swampinabox
    virsh net-start swampinabox
fi
