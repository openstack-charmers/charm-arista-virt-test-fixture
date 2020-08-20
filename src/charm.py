#!/usr/bin/env python3
#
# Copyright 2020 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
from pathlib import Path
import subprocess

import sys
sys.path.append('lib')

import charmhelpers.core.templating as ch_templating
from charmhelpers.core.host import (
    CompareHostReleases,
    lsb_release,
)
from charmhelpers.fetch import apt_install

from ops.main import main
import ops_openstack

logger = logging.getLogger(__name__)


class CharmAristaVirtTestFixture(ops_openstack.OSBaseCharm):

    PACKAGES = ['qemu-kvm', 'libvirt-daemon-system', 'bridge-utils',
                'virtinst']

    def __init__(self, *args):
        super().__init__(*args)

        # NOTE(lourot): on_install has already been registered by the parent
        # constructor.
        self.framework.observe(self.on.start, self.on_start)

    def on_install(self, event):
        super().on_install(event)  # installs PACKAGES

        # Installs series-dependent packages:
        ubuntu_series = lsb_release()['DISTRIB_CODENAME'].lower()
        if CompareHostReleases(ubuntu_series) < 'bionic':
            apt_install(['libvirt-bin'], fatal=True)
        else:
            apt_install(['libvirt-clients'], fatal=True)

    def on_start(self, event):
        self.__render_templates()
        self.__create_virtual_network()
        self.__create_virtual_machine()
        self.__expose_api()
        self.state.is_started = True

    __VIRTUAL_NETWORK_CONFIG_FILE = '/etc/arista/arista-virsh-network.xml'
    __CONFIG_CONTEXT = {
        'virtual_network_name': 'arista',
        'linux_bridge_name': 'virbr1',
    }

    def __render_templates(self):
        """Renders templates/* files."""
        config_dir = Path(os.path.dirname(self.__VIRTUAL_NETWORK_CONFIG_FILE))
        config_dir.mkdir(exist_ok=True, mode=0o755)

        template_name = os.path.basename(self.__VIRTUAL_NETWORK_CONFIG_FILE)
        target_path = str(config_dir / template_name)
        logger.info('Rendering {}'.format(target_path))
        ch_templating.render(template_name, target_path,
                             context=self.__CONFIG_CONTEXT, perms=0o644)

    def __create_virtual_network(self):
        """Creates a virsh network and an associated linux bridge."""
        logger.info("Creating a virtual network '{}' and a linux bridge '{}'"
                    .format(self.__CONFIG_CONTEXT['virtual_network_name'],
                            self.__CONFIG_CONTEXT['linux_bridge_name']))
        subprocess.check_call(['virsh', 'net-define',
                               self.__VIRTUAL_NETWORK_CONFIG_FILE])
        subprocess.check_call(['virsh', 'net-start',
                               self.__CONFIG_CONTEXT['virtual_network_name']])
        subprocess.check_call(['virsh', 'net-autostart',
                               self.__CONFIG_CONTEXT['virtual_network_name']])

    def __create_virtual_machine(self):
        """Creates the arista-cvx KVM instance."""
        vm_name = 'arista-cvx'
        logger.info('Launching the {} VM'.format(vm_name))
        arista_image_path = self.framework.model.resources.fetch(
            'arista-image')
        subprocess.check_call([
            'virt-install', '--name', vm_name, '--ram=1536', '--vcpus=1',
            '--boot', 'menu=on', '--disk',
            'path={},device=disk,bus=ide,size=10'.format(arista_image_path),
            '--graphics', 'none', '--network',
            'bridge:{},model=e1000'.format(
                self.__CONFIG_CONTEXT['linux_bridge_name']),
            '--autostart', '--noautoconsole', '--os-variant=generic'])

    def __expose_api(self):
        """Exposes Arista CVX's eAPI to the world."""
        ingress_address = str(self.model.get_binding('public').network
                              .ingress_address)
        ingress_port = '443'
        logger.info('Exposing {}:{}'.format(ingress_address, ingress_port))
        subprocess.check_call([
            'iptables', '-t', 'nat', '-A', 'PREROUTING', '-p', 'tcp',
            '-d', ingress_address, '--dport', ingress_port, '-j', 'DNAT',
            '--to-destination', '172.27.32.7'])
        subprocess.check_call([
            'iptables', '-D', 'FORWARD',
            '-o', self.__CONFIG_CONTEXT['linux_bridge_name'],
            '-j', 'REJECT', '--reject-with', 'icmp-port-unreachable'])


if __name__ == '__main__':
    main(CharmAristaVirtTestFixture)
