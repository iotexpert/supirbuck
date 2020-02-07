
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


def calcR1R2():
    R1R2Ratio = (Vinmin - Ven) / Ven
    print(f'Ratio={R1R2Ratio}')
    possibleResistors = resistors.findResistorStack(R1R2Ratio)
    #print(possibleResistors)
    errorMin = 1e9

    for resPair in possibleResistors:
        r1r2tolerance = 1
        R1 = resPair[0] / r1r2tolerance
        R2 = resPair[1] * r1r2tolerance
        IR2 = 1.2/R2
        IR1 = IR2 + 0.000001
        VR1 = IR1 * R1
        enable = VR1 + Ven
        #error = (1 - (enable/Vinmin)) * 100
        error = abs(resPair[0]+resPair[1] - 49900 - 7500)

        if error < errorMin:
            errorMin = error
            bestPair = resPair
            bestEnable = enable
    
    print(f'R1={bestPair[0]} R2={bestPair[1]} Total={bestPair[1]+bestPair[0]} enable={bestEnable:.2f} ')

    return bestPair

R1R2 = calcR1R2()
print(R1R2)
    

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