# K8S
Deploying a Kubernetes Cluster on Openstack
## Requirements
- [openstack](https://github.com/clocare/cloud)
- [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- ansible: `pip install ansible --upgrade`
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
#### hint: if you deployed your openstack cloud using [clocare/cloud](), these requirements are already satisfied

## Getting your Cluster up
1. clone this repo 
```
git clone https://github.com/clocare/k8s
```
2. run `terraform init`
3. change default values in [variables.tf](/variables.tf) file
4. deploy cluster infrastructure
```
terraform apply
```
5. wait for a couple of minutes until your instances are ready     
6. deploy your k8s cluster
```
./deploy-cluster.sh
```
## Destroying the cluster
just run `terraform destroy`