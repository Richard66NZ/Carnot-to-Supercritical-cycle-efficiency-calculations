#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 1 March 2021

This source code is provided by Richard J Smith 'as is' and 'with all faults'. The provider makes no 
representations or warranties of any kind concerning the safety, suitability, inaccuracies, 
typographical errors, or other harmful components of this software.
"""

import matplotlib.pyplot as plt
import numpy as np
from pyXSteam.XSteam import XSteam

steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

print('Rankine supercritical cycle (single reheat) analysis')

p1 = 0.1
s1 = steamTable.sL_p(p1)
T1 = steamTable.t_ps(p1, s1)
h1 = steamTable.hL_p(p1)
print('\nPoint 1')
print(f"P1: {round(float(p1),1)} bar")
print(f"T1: {round(float(T1),1)} degC")
print(f"H1: {round(float(h1),1)} kJ/kg")
print(f"S1: {round(float(s1),3)} kJ/kg K")

p2 = 350
s2 = s1

v = 1/steamTable.rhoL_p(p1)
w_p = v*(p2-p1)

print('\nPoint 2')
h2 = h1+w_p
print(f"H2: {round(float(h2),1)} kJ/kg")

T2 = steamTable.t_ph(p2, h2)
print(f"T2: {round(float(T2),1)} degC")

p3 = p2
T3 = 600
h3 = steamTable.h_pt(p3, T3)
s3 = steamTable.s_pt(p3, T3)
print('\nPoint 3')
print(f"T3: {round(float(T3),1)} degC")
print(f"P3: {round(float(p3),1)} bar")
print(f"H3: {round(float(h3),1)} kJ/kg")
print(f"S3: {round(float(s3),3)} kJ/kg K")

p4 = 80
print(f"Reheat Pressure: {round(float(p4),1)} bar")
s4 = s3
T4 = steamTable.t_ps(p4, s4)
h4 = steamTable.h_pt(p4, T4)
print('\nPoint 4')
print(f"T4: {round(float(T4),1)} degC")
print(f"P4: {round(float(p4),1)} bar")
print(f"H4: {round(float(h4),1)} kJ/kg")
print(f"S4: {round(float(s4),3)} kJ/kg K")

p5 = p4
T5 = T3 
h5 = steamTable.h_pt(p5, T5)
s5 = steamTable.s_pt(p5, T5)
print('\nPoint 5')
print(f"T5: {round(float(T5),1)} degC")
print(f"p5: {round(float(p5),1)} bar")
print(f"H5: {round(float(h5),1)} kJ/kg")
print(f"S5: {round(float(s5),3)} kJ/kg K")

p6 = p1
s6 = s5
T6 = steamTable.t_ps(p6, s6)
x6 = steamTable.x_ps(p6, s6)
h6 = steamTable.h_px(p6, x6)
print('\nPoint 6')
print(f"T6: {round(float(T6),1)} degC")
print(f"p6: {round(float(p6),1)} bar")
print(f"H6: {round(float(h6),1)} kJ/kg")
print(f"S6: {round(float(s6),3)} kJ/kg K")
print(f"x6: {round(float(x6*100),1)} % dry")

print('\nSummary')
print(f"Work required by pump: {round(float(w_p),1)} kJ/kg")

w_HPt = h3-h4
print(f"Work generated by HP turbine: {round(float(w_HPt),1)} kJ/kg")

w_LPt = h5-h6
print(f"Work generated by LP turbine: {round(float(w_LPt),1)} kJ/kg")
print(f"Total work output by turbine: {round(float(w_HPt+w_LPt),1)} kJ/kg")

q_H = (h3-h2)+(h5-h4)
print(f"Heat input by boiler: {round(float(q_H),1)} kJ/kg")

q_L = h6-h1
print(f"Heat rejected by the condenser: {round(float(q_L),1)} kJ/kg")

eta_th = (w_HPt+w_LPt-w_p)/q_H*100
print(f"Thermal efficiency is: {round(float(eta_th),1)}%")

HRcycle = 3600*100/eta_th
print(f"HR rankine cycle: {round(float(HRcycle),1)} kJ/kWh")

font = {'family' : 'Times New Roman',
        'size'   : 22}

plt.figure(figsize=(15,10))
plt.title('T-s Diagram - Rankine Supercrtical Cycle (Ideal) with single reheat')
plt.rc('font', **font)

plt.ylabel('Temperature (C)')
plt.xlabel('Entropy (s)')
plt.xlim(-2,10)
plt.ylim(0,700)

T = np.linspace(0, 373.945, 400) # range of temperatures
# saturated vapor and liquid entropy lines
svap = [s for s in [steamTable.sL_t(t) for t in T]]
sliq = [s for s in [steamTable.sV_t(t) for t in T]]

plt.plot(svap, T, 'b-', linewidth=2.0)
plt.plot(sliq, T, 'r-', linewidth=2.0)

superlistx = [s1, s2]
superlisty = [T1, T2]
for x in np.arange(s1, s3, 0.1):  
    Tx = steamTable.t_ps(p2, x)
    hxdash = steamTable.h_pt(p2, Tx)
    sxdash = steamTable.s_pt(p2, Tx)
    Txdash = steamTable.t_ps(p2, sxdash)
    superlistx.append(sxdash)
    superlisty.append(Txdash)    

hxdash = steamTable.h_pt(p2, T3)
sxdash = steamTable.s_pt(p2, T3)
Txdash = steamTable.t_ps(p2, sxdash)
superlistx.append(sxdash)
superlisty.append(Txdash)  

superlistx.extend([s3, s4, s5, s6, s1])
superlisty.extend([T3, T4, T5, T6, T1])  

plt.plot(superlistx, superlisty, 'black', linewidth=2.0)

plt.text(s1-.1,T1,f'(1)',
    ha='right',backgroundcolor='white')
plt.text(s1-.1,T1+30,f'(2)',
    ha='right',backgroundcolor='white')
plt.text(s3+.2,T3,f'(3)',
    ha='left',backgroundcolor='white')
plt.text(s4-.1,T4-25,f'(4)',
    ha='right',backgroundcolor='white')
plt.text(s5+.2,T5,f'(5)',
    ha='left',backgroundcolor='white')
plt.text(s6+.1,T6,f'(6)',
    ha='left',backgroundcolor='white')

plt.savefig('Plot-09.png')
