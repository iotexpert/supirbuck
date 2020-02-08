
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



def calcVen(VR2,R1,R2,Ileak):
    IR1 = VR2/R2 + Ileak
    VR1 = IR1 * R1
    return(VR1+VR2)

resList = [49900,7500]
#resList = resistors.resitorList

def calcR1R2():
    VenLow = 1.14
    VenHigh = 1.26
    VenNom = 1.2
    IleakLow = -0.000001
    IleakHigh = 0.000001
    IleakNom = 0
    resTolerance = 0.01

    bestLow = 22.0
    bestList = []

    for Res1 in resList:
        for Res2 in resList:


            VenableLow = calcVen(VenLow,Res1 * (1-resTolerance),Res2 * (1+resTolerance),IleakLow )
            VenableHigh = calcVen(VenHigh,Res1 * (1+resTolerance),Res2 * (1-resTolerance),IleakHigh )
            VenableNom = calcVen(VenNom,Res1,Res2,IleakNom )

            print((Res1,Res2,VenableLow,VenableNom,VenableHigh))
#            if VenableLow < bestLow and VenableLow >= Vinmin:
            if VenableLow < bestLow :

                bestLow = VenableLow
                bestList = [(Res1,Res2,VenableLow,VenableNom,VenableHigh)]
            
#            if VenableLow == bestLow and VenableLow >= Vinmin:
            if VenableLow == bestLow :
                bestList = [(Res1,Res2,VenableLow,VenableNom,VenableHigh)]
            

    print(f'BestList = {bestList}')
         

'''
            if((VenableErrorBest == None and VenableError>0) or (VenableError >= 0 and VenableError <= VenableErrorBest)):
                print (f'VenableErrorBest = {VenableErrorBest}')
                best = (Res1,Res2,VenableNom,VenableError)
                VenableErrorBest = VenableError
                print(best)
            #print(f'R1 = {Res1} R2={Res2} VenableNom={VenableNom:.1f} VenableError={VenableError:.1f}')
#    print(best)
'''

'''
def calcR1R2(optimizeRes=True,optimizeVError=False):
    R1R2Ratio = (Vinmin - Ven) / Ven
    print(f'Ratio={R1R2Ratio}')
    possibleResistors = resistors.findResistorStack(R1R2Ratio)
    #print(possibleResistors)
    resErrorMin = None
    vErrorMin = None
   
    for resPair in possibleResistors:
        r1r2tolerance = 0.99
        R1 = resPair[0] / r1r2tolerance
        R2 = resPair[1] * r1r2tolerance
        IR2 = 1.2/R2
        IR1 = IR2 + 0.000001
        VR1 = IR1 * R1
        enable = VR1 + Ven

        vError = enable-Vinmin   
        resError = abs(resPair[0]+resPair[1] - 49900 - 7500)

        if vErrorMin is None:
            vErrorMin = vError

        if resErrorMin is None:
            resErrorMin = resError
        
        if resError <= resErrorMin and optimizeRes:
            resErrorMin = resError
            bestPair = resPair
            bestEnable = enable

        if vError <= vErrorMin and optimizeVError:
            vErrorMin = vError
            bestPair = resPair
            bestEnable = enable  

    print(f'R1={bestPair[0]} R2={bestPair[1]} Total={bestPair[1]+bestPair[0]} enable={bestEnable:.2f} ')

    return bestPair

R1R2 = calcR1R2(optimizeRes=False,optimizeVError=True)
'''

calcR1R2()

#print(R1R2)
    

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