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
from ops.charm import CharmBase
from ops.main import main

logger = logging.getLogger(__name__)


class CharmAristaVirtTestFixture(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self.on_install)

    def on_install(self, event):
        logger.info("Congratulations, the charm was properly installed!")


if __name__ == '__main__':
    main(CharmAristaVirtTestFixture)
