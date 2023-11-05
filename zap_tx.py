#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: ZAP
# Author: Josh Rabinowitz
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from enum import Enum
import osmosdr
import time

class ZapCommand(Enum):
    ON_1 = 1
    OFF_1 = 2
    ON_2 = 3
    OFF_2 = 4
    ON_ALL = 5
    OFF_ALL = 6

class ZapTX(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "ZapTX")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 8e6
        self.freq = freq = 433.92e6
        self.baud = baud = 1/(171e-6)
        #self.baud = baud = 5847
        self.sps = sps = 1368 #int(samp_rate/baud)
        self.data = []

        self.GAP = GAP = "0"*31
        self.STOP = STOP = "1000100010001000100010001000111010001110100011101000111010001110100010001000100010001000100010001"

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(60, 0)
        self.osmosdr_sink_0.set_if_gain(50, 0)
        self.osmosdr_sink_0.set_bb_gain(30, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(self.data, True, 1, [])
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, sps)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_repeat_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))

    def set_cmd(self, cmd):
        self.data = []

        if cmd == ZapCommand.ON_1:
            CMD = "1000100010001000100010001000111010001110100011101000111010001110100010001110111010001000111011101"
        elif cmd == ZapCommand.OFF_1:
            CMD = "1000100010001000100010001000111010001110100011101000111010001110100010001110111011101110100010001"
        elif cmd == ZapCommand.ON_2:
            CMD = "1000100010001000100010001000111010001110100011101000111010001110111011101000100010001000111011101"
        elif cmd == ZapCommand.OFF_2:
            CMD = "1000100010001000100010001000111010001110100011101000111010001110111011101000100011101110100010001"
        elif cmd == ZapCommand.ON_ALL:
            CMD = "1000100010001000100010001000111010001110111011101000111010001110100010001000100010001000111011101"
        elif cmd == ZapCommand.OFF_ALL:
            CMD = "1000100010001000100010001000111010001110111011101000111010001110100010001000100011101110100010001"
        # Pairing not implemented as need continuous transmission until release
        else:
            assert 0
        self.data += (self._bin2arr(CMD)+self._bin2arr(self.GAP))*10
        self.data += self._bin2arr(self.STOP)
        # Command MUST be padded. Sink requires certain amount of samples before xmit
        #self.data += [0]*4096

    def set_addr(self, addr):
        self.addr = self._bin2arr(addr)

    def _mkcmd(self, cmd):
        return self._bin2arr(cmd) + self._bin2arr(self.COMMAND_GAP)

    def _bin2arr(self, s):
        return [int(b) for b in s]

    #def _encode(self, data):
    #    out_data = []
    #    for d in data:
    #        d = int(d)
    #        if d == 0:
    #            out_data += [0]
    #        else:
    #            out_data += [1]
    #    return out_data

    def restart(self):
        self.samp_rate = samp_rate = 8e6
        self.freq = freq = 433.92e6
        self.baud = baud = 5847
        # Disconnect and reconnect the vector source to start the flowgraph over
        self.lock()
        self.disconnect((self.blocks_repeat_0, 0), (self.osmosdr_sink_0, 0))
        self.disconnect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))

        self.blocks_vector_source_x_0 = blocks.vector_source_c(self.data, False, 1, [])
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, int(samp_rate/baud))

        self.connect((self.blocks_repeat_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.unlock()

    #def get_sps(self):
    #    return self.sps

    #def set_sps(self, sps):
    #    self.sps = sps
    #    self.blocks_repeat_0.set_interpolation(self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.sps = int(samp_rate/baud)
        self.blocks_repeat_0.set_interpolation(self.sps)
