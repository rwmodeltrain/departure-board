#! /bin/sh
sudo modprobe fbtft_device name=sainsmart18 rotate=270
sleep 3
con2fbmap 1 1
sleep 2
amixer set PCM -- 1000
sudo mount.cifs //192.168.1.61/Data /mnt/koploper -o username=username,password=password