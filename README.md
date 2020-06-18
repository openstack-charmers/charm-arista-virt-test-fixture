# Arista test fixture

> **TODO**:
>
> * implement `arista-image-sha256sum` config option,
> * set up Travis CI to run `tox`.

This [Juju charm](https://juju.is/docs) installs KVM, runs an
[Arista CVX](https://www.arista.com/en/cg-cv/cv-deploying-cvx) virtual machine
on top of it and exposes its API (named eAPI). This allows you to easily
implement and validate software talking to Arista's eAPI, like
[this OpenStack Neutron plugin](https://github.com/openstack-charmers/charm-neutron-arista/tree/master/src).

It can be deployed on OpenStack. In other words it can run Arista CVX on KVM on
KVM.

This charm is implemented with the
[Operator framework](https://github.com/canonical/operator).

## Deploying

### From the store

```
$ juju deploy arista-virt-test-fixture                              \
      --resource arista-image=/path/to/arista-cvx-virt-test.qcow2   \
      --config arista-image-sha256sum=d19c70248ec44cf634496cce72051ca5ef2f8ef6dff04e0e6fca353476d3654e
$ juju status | grep ready
arista-virt-test-fixture/0*  active    idle   0        172.20.0.12            Unit is ready
$ curl --insecure --location --silent https://172.20.0.12 | grep "<title>"
   <title>Command API Explorer</title>
```

`arista-cvx-virt-test.qcow2` is based on Arista's
[official image](https://www.arista.com/en/cg-cv/cv-deploying-cvx) and is
expected to:

* configure the `interface management 1` with the IP address `172.27.32.7/23`,
* expose eAPI to `https/443`, and
* route all outgoing traffic to `172.27.32.1`.

### From source

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
```
