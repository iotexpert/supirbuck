
import math
import resistors


Vin = 12
Vinmin = 9.2
Vout = 1.2
Iout = 12
vripple = Vout * 0.01
fs = 600000
Vref = 0.5
Ven = 1.2

def milliAmps(current):
    return current/1000

def microAmps(current):
    return current/1e6

resList = resistors.findResistorStack(.262)
#print( resList)
#print(resistors.lowestResistance(resList))
#print(resistors.largestResistance(resList))



#print(resistors.chooseResistor(49899))

def calcR1R2():
    R2R1Ratio = Ven/(Vinmin - Ven)
    possibleResistors = resistors.findResistorStack(R2R1Ratio)
    return possibleResistors

R1R2List = calcR1R2()

for i in R1R2List:
    enable = 9.2 / (i[0]+i[1]) * i[0]
    print(f'R1={i[0]} R2={i[1]} Total={i[0]+i[1]} enable={enable}')
    

#print(R1R2List)

# R1 = 49900
# Vencalc = Vinmin * R2 * (R1 + R2)
#print(f'R1 = {R1}')
#print(f'R2 = {R2}')
#print(f'VenCalc = {Vencalc}')






'''
phase_boost = 70

FZ2 = Fo*math.sqrt((1-math.sin(phase_boost)/(1+sin(phase_boost))))


FZ1 = 0.5*FZ2
FP3 = 0.5*Fs

c4 = 2.2nf

r4 = (1/2*math.pi*c4*fp2)
r5 = 1/(2*math.pi*c4*fz2)
r6 = Vref / (Vout - Vref)
'''