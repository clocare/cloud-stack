echo "generating inventory and cluster.yml files"
python3 script.py

echo "installing docker on instances"
ansible-playbook -u ubuntu -i inventory ansible-playbook.yml

echo "downloading rke if doesn't exist"
if ! [ -f rke ]; then
  curl -o rke -s -L https://github.com/rancher/rke/releases/download/v1.2.8/rke_linux-amd64
fi

echo "creating k8s cluster"
chmod +x rke
./rke up

echo "setting up kubeconfig file"
mkdir --parents ~/.kube
mv -f kube_config_cluster.yml ~/.kube/config

echo "cluster deployed successfully, now you can use kubectl command"