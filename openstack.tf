# Define required providers
terraform {
required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.35.0"
    }
  }
}

# Configure the OpenStack Provider
provider "openstack" {
  user_name   = var.openstack_username
  tenant_name = var.openstack_project_name
  password    = var.openstack_password
  auth_url    = var.openstack_auth_url
  region      = var.openstack_region
}

resource "openstack_networking_router_v2" "k8s" {
  name                = "${var.cluster_name}-router"
  admin_state_up      = true
  external_network_id = var.external_network_id
}

resource "openstack_networking_network_v2" "k8s" {
  name           = "${var.cluster_name}-network"
  admin_state_up = "true"
}

resource "openstack_networking_subnet_v2" "k8s" {
  name            = "${var.cluster_name}-subnet"
  network_id      = openstack_networking_network_v2.k8s.id
  cidr            = "192.168.1.1/24"
  ip_version      = 4
  dns_nameservers = ["8.8.8.8", "8.8.4.4"]
}

resource "openstack_networking_router_interface_v2" "k8s" {
  router_id = openstack_networking_router_v2.k8s.id
  subnet_id = openstack_networking_subnet_v2.k8s.id
}

resource "openstack_compute_keypair_v2" "k8s" {
  name       = "${var.cluster_name}-keypairs"
  public_key = chomp(file(var.public_key_path))
}

resource "openstack_networking_secgroup_v2" "k8s" {
  name                 = "${var.cluster_name}-k8s"
  delete_default_rules = true
}

resource "openstack_networking_secgroup_rule_v2" "k8s_ingress" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = -1
  port_range_min    = "20"
  port_range_max    = "33000"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.k8s.id
}

resource "openstack_networking_secgroup_rule_v2" "k8s_egress" {
  direction         = "egress"
  ethertype         = "IPv4"
  protocol          = -1
  port_range_min    = "1"
  port_range_max    = "65535"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.k8s.id
}

resource "openstack_compute_instance_v2" "k8s-controller" {
  count           = var.controller_count
  name            = "${var.cluster_name}-k8s-controller"
  flavor_id       = var.flavor_id
  key_pair        = openstack_compute_keypair_v2.k8s.name
  security_groups = [openstack_networking_secgroup_v2.k8s.name]

  block_device {
    uuid                  = var.image_id
    source_type           = "image"
    volume_size           = 2
    boot_index            = 0
    destination_type      = "volume"
    delete_on_termination = true
  }

  network {
    name = openstack_networking_network_v2.k8s.name
  }
}

resource "openstack_compute_instance_v2" "k8s-worker" {
  count           = var.worker_count
  name            = "${var.cluster_name}-k8s-worker"
  flavor_id       = var.flavor_id
  key_pair        = openstack_compute_keypair_v2.k8s.name
  security_groups = [openstack_networking_secgroup_v2.k8s.name]

  block_device {
    uuid                  = var.image_id
    source_type           = "image"
    volume_size           = 2
    boot_index            = 0
    destination_type      = "volume"
    delete_on_termination = true
  }

  network {
    name = openstack_networking_network_v2.k8s.name
  }
}

resource "openstack_compute_floatingip_v2" "k8s_controller" {
  count = var.controller_count
  pool  = var.floatingip_pool
}

resource "openstack_compute_floatingip_v2" "k8s_worker" {
  count = var.worker_count
  pool  = var.floatingip_pool
}

resource "openstack_compute_floatingip_associate_v2" "k8s_controller" {
  count       = var.controller_count
  floating_ip = openstack_compute_floatingip_v2.k8s_controller[count.index].address
  instance_id = openstack_compute_instance_v2.k8s_controller[count.index].id
}

resource "openstack_compute_floatingip_associate_v2" "k8s_worker" {
  count       = var.worker_count
  floating_ip = openstack_compute_floatingip_v2.k8s_worker[count.index].address
  instance_id = openstack_compute_instance_v2.k8s_worker[count.index].id
}

output "controller_public_ips" {
  value = openstack_networking_floatingip_v2.k8s_controller[*].address
}

output "worker_public_ips" {
  value = openstack_networking_floatingip_v2.k8s_worker[*].address
}

output "controller_local_ips" {
  value = openstack_compute_instance_v2.k8s_controller[*].access_ip_v4
}

output "worker_local_ips" {
  value = openstack_compute_instance_v2.k8s_worker[*].access_ip_v4
}