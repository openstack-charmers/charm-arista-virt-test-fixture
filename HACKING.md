# Arista test fixture

> **TODO**:
>
> * implement `arista-image-sha256sum` config option,
> * set up Travis CI to run `tox`.

## Deploying from source

```
$ tox -e build
$ juju deploy . --resource arista-image=/path/to/arista-cvx-virt-test.qcow2
```

## Publishing to the store

```
$ tox -e build
$ rm -rf .tox
$ charm login
$ touch /tmp/dummy-arista-image.qcow2
$ charm push . cs:~openstack-charmers-next/arista-virt-test-fixture \
    -r arista-image=/tmp/dummy-arista-image.qcow2
url: cs:~openstack-charmers-next/arista-virt-test-fixture-0
channel: unpublished
Uploaded "/tmp/dummy-arista-image.qcow2" as arista-image-0
$ charm release cs:~openstack-charmers-next/arista-virt-test-fixture-0 \
    --resource arista-image-0
url: cs:~openstack-charmers-next/arista-virt-test-fixture-0
channel: stable
warning: bugs-url and homepage are not set.  See set command.
$ charm set cs:~openstack-charmers-next/arista-virt-test-fixture \
    homepage=https://github.com/openstack-charmers/charm-arista-virt-test-fixture
$ charm set cs:~openstack-charmers-next/arista-virt-test-fixture \
    bugs-url=https://github.com/openstack-charmers/charm-arista-virt-test-fixture/issues
$ charm grant cs:~openstack-charmers-next/arista-virt-test-fixture-0 \
    --acl read everyone
```

The published charm can be found
[here](https://jaas.ai/u/openstack-charmers-next/arista-virt-test-fixture).
