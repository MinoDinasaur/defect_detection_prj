source /home/admin/Desktop/dfdt/bin/activate
# sudo ip link set eth0 down
sudo ip addr add 192.168.1.1/24 dev eth0
sudo ip link set eth0 up
ip addr show dev eth0
python main.py
