
import math

import resistors


# Input Power Supply
Vin = 21.0
VinMax = 21.0
VinMin = 19.0

# Load Requiresments
Vout = 1.2
Iout = 12

# Oscilator Duty Cycle 
D = Vout/Vin

# This variable controls the under voltage lockout
# choose the lowest number where the power from the supply > output power 
# e.g power supply needs to be able to deliver  VenMin*I = Vout*Iout
VenMin = 15
Ven = 1.2


#########################################################################################################
#
# Enabling the IR3894
#
#########################################################################################################
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
    pwrSupplyMargin = 0.01

    bestError = None

    for Res1 in resistors.resitorList:
        for Res2 in resistors.resitorList:
            VenActLow = calcVen(VenLow,Res1 * (1-resistors.resTolerance),Res2 * (1+resistors.resTolerance),IleakLow )
            VenActHigh = calcVen(VenHigh,Res1 * (1+resistors.resTolerance),Res2 * (1-resistors.resTolerance),IleakHigh )
            VenActNom = calcVen(VenNom,Res1,Res2,IleakNom)
            VenError = VenActLow - (VenMin * (1+pwrSupplyMargin))

            if ( (bestError == None or (VenError<bestError and VenActHigh< (VinMin/(1+pwrSupplyMargin))    ) ) and VenError>0):
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


#########################################################################################################
#
# Programming the frequency
#
#########################################################################################################

#
#
#
#

def calcRt():

    #takes ohms ... return a tuple of low, nom, high khz
    def calcFreq(Rt):
        
        # from the datasheet
        oscAccuracy = .1

        RtNom = Rt/1000
        oscNom = 19954 * RtNom**(-0.953)

        RtFast = RtNom * (1-resistors.resTolerance)   
        oscFast = 19954 * RtFast**(-0.953)* (1+oscAccuracy)

        RtSlow = RtNom / (1-resistors.resTolerance)
        oscSlow = 19954 * RtSlow**(-0.953) /  (1+oscAccuracy)

        return (oscSlow,oscNom,oscFast)


    #test = calcFreq(80600)
    #print(f'Rt=80.6K Freq = {test}')

    # maximum frequency in kHz
    FsMax = Vout / (Vin * 60e-9 ) / 1000

    print(f'FsMax = {FsMax:.1f} kHz')

    bestError = None
    Rt = None

    for res in resistors.resitorList:
        FsCalc = calcFreq(res*(1-resistors.resTolerance))
        error = FsMax - FsCalc[2]
        if (bestError == None or error<bestError) and   error > 0 :
            bestError = error
            Rt = res
            Fs = FsCalc
            D=

    print(f'bestError = {bestError} Rt = {Rt} Fs={Fs}')


calcRt()

#########################################################################################################
#
# Programming the frequency
#
#########################################################################################################



def milliAmps(current):
    return current/1000

def microAmps(current):
    return current/1e6

