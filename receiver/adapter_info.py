import linuxdvb
import fcntl

fefd = open('/dev/dvb/adapter0/frontend0', 'r+')

# Information
feinfo = linuxdvb.dvb_frontend_info()
fcntl.ioctl(fefd, linuxdvb.FE_GET_INFO, feinfo)
print feinfo.name
for bit, flag in linuxdvb.fe_caps.items():
    if (feinfo.caps & bit) > 0:
        print("cap = "+flag)

# Close
fefd.close()
