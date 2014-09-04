/* -*- mode: c; c-file-style: "linux"; compile-command: "scons -C ../.." -*-
 *  vi: set shiftwidth=8 tabstop=8 noexpandtab:
 *
 *  Copyright 2014 Joel Lehtonen
 *  
 *  This program is free software: you can redistribute it and/or
 *  modify it under the terms of the GNU Affero General Public License
 *  as published by the Free Software Foundation, either version 3 of
 *  the License, or (at your option) any later version.
 *  
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *  
 *  You should have received a copy of the GNU Affero General Public
 *  License along with this program.  If not, see
 *  <http://www.gnu.org/licenses/>.
 */

#include <err.h>
#include <fcntl.h>
#include <glib.h>
#include <poll.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include "serial.h"

static gchar *serial_dev = NULL;
static gint serial_speed = 0;
static gboolean serial_drain = false;

static GOptionEntry entries[] =
{
  { "speed", 's', 0, G_OPTION_ARG_INT, &serial_speed, "Serial port baud rate (default: do not set)", "BAUD" },
  { "file", 'f', 0, G_OPTION_ARG_FILENAME, &serial_dev, "Write bitstream to FILE. Required.", "FILE" },
  { "drain", 'd', 0, G_OPTION_ARG_NONE, &serial_drain, "Drain serial port between PES packets", NULL },
  { NULL }
};

int main(int argc, char *argv[])
{
	GError *error = NULL;
	GOptionContext *context;
	
	context = g_option_context_new("- Serializes bitcoin blocks and transactions");
	g_option_context_add_main_entries(context, entries, NULL);
	if (!g_option_context_parse(context, &argc, &argv, &error))
	{
		g_print("option parsing failed: %s\n", error->message);
		exit(1);
	}

	if (serial_dev == NULL) {
		errx(1,"Option --file is mandatory. Try '%s --help'",argv[0]);
	}

	if (argc != 1) {
		errx(1,"Too many arguments on command line. Try '%s --help'",argv[0]);
	}

	// Prepare serial port
	int dev_fd = serial_open_raw(serial_dev, O_NOCTTY|O_WRONLY,
				     serial_speed);
	if (dev_fd == -1) {
		err(2,"Unable to open serial port %s",serial_dev);
	}

	//FILE *dev_file = fdopen(dev_fd, "wb");
	//if (dev_file == NULL) err(2,"File wrapping failed");
	int i=0;
	char buf[179];
	memset(buf,' ',sizeof(buf));

	// Process messages forever
	while (true) {
		i++;
		
		// Get time
		struct timespec now;
		if (clock_gettime(CLOCK_REALTIME, &now)) {
			err(10,"Unable to get time");
		}

		// Output the full string
		int n = snprintf(buf,178,"Kryptoradio delay test,%ld.%09ld,%d",now.tv_sec,now.tv_nsec,i);
		if (n < 0) {
			errx(2,"printf error");
		}
		buf[n]=',';
		buf[177]='\n';

		// Write it
		if (write(dev_fd,buf,178) != 178) {
			err(2,"write() error");
		}

		// Optionally drain
		if (serial_drain && tcdrain(dev_fd) != 0) {
			err(2,"Unable to drain");
		}
	}
	return 0; // Never reached
}
