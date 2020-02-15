
import math

import resistors
import inductors

# Input Power Supply
Vin = 20
VinMax = 21.0
VinMin = 19.0

# Load Requiresments
Vout = 5.0
Iout = 12



# This variable controls the under voltage lockout
# choose the lowest number where the power from the supply > output power 
# e.g power supply needs to be able to deliver  VenMin*I = Vout*Iout
VenMin = 0.7 * Vin

Ven = 1.2

#########################################################################################################
Cin=None
C1=None
C5=None
C6=None
Cref=None
C4=None
C2=None
Co=None
Cvcc=None
Lo=None
R3=None
R5=None
R7=None
R6=None
R8=None

R4=None
Rt=None
R1=None
Rpg=None
R2=None




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
        
        # From the datasheet the Oscillator will be with +-10%
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
#            D = Vout/Vin

    print(f'bestError = {bestError} Rt = {Rt} Fs={Fs}')
    return (Rt,Fs)


fVal = calcRt()
Rt = fVal[0]
Fs = fVal[1][2]*1000


#########################################################################################################
#
# Bootstrap Capacitor Selection
#
#########################################################################################################


C1 = 0.000001


#########################################################################################################
#
# Input Capacitor Selection
#
# C1
#
#########################################################################################################

D = Vout/Vin
Irms = Iout * (D * (1-D))**0.5

print(f'D={D:0.2f} Irms={Irms:0.2f}A')


#########################################################################################################
#
# Inductor Selection
#
#########################################################################################################


#Fs = 600000
deltai = 0.3 * Iout
Lo = (Vin-Vout) * Vout / (Vin * deltai * Fs) 
print(f'Fs = {Fs} Vin={Vin} Vout={Vout} deltai={deltai}')

print(f'Calc Lo={Lo*1e6:0.2f} uH')

Lo = inductors.chooseInductor(Lo)
print(f'Found Lo = {Lo[2]*1e6}uH')




#########################################################################################################
#
# Output Capacitor Selection
# Co C5
#
#########################################################################################################





#########################################################################################################
#
# Feedback Compensation
#
# R3, R4, R5, R6 
# C2, C3, C4
#########################################################################################################



#########################################################################################################
#
# Vref Bypass Capacitor
# Cref
#
#########################################################################################################


#########################################################################################################
#
# Print Results
# 
#
#########################################################################################################')
print('')
print('')
print('')
print('#########################################################################################################')

print(f'Cin={Cin}')
print(f'C1={C1}')
print(f'C5={C5}')
print(f'C6={C6}')
print(f'Cref={Cref}')
print(f'C4={C4}')
print(f'C2={C2}')
print(f'Co={Co}')
print(f'Cvcc={Cvcc}')
print(f'Lo={Lo}')
print(f'R3={R3}')
print(f'R5={R5}')
print(f'R7={R7}')
print(f'R6={R6}')
print(f'R8={R8}')
print(f'R4={R4}')
print(f'Rt={Rt}')
print(f'R1={R1}')
print(f'Rpg={Rpg}')
print(f'R2={R2}')


def milliAmps(current):
    return current/1000

def microAmps(current):
    return current/1e6

