
import math
import resistors


# Input Power Supply
Vin = 20.0
VinMax = 21.0
VinMin = 19.0

# Load Requiresments
Vout = 1.2
Iout = 12

# This variable controls the under voltage lockout
# choose the lowest number where the power from the supply > output power 
# e.g power supply needs to be able to deliver  VenMin*I = Vout*Iout
VenMin = 15

vripple = Vout * 0.01
fs = 600000
Vref = 0.5
Ven = 1.2

def milliAmps(current):
    return current/1000

def microAmps(current):
    return current/1e6



def calcVen(VR2,R1,R2,Ileak):
    IR1 = VR2/R2 + Ileak
    VR1 = IR1 * R1
    return(VR1+VR2)

def calcR1R2():
    # These parameter are from the IR3894 Datasheet
    VenLow = 1.14
    VenHigh = 1.26
    VenNom = 1.2
    IleakLow = -0.000001
    IleakHigh = 0.000001
    IleakNom = 0
    resTolerance = 0.01

    bestError = None

    for Res1 in resistors.resitorList:
        for Res2 in resistors.resitorList:
            VenActLow = calcVen(VenLow,Res1 * (1-resTolerance),Res2 * (1+resTolerance),IleakLow )
            VenActHigh = calcVen(VenHigh,Res1 * (1+resTolerance),Res2 * (1-resTolerance),IleakHigh )
            VenActNom = calcVen(VenNom,Res1,Res2,IleakNom)
            VenError = VenActLow - VenMin

            if ( (bestError == None or (VenError<bestError and VenActHigh<VinMin) ) and VenError>0):
                bestError = VenError
                bestList = (Res1,Res2,VenActLow,VenActNom,VenActHigh)
                R1 = Res1
                R2 = Res2
    return bestList
      
enableParams = calcR1R2()
print(f'R1={enableParams[0]}')
print(f'R2={enableParams[1]}')
print(f'VenLow = {enableParams[2]:.2f}')
print(f'VenNom = {enableParams[3]:.2f}')
print(f'VenHigh = {enableParams[4]:.2f}')




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