import numpy as np

print("Enter temperature (deg C): ")
T_C = float(input())

T = T_C+273.15
S = 35
# T =

pHT = (11911.08 - 18.2499*S - 0.039336*S**2)/T - 366.27059 + 0.53993607*S + 0.00016329*S**2 + (64.52243 - 0.084041*S)*np.log(T) - 0.11149858*T

print("Tris pH at {} is calculated as {}".format(T_C, pHT))

# T25 = 25+273.15
# T = 20+273.15
# S = 35
# # T =
#
# pHT25 = (11911.08 - 18.2499*S - 0.039336*S**2)/T25 - 366.27059 + 0.53993607*S + 0.00016329*S**2 + (64.52243 - 0.084041*S)*np.log(T25) - 0.11149858*T25
# pHT20 = (11911.08 - 18.2499*S - 0.039336*S**2)/T20 - 366.27059 + 0.53993607*S + 0.00016329*S**2 + (64.52243 - 0.084041*S)*np.log(T20) - 0.11149858*T20
#
# print(pHT20)
#
# deltapHdeltaT = (pHT25-pHT20)/(T25-T20)
#
# print(deltapHdeltaT)
