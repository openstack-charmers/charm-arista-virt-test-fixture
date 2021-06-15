# Arista test fixture

This [Juju charm](https://juju.is/docs) installs KVM, runs an [Arista CVX](https://www.arista.com/en/cg-cv/cv-deploying-cvx) virtual machine on top of it and exposes its API (named eAPI). This allows you to easily implement and validate software talking to Arista's eAPI, like [this OpenStack Neutron plugin](https://github.com/openstack-charmers/charm-neutron-arista/tree/master/src).

It can be deployed on OpenStack. In other words it can run Arista CVX on KVM on KVM.

This charm is implemented with the [Operator framework](https://github.com/canonical/operator).

## Deploying

```
$ juju deploy cs:~openstack-charmers-next/arista-virt-test-fixture  \
      --constraints mem=4G                                          \
      --resource arista-image=/path/to/arista-cvx-virt-test.qcow2
$ juju status | grep ready
arista-virt-test-fixture/0*  active    idle   0        172.20.0.12            Unit is ready
$ curl --insecure --location --silent https://172.20.0.12 | grep "<title>"
   <title>Command API Explorer</title>
```

`arista-cvx-virt-test.qcow2` is based on Arista's [official image](https://www.arista.com/en/cg-cv/cv-deploying-cvx) and is expected to:

* configure the `interface management 1` with the IP address `172.27.32.7/23`,
* expose eAPI to `https/443`, and
* route all outgoing traffic to `172.27.32.1`.
