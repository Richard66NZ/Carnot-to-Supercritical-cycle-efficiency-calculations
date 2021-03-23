#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 14 December 2020 (update)

This source code is provided by Richard J Smith 'as is' and 'with all faults'. The provider makes no 
representations or warranties of any kind concerning the safety, suitability, inaccuracies, 
typographical errors, or other harmful components of this software.
"""

import matplotlib.pyplot as plt
import numpy as np
from pyXSteam.XSteam import XSteam

steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

print('Rankine superheat cycle analysis')

p1 = 0.1
s1 = steamTable.sL_p(p1)
T1 = steamTable.t_ps(p1, s1)
h1 = steamTable.hL_p(p1)
print('\nPoint 1')
print(f"p1: {round(float(p1),1)} bar")
print(f"T1: {round(float(T1),1)} degC")
print(f"H1: {round(float(h1),1)} kJ/kg")
print(f"S1: {round(float(s1),3)} kJ/kg K")

p2 = 180
s2 = s1

v = 1/steamTable.rhoL_p(p1)
w_p = v*(p2-p1)

print('\nPoint 2')
h2 = h1+w_p
print(f"H2: {round(float(h2),1)} kJ/kg")

T2 = steamTable.t_ph(p2, h2)
print(f"T2: {round(float(T2),1)} degC")

h2dash = steamTable.hL_p(p2)
s2dash = steamTable.sL_p(p2)
T2dash = steamTable.t_ph(p2, h2dash)
print('\nPoint 2 dash')
print(f"T2dash: {round(float(T2dash),1)} degC")
print(f"p2dash: {round(float(p2),1)} bar")
print(f"H2dash: {round(float(h2dash),1)} kJ/kg")
print(f"S2dash: {round(float(s2dash),3)} kJ/kg K")

h3dash = steamTable.hV_p(p2)
s3dash = steamTable.sV_p(p2)
T3dash = T2dash
print('\nPoint 3dash')
print(f"T3dash: {round(float(T3dash),1)} degC")
print(f"H3dash: {round(float(h3dash),1)} kJ/kg")
print(f"S3dash: {round(float(s3dash),3)} kJ/kg K")

p3 = p2
T3 = 540
h3 = steamTable.h_pt(p3, T3)
s3 = steamTable.s_pt(p3, T3)
print('\nPoint 3')
print(f"T3: {round(float(T3),1)} degC")
print(f"p3: {round(float(p3),1)} bar")
print(f"H3: {round(float(h3),1)} kJ/kg")
print(f"S3: {round(float(s3),3)} kJ/kg K")

p4 = p1
s4 = s3
T4 = steamTable.t_ps(p4, s4)
x4 = steamTable.x_ps(p4, s4)
h4 = steamTable.h_px(p4, x4)
print('\nPoint 4')
print(f"T4: {round(float(T4),1)} degC")
print(f"p4: {round(float(p4),1)} bar")
print(f"H4: {round(float(h4),1)} kJ/kg")
print(f"S4: {round(float(s4),3)} kJ/kg K")
print(f"x4: {round(float(x4*100),1)} % dry")

print('\nSummary')
print(f"Work required by pump: {round(float(w_p),1)} kJ/kg")

w_HPt = h3-h4
print(f"Work generated by turbine: {round(float(w_HPt),1)} kJ/kg")

q_H = (h3-h2)
print(f"Heat input by boiler: {round(float(q_H),1)} kJ/kg")

q_L = h4-h1
print(f"Heat rejected by the condenser: {round(float(q_L),1)} kJ/kg")

eta_th = (w_HPt-w_p)/q_H*100
print(f"Thermal efficiency is: {round(float(eta_th),1)}%")

HRcycle = 3600*100/eta_th
print(f"HR rankine cycle: {round(float(HRcycle),1)} kJ/kWh")

font = {'family' : 'Times New Roman',
        'size'   : 22}

plt.figure(figsize=(15,10))
plt.title('T-s Diagram - Rankine Superheat Cycle (Ideal)')
plt.rc('font', **font)

plt.ylabel('Temperature (C)')
plt.xlabel('Entropy (s)')
plt.xlim(-2,10)
plt.ylim(0,600)

T = np.linspace(0, 373.945, 400) # range of temperatures
# saturated vapor and liquid entropy lines
svap = [s for s in [steamTable.sL_t(t) for t in T]]
sliq = [s for s in [steamTable.sV_t(t) for t in T]]

plt.plot(svap, T, 'b-', linewidth=2.0)
plt.plot(sliq, T, 'r-', linewidth=2.0)

plt.plot([s1, s2, s2dash, s3dash, s3, s4, s1],[T1, T2, T2dash, T3dash, T3, T4, T1], 'black', linewidth=2.0)

plt.text(s1-.1,T1,f'(1)',
    ha='right',backgroundcolor='white')
plt.text(s1-.1,T1+30,f'(2)',
    ha='right',backgroundcolor='white')
plt.text(s2dash-.15,T2dash,f"(2')",
    ha='right',backgroundcolor='white')
plt.text(s3dash-.1,T3dash-25,f"(3')",
    ha='right',backgroundcolor='white')
plt.text(s3+.2,T3,f'(3)',
    ha='left',backgroundcolor='white')
plt.text(s4+.1,T4,f'(4)',
    ha='left',backgroundcolor='white')

plt.savefig('Plot-06.png')
