# Arista test fixture

> **WARNING**: WIP

This [Juju charm](https://juju.is/docs) installs KVM, runs an
[Arista CVX](https://www.arista.com/en/cg-cv/cv-deploying-cvx) virtual machine
on top of it and exposes its API (named eAPI). This allows you to easily
implement and validate software talking to Arista's eAPI, like
[this OpenStack Neutron plugin](https://github.com/openstack-charmers/charm-neutron-arista/tree/master/src).

It can be deployed on OpenStack. In other words it can run Arista CVX on KVM on
KVM.

This charm is implemented with the
[Operator framework](https://github.com/canonical/operator).

## Deploy

### From the store

```
$ juju deploy arista-virt-test-fixture                              \
      --resource arista-image=/path/to/arista-cvx-virt-test.qcow2   \
      --config arista-image-sha256sum=d19c70248ec44cf634496cce72051ca5ef2f8ef6dff04e0e6fca353476d3654e
```

`arista-cvx-virt-test.qcow2` is based on Arista's
[official image](https://www.arista.com/en/cg-cv/cv-deploying-cvx) and is
expected to:

* configure the `interface management 1` with the IP address `172.27.32.7/23`,
* expose eAPI to `https/443`, and
* route all outgoing traffic to `172.27.32.1`.

### From source

```bash
$ tox -e build
$ juju deploy . --resource arista-image=/path/to/arista-cvx-virt-test.qcow2
```
