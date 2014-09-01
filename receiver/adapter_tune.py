import linuxdvb
import fcntl
from datetime import datetime
import csv

fefd = open('/dev/dvb/adapter0/frontend0', 'r+')
dmfd = open('/dev/dvb/adapter0/demux0', 'r+')

# Tune
params = linuxdvb.dvb_frontend_parameters()
params.frequency = 634000000
params.inversion = linuxdvb.INVERSION_AUTO
params.u.ofdm.bandwidth = linuxdvb.BANDWIDTH_8_MHZ
params.u.ofdm.code_rate_HP = linuxdvb.FEC_AUTO
params.u.ofdm.code_rate_LP = linuxdvb.FEC_AUTO
params.u.ofdm.constellation = linuxdvb.QAM_AUTO
params.u.ofdm.transmission_mode = linuxdvb.TRANSMISSION_MODE_AUTO
params.u.ofdm.guard_interval = linuxdvb.GUARD_INTERVAL_AUTO
params.u.ofdm.hierarchy_information = linuxdvb.HIERARCHY_NONE
fcntl.ioctl(fefd, linuxdvb.FE_SET_FRONTEND, params)

# Pes stream
pesfilter = linuxdvb.dmx_pes_filter_params()
pesfilter.pid = 8101
pesfilter.input = linuxdvb.DMX_IN_FRONTEND
pesfilter.output = linuxdvb.DMX_OUT_TAP
pesfilter.pes_type = linuxdvb.DMX_PES_OTHER
pesfilter.flags = linuxdvb.DMX_IMMEDIATE_START
fcntl.ioctl(dmfd, linuxdvb.DMX_SET_PES_FILTER, pesfilter)

outfile = open('data.csv', 'wb')
csv = csv.writer(outfile)
csv.writerow(('Packet','Delay'))

static_part = "Valvoja paljonx viive? "
for i in range(0,1000):
    line = dmfd.readline()
    if len(line) != 44:
        continue
    if not line.startswith(static_part):
        continue
    strdate = line[(len(static_part)):]
    tx_date = datetime.fromtimestamp(float(strdate))
    rx_date = datetime.now()
    diff = rx_date - tx_date
    csv.writerow((i,diff.total_seconds()))

outfile.close()

# Close
fcntl.ioctl(dmfd, linuxdvb.DMX_STOP)
dmfd.close()
fefd.close()
