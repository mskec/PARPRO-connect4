# Setup environment
cd ~ &&
apt-get update &&
apt-get install -y python-dev &&
apt-get install -y python-pip &&
apt-get install -y git &&

apt-get install -y mpich2 &&
pip install mpi4py &&

cat /dev/zero | ssh-keygen -q -t rsa -N "" &&
cat .ssh/id_rsa.pub