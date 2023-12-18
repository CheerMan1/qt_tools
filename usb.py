# -*- coding: utf-8 -*-
import usb

# find our device
dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)

print(dev)
