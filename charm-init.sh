#!/bin/bash

# FIXME: we should get rid of this script entirely as this is not the desired
# pattern anymore for the Operator Framework. We should make use of charmcraft
# instead. Example of another charm that has made this move already:
# https://github.com/openstack/charm-ceph-iscsi/commit/224b5df3

UPDATE=""
while getopts ":u" opt; do
  case $opt in
    u) UPDATE=true;;
  esac
done

git submodule update --init

# Disable pbr version calculation, see
# * https://stackoverflow.com/a/65670826/1855917
# * https://docs.openstack.org/pbr/latest/user/packagers.html#versioning
export PBR_VERSION=1.2.3

if [[ -z "$UPDATE" ]]; then
    pip3 install -t lib -r build-requirements.txt
else
    git -C mod/operator pull origin master

    # FIXME: the repository has moved to
    # https://opendev.org/openstack/charm-ops-openstack so pulling is now
    # pointless until that submodule gets fixed:
    # git -C mod/ops-openstack pull origin master

    git -C mod/charm-helpers pull origin master

    pip3 install -t lib -r build-requirements.txt --upgrade
fi

ln -f -t lib -s ../mod/operator/ops

# FIXME: this file has been renamed in newer versions of this dependency:
ln -f -t lib -s ../mod/ops-openstack/ops_openstack.py
