
import math
import resistors


Vin = 12
VinMax = 12
VinMin = 12

Iout = 12

# lowest voltage where you can deliver the required power
Vinmin = 15
Vout = 1.2
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

#resList = [49900,7500]
resList = resistors.resitorList

def calcR1R2():
    VenLow = 1.14
    VenHigh = 1.26
    VenNom = 1.2
    IleakLow = -0.000001
    IleakHigh = 0.000001
    IleakNom = 0
    resTolerance = 0.01

    bestError = None

    for Res1 in resList:
        for Res2 in resList:
            VenableLow = calcVen(VenLow,Res1 * (1-resTolerance),Res2 * (1+resTolerance),IleakLow )
            VenableHigh = calcVen(VenHigh,Res1 * (1+resTolerance),Res2 * (1-resTolerance),IleakHigh )
            VenableNom = calcVen(VenNom,Res1,Res2,IleakNom)
            VenError = VenableLow - Vinmin

            if ( (bestError == None or VenError<bestError) and VenError>0):
                bestError = VenError
                bestList = (Res1,Res2,VenableLow,VenableNom,VenableHigh)

    print(f'BestList = {bestList}')
         

calcR1R2()


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