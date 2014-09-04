#!/bin/sh -eu
gcc --std=gnu99 -Wall always_on.c serial.c `pkg-config --libs --cflags glib-2.0`
