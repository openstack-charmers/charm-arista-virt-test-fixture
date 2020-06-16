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
from ops.main import main
import ops_openstack

logger = logging.getLogger(__name__)


class CharmAristaVirtTestFixture(ops_openstack.OSBaseCharm):

    PACKAGES = ['qemu-kvm', 'libvirt-clients', 'libvirt-daemon-system',
                'bridge-utils', 'virtinst']

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.start, self.on_start)

    def on_start(self, event):
        self.__render_templates()
        self.__create_virtual_network()
        self.state.is_started = True

    __VIRTUAL_NETWORK_CONFIG_FILE = '/etc/arista/arista-virsh-network.xml'
    __VIRTUAL_NETWORK_NAME = 'arista'

    def __render_templates(self):
        """Renders templates/* files."""
        config_dir = Path(os.path.dirname(self.__VIRTUAL_NETWORK_CONFIG_FILE))
        config_dir.mkdir(exist_ok=True, mode=0o755)

        template_name = os.path.basename(self.__VIRTUAL_NETWORK_CONFIG_FILE)
        context = {
            'virtual_network_name': self.__VIRTUAL_NETWORK_NAME
        }
        ch_templating.render(template_name, str(config_dir / template_name),
                             context, perms=0o644)

    def __create_virtual_network(self):
        """Creates a virsh network and an associated linux bridge."""
        subprocess.check_call(['virsh', 'net-define',
                               self.__VIRTUAL_NETWORK_CONFIG_FILE])
        subprocess.check_call(['virsh', 'net-start',
                               self.__VIRTUAL_NETWORK_NAME])
        subprocess.check_call(['virsh', 'net-autostart',
                               self.__VIRTUAL_NETWORK_NAME])


if __name__ == '__main__':
    main(CharmAristaVirtTestFixture)
