# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 13:19:11 2022

@author: rubir
"""

from load_flow_FB import case_powerflow
import pandas as pd
import matplotlib.pyplot as plt


s="Sheet5"
Q_flex = pd.read_excel('optimal_Q.xlsx', s)         
def load_data_read(s,Q_flex):    
    active = pd.ExcelFile('Active_load.xls')
    reactive=pd.ExcelFile('ReActive_load.xls')
    df1 = pd.read_excel(active, s)
    df2 = pd.read_excel(reactive, s)
    active_load_year=df1.values.tolist()
    reactive_load_year =df2.values.tolist()    
    reactive_load_year[47]=Q_flex[1]
    reactive_load_year[77]=Q_flex[0]        
    return active_load_year, reactive_load_year

list_losses_year=[] 
voltage_years=[] 
active_load_year, reactive_load_year=load_data_read(s,Q_flex)   
list_vol ,list_losses_hourly   =case_powerflow(active_load_year,reactive_load_year,s)  
list_losses_year.append(list_losses_hourly)
df3=pd.DataFrame(list_losses_year)
df = pd.DataFrame (list_vol) #convert list of 24 hours and buses voltage into datafarme
voltage_years.append(df)  # store the dataframe of each years
Excelwriter = pd.ExcelWriter("FB_voltages.xlsx",engine="xlsxwriter")
# loop process the list of dataframes
for i, df in enumerate (voltage_years):
    df.to_excel(Excelwriter, sheet_name="Sheet" + str(i+1),index=False)
#And finally save the file
Excelwriter.save()    


V_OPF = pd.read_excel('optimal_v.xlsx', s)  
Voltage_years_tran= df.T
voltage_95_opf=(V_OPF.iloc[95])
voltage_95_fb=  Voltage_years_tran.iloc[95]

plt.plot(voltage_95_opf,label="Jabr_OPF")
plt.plot(voltage_95_fb, label='Forward/backward')
plt.legend() 
plt.ylabel("Voltages [pu]")
plt.xlabel("Time [Hours]")
