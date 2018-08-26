#!/usr/bin/env sh

gcc -Wall -pthread -o controll controll.c -lpigpiod_if2 -lrt
