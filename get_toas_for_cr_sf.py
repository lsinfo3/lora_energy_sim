#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 14:26:13 2024

@author: Dr. Frank Loh
"""

try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

import numpy as np
import matplotlib.pyplot as plt

def calctoa(sf, coding_rate):
    #default LoRa setup for Europe
    payload_bytes = np.arange(1,52)
    cyclic_redundancy_check = 1
    header_enabled = 1
    header_length = 20
    preamble_length = 8
    bandwidth = 125000
    
    if sf < 11:
        low_datarate_optimize = 0
    else:
        low_datarate_optimize = 1
    
    #calculation of symbols per packet
    all_packet = (8 * payload_bytes - (4*sf) + 8 + 16 * cyclic_redundancy_check + header_length * header_enabled) / (4 * sf - 2*low_datarate_optimize)
    n_packet = 8 + (np.ceil(all_packet)* (coding_rate + 4))
    #with preamble and 4.25symbols for synchronization
    total_symbols = preamble_length + 4.25 + n_packet
    #get symbol duration
    symbol_duration = (2**sf)/bandwidth
    #get time on air
    toa_array = symbol_duration * total_symbols
    return toa_array, total_symbols

def calcplsymb(sf):
    payload_bytes = np.arange(1,52)
    coding_rate = 1
    if sf < 11:
        low_datarate_optimize = 0
    else:
        low_datarate_optimize = 1
    pl_symb_only = (8 * payload_bytes - (4*sf) + 8) / (4 * sf - 2*low_datarate_optimize)
    pl_symb_packet = 8 + (np.ceil(pl_symb_only) * (coding_rate + 4))
    return pl_symb_packet

#spreading factors in the range of 7 to 12
sf = np.arange(7,13)

#one time on air (toa) calculation for each spreading factor (sf) and coding
#rate (cr)
toa_cr1_sf7, symb_cr1_sf7 = calctoa(sf[0], coding_rate = 1)
toa_cr2_sf7, symb_cr2_sf7 = calctoa(sf[0], coding_rate = 2)
toa_cr3_sf7, symb_cr3_sf7 = calctoa(sf[0], coding_rate = 3)
toa_cr4_sf7, symb_cr4_sf7 = calctoa(sf[0], coding_rate = 4)
pl_symb_only_sf7 = calcplsymb(sf[0])

toa_cr1_sf8, symb_cr1_sf8 = calctoa(sf[1], coding_rate = 1)
toa_cr2_sf8, symb_cr2_sf8 = calctoa(sf[1], coding_rate = 2)
toa_cr3_sf8, symb_cr3_sf8 = calctoa(sf[1], coding_rate = 3)
toa_cr4_sf8, symb_cr4_sf8 = calctoa(sf[1], coding_rate = 4)
pl_symb_only_sf8 = calcplsymb(sf[1])

toa_cr1_sf9, symb_cr1_sf9 = calctoa(sf[2], coding_rate = 1)
toa_cr2_sf9, symb_cr2_sf9 = calctoa(sf[2], coding_rate = 2)
toa_cr3_sf9, symb_cr3_sf9 = calctoa(sf[2], coding_rate = 3)
toa_cr4_sf9, symb_cr4_sf9 = calctoa(sf[2], coding_rate = 4)
pl_symb_only_sf9 = calcplsymb(sf[2])

toa_cr1_sf10, symb_cr1_sf10 = calctoa(sf[3], coding_rate = 1)
toa_cr2_sf10, symb_cr2_sf10 = calctoa(sf[3], coding_rate = 2)
toa_cr3_sf10, symb_cr3_sf10 = calctoa(sf[3], coding_rate = 3)
toa_cr4_sf10, symb_cr4_sf10 = calctoa(sf[3], coding_rate = 4)
pl_symb_only_sf10 = calcplsymb(sf[3])

toa_cr1_sf11, symb_cr1_sf11 = calctoa(sf[4], coding_rate = 1)
toa_cr2_sf11, symb_cr2_sf11 = calctoa(sf[4], coding_rate = 2)
toa_cr3_sf11, symb_cr3_sf11 = calctoa(sf[4], coding_rate = 3)
toa_cr4_sf11, symb_cr4_sf11 = calctoa(sf[4], coding_rate = 4)
pl_symb_only_sf11 = calcplsymb(sf[4])

toa_cr1_sf12, symb_cr1_sf12 = calctoa(sf[5], coding_rate = 1)
toa_cr2_sf12, symb_cr2_sf12 = calctoa(sf[5], coding_rate = 2)
toa_cr3_sf12, symb_cr3_sf12 = calctoa(sf[5], coding_rate = 3)
toa_cr4_sf12, symb_cr4_sf12 = calctoa(sf[5], coding_rate = 4)
pl_symb_only_sf12 = calcplsymb(sf[5])

#time on air distribution among all coding rates for reference
total_toa_distrib_7 = np.concatenate((toa_cr1_sf7, 
                                      toa_cr2_sf7, 
                                      toa_cr3_sf7,
                                      toa_cr4_sf7), axis=0)

total_toa_distrib_8 = np.concatenate((toa_cr1_sf8, 
                                      toa_cr2_sf8, 
                                      toa_cr3_sf8,
                                      toa_cr4_sf8), axis=0)

total_toa_distrib_9 = np.concatenate((toa_cr1_sf9, 
                                      toa_cr2_sf9, 
                                      toa_cr3_sf9,
                                      toa_cr4_sf9), axis=0)

total_toa_distrib_10 = np.concatenate((toa_cr1_sf10, 
                                      toa_cr2_sf10, 
                                      toa_cr3_sf10,
                                      toa_cr4_sf10), axis=0)

total_toa_distrib_11 = np.concatenate((toa_cr1_sf11, 
                                      toa_cr2_sf11, 
                                      toa_cr3_sf11,
                                      toa_cr4_sf11), axis=0)

total_toa_distrib_12 = np.concatenate((toa_cr1_sf12, 
                                      toa_cr2_sf12, 
                                      toa_cr3_sf12,
                                      toa_cr4_sf12), axis=0)

total_toa_distrib_all = np.concatenate((total_toa_distrib_7, 
                                      total_toa_distrib_8, 
                                      total_toa_distrib_9,
                                      total_toa_distrib_10,
                                      total_toa_distrib_11,
                                      total_toa_distrib_12), axis=0)

plt.rcParams.update({'font.size': 14})
plt.rcParams.update({'axes.labelsize': 14})
plt.rcParams.update({'xtick.labelsize': 14})
plt.rcParams.update({'ytick.labelsize': 14})

#example plot for coding rate 2 and all spreading factors and payloads
#payload up to 51B is used as this is the limit for larger spreading factors
n = 3
colors = plt.cm.copper(np.linspace(0,1,n))

plt.figure(1, figsize=(5, 3))   
 
plt.plot(np.arange(1, 52), toa_cr2_sf7, color=colors[0], linewidth=2, label='SF7')
plt.plot(np.arange(1, 52), toa_cr2_sf8, color=colors[0], linestyle='dashed', linewidth=2, label='SF8')
plt.plot(np.arange(1, 52), toa_cr2_sf9, color=colors[1], linewidth=2, label='SF9')
plt.plot(np.arange(1, 52), toa_cr2_sf10, color=colors[1], linestyle='dashed', linewidth=2, label='SF10')
plt.plot(np.arange(1, 52), toa_cr2_sf11, color=colors[2], linewidth=2, label='SF11')
plt.plot(np.arange(1, 52), toa_cr2_sf12, color=colors[2], linestyle='dashed', linewidth=2, label='SF12')

plt.grid(which='major')
plt.ylabel('time on air [s]')
plt.xlabel('payload [B]')
plt.legend(loc='best', handletextpad=0.2, handlelength=0.8, ncol=2, borderpad=0.2, labelspacing = 0.1, borderaxespad = 0.2, columnspacing = 0.3)
plt.tight_layout()
plt.savefig('toa_distribution.pdf')

