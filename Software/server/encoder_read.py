#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import pigpio
import sys

A = 15
B = 7

flg = 2

pi = pigpio.pi()
pi.set_mode(A,pigpio.INPUT)
pi.set_mode(B,pigpio.INPUT)

pi.set_pull_up_down(A,pigpio.PUD_UP)    #A相側のピンに内部プルアップを有効化
pi.set_pull_up_down(B,pigpio.PUD_UP)    #B相側のピンに内部プルアップを有効化

def cb_interrupt():
    global rotate
    if pi.read(B) == 1: #B相がLOW
        if flg == 1:    #かつ前回のB相がLOWなら
            rotate += 1 #回転数+1

        flg = 1         #B相がLOWなので現状右回転

    else:   #B相がHIGH
        if flg == 0:        #かつ前回のB相もHIGHなら
            rotate -= 1     #回転数-1

        flg = 0         #B相がHIGHなので現状左回転

    sys.stdout.write("\r{}".format(rotate))  #回転数を出力
    sys.stdout.flush()

cb = pi.callback(A,pigpio.FALLING_EDGE,cb_interrupt)