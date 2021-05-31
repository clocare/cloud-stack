variable "openstack_username"{
    description = "the openstack username"
    default = "admin"
}

variable "openstack_password"{
    description = "the openstack password"
    default = "password"
}

variable "openstack_project_name"{
    description = "the openstack project name"
    default = "admin"
}

variable "openstack_auth_url"{
    description = "the openstack auth_url"
    default = "http://controller:5000/v3"
}

variable "openstack_region"{
    description = "the openstack username"
    default = "RegionOne"
}

variable "cluster_name"{
    description = "the k8s cluster ame"
    default = "clokube"
}

variable "external_network_id"{
    description = "the openstack external_network_id"
    default = "f67f0d72-0ddf-11e4-9d95-e1f29f417e2f"
}

variable "public_key_path"{
    description = "the public_key_path"
    default = "~/.ssh/id_rsa.pub"
}

variable "controller_count"{
    description = "the k8s cluster controller nodes count"
    default = 1
}

variable "worker_count"{
    description = "the k8s cluster worker nodes count"
    default = 2
}

variable "flavor_id"{
    description = "the openstack flavor id for compute nodes"
    default = "f67f0d72-0ddf-11e4-9d95-e1f29f417e2f"
}

variable "image_id"{
    description = "the openstack image id for compute nodes"
    default = "f67f0d72-0ddf-11e4-9d95-e1f29f417e2f"
}

variable "floatingip_pool"{
    description = "the openstack floating ip pool"
    default = "pub-net"
}