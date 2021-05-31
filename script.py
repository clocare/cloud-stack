import yaml,json,subprocess

command = subprocess.run('terraform output -json controller_local_ips', capture_output=True,shell=True)
controller_local_ips=json.loads(command.stdout)

command = subprocess.run('terraform output -json controller_public_ips', capture_output=True,shell=True)
controller_public_ips=json.loads(command.stdout)

command = subprocess.run('terraform output -json worker_local_ips', capture_output=True,shell=True)
worker_local_ips=json.loads(command.stdout)

command = subprocess.run('terraform output -json worker_public_ips', capture_output=True,shell=True)
worker_public_ips=json.loads(command.stdout)

cluster = yaml.load('''
services:
  etcd:
    image: ""
    ca_cert: ""
    cert: ""
    key: ""
    path: ""
    uid: 0
    gid: 0
    retention: ""
    creation: ""
  kube-api:
    image: ""
    service_cluster_ip_range: 10.43.0.0/16
    service_node_port_range: ""
    pod_security_policy: false
    always_pull_images: false
  kube-controller:
    image: ""
    cluster_cidr: 10.42.0.0/16
    service_cluster_ip_range: 10.43.0.0/16
  scheduler:
    image: ""
  kubelet:
    image: ""
    cluster_domain: cluster.local
    infra_container_image: ""
    cluster_dns_server: 10.43.0.10
    fail_swap_on: false
    generate_serving_certificate: false
  kubeproxy:
    image: ""
network:
  plugin: calico
  mtu: 0
authentication:
  strategy: x509
  sans: []
  webhook: null
addons: ""
addons_include: []
system_images:
  etcd: rancher/mirrored-coreos-etcd:v3.4.15-rancher1
  alpine: rancher/rke-tools:v0.1.74
  nginx_proxy: rancher/rke-tools:v0.1.74
  cert_downloader: rancher/rke-tools:v0.1.74
  kubernetes_services_sidecar: rancher/rke-tools:v0.1.74
  kubedns: rancher/mirrored-k8s-dns-kube-dns:1.15.10
  dnsmasq: rancher/mirrored-k8s-dns-dnsmasq-nanny:1.15.10
  kubedns_sidecar: rancher/mirrored-k8s-dns-sidecar:1.15.10
  kubedns_autoscaler: rancher/mirrored-cluster-proportional-autoscaler:1.8.1
  coredns: rancher/mirrored-coredns-coredns:1.8.0
  coredns_autoscaler: rancher/mirrored-cluster-proportional-autoscaler:1.8.1
  nodelocal: rancher/mirrored-k8s-dns-node-cache:1.15.13
  kubernetes: rancher/hyperkube:v1.20.6-rancher1
  flannel: rancher/coreos-flannel:v0.13.0-rancher1
  flannel_cni: rancher/flannel-cni:v0.3.0-rancher6
  calico_node: rancher/mirrored-calico-node:v3.17.2
  calico_cni: rancher/mirrored-calico-cni:v3.17.2
  calico_controllers: rancher/mirrored-calico-kube-controllers:v3.17.2
  calico_ctl: rancher/mirrored-calico-ctl:v3.17.2
  calico_flexvol: rancher/mirrored-calico-pod2daemon-flexvol:v3.17.2
  canal_node: rancher/mirrored-calico-node:v3.17.2
  canal_cni: rancher/mirrored-calico-cni:v3.17.2
  canal_controllers: rancher/mirrored-calico-kube-controllers:v3.17.2
  canal_flannel: rancher/coreos-flannel:v0.13.0-rancher1
  canal_flexvol: rancher/mirrored-calico-pod2daemon-flexvol:v3.17.2
  weave_node: weaveworks/weave-kube:2.8.1
  weave_cni: weaveworks/weave-npc:2.8.1
  pod_infra_container: rancher/mirrored-pause:3.2
  ingress: rancher/nginx-ingress-controller:nginx-0.43.0-rancher3
  ingress_backend: rancher/mirrored-nginx-ingress-controller-defaultbackend:1.5-rancher1
  metrics_server: rancher/mirrored-metrics-server:v0.4.1
  windows_pod_infra_container: rancher/kubelet-pause:v0.1.6
  aci_cni_deploy_container: noiro/cnideploy:5.1.1.0.1ae238a
  aci_host_container: noiro/aci-containers-host:5.1.1.0.1ae238a
  aci_opflex_container: noiro/opflex:5.1.1.0.1ae238a
  aci_mcast_container: noiro/opflex:5.1.1.0.1ae238a
  aci_ovs_container: noiro/openvswitch:5.1.1.0.1ae238a
  aci_controller_container: noiro/aci-containers-controller:5.1.1.0.1ae238a
  aci_gbp_server_container: noiro/gbp-server:5.1.1.0.1ae238a
  aci_opflex_server_container: noiro/opflex-server:5.1.1.0.1ae238a
ssh_key_path: ~/.ssh/id_rsa
ssh_cert_path: ""
ssh_agent_auth: false
authorization:
  mode: rbac
  options: {}
kubernetes_version: ""
ingress:
  provider: ""
  options: {}
  http_port: 0
  https_port: 0
  network_mode: ""
  tolerations: []
  default_http_backend_priority_class_name: ""
  nginx_ingress_controller_priority_class_name: ""
cluster_name: ""
cloud_provider:
  name: ""
prefix_path: ""
win_prefix_path: ""
addon_job_timeout: 0
bastion_host:
  address: ""
  port: ""
  user: ""
  ssh_key: ""
  ssh_key_path: ""
  ssh_cert: ""
  ssh_cert_path: ""
monitoring:
  provider: ""
  metrics_server_priority_class_name: ""
restore:
  restore: false
  snapshot_name: ""
rotate_encryption_key: false
dns: null''', Loader=yaml.FullLoader)

cluster['nodes'] = []

node = yaml.load('''
- port: "22"
  hostname_override: ""
  user: ubuntu
  docker_socket: /var/run/docker.sock
  ssh_key: ""
  ssh_key_path: ~/.ssh/id_rsa
  ssh_cert: ""
  ssh_cert_path: ""
''', Loader=yaml.FullLoader)

for i in range(len(controller_local_ips)):
    controller_node=node[0].copy()
    controller_node['role']=["etcd", "controlplane"]
    controller_node['address']=controller_public_ips[i]
    controller_node['internal_address']=controller_local_ips[i]
    cluster['nodes'].append(controller_node)

for i in range(len(worker_local_ips)):
    worker_node=node[0].copy()
    worker_node['role']=['worker']
    worker_node['address']=worker_public_ips[i]
    worker_node['internal_address']=worker_local_ips[i]
    cluster['nodes'].append(worker_node)

with open('cluster.yml', 'w+') as file:
    file.write(yaml.dump(cluster))

print('created cluster.yml file')

inventory='[controller]'

for ip in controller_public_ips:
    inventory+='\n{}'.format(ip)

inventory+='\n[worker]'

for ip in worker_public_ips:
    inventory+='\n{}'.format(ip)

inventory+='''
[all:children]
worker
controller
'''
with open('inventory', 'w+') as file:
    file.write(inventory)
    
print('created cluster.yml file')