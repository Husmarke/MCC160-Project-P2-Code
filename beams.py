#cantilever, end load

#diamond propeties:
E = 1.05*10**12 # youngs modulus
d = 3500 # density [kg/m^3]
DSMax = 2800 * 10**6 # maximal stress without fracturing [Pascal]

#beam dimensions
L = 0.00724 # length [m]
b = 0.02000 # bredth [m]
h = 0.00300 # hight [m]

I = (b*h**3)/12 # inertia
print(I)

#----------------------------------------------------
# optimising F from maximum amount of stress
# link https://www.engineeringtoolbox.com/cantilever-beams-d_1848.html
step = 0.001
F = 0
while True:
    SMax = h*F*(L/I)
    if SMax < DSMax:
        F +=step
    else:
        break
F -=step
SMax = h*F*L/I
print("diamond (maximum stress > calculated stress)")
print(DSMax,"Pascal", ">", round(SMax,6),"Pascal")
print("the maximal stress is",round(SMax,6),"Pascal\nwith F=",round(F,5),"N")

#-----------------------------------------
# calculating maximal deflection of beam
# link https://mechanicalc.com/reference/beam-analysis
DMax = (F*L**3)/(3*E*I) # formel för att räkna ut deflektionen av "end loaded cantilever"
amp = DMax
print(DMax,"m")

#----------------------------------
# Setup variables for wave/impedance calculations
fHz = 160*10^3 # theoretical frequency of vibration [Hz]

dAir = 0.001204 # density of air [g/cm^3]
dMuscle = 1.065 # --  || -- Muscle [g/cm^3]
dBone = 1.9 # --  || -- Bone [g/cm^3]
dFat = 0.95 # --  || -- Fat [g/cm^3]
dSkin = 1.15 # --  || -- Skin [g/cm^3]

vAir = 343 # speed of sound thrugh the medium air [m/s]
vMuscle = 1590 # -- || -- muscle (across fibres) [m/s]
vBone = 4080 # -- || -- bone [m/s]
vFat = 1450 # -- || -- fat [m/s]
vSkin = 1730 # -- || -- skin [m/s]

impMuscle = 1.69*10**6 # acustic impedance of tissue [kg/(sec*m^2)]
impBone = 7.75*10**6 # -- || --
impFat = 1.38*10**6 # -- || --
impSkin = 1.99*10**6 # -- || -- 

#--------------------------------------------
# power of ultrasound [Watts/cm^2]
# link https://www.echopedia.org/wiki/The_principle_of_ultrasound
beamA = 1 # beam area [cm^2]
power = amp**2/beamA
print("power:", power,"W/cm^2")

#----------------------------------
# wavelength
# link https://www.omnicalculator.com/physics/sound-wavelength
wLenAir = vAir/fHz
wLenMuscle = vMuscle/fHz
wLenBone = vBone/fHz
wLenFat = vFat/fHz
wLenSkin = vSkin/fHz
print(f"The Wavelength based on medium:\nAir: {wLenAir} m/s\nMuscle: {wLenMuscle} m/s\nBone: {wLenBone} m/s\nFat: {wLenFat} m/s\nSkin: {wLenSkin} m/s")

#-----------------------------------
# specific acoustic impedance [MRayl]
# link https://www.omnicalculator.com/physics/acoustic-impedance
zAir = dAir*vAir
zMuscle = dMuscle*vMuscle
zBone=dBone*vBone
zFat=dFat*vFat
zSkin=dSkin*vSkin
print(f"The specific acoustic impedance based on medium:\nAir: {zAir} MRayl\nMuscle: {zMuscle} MRayl\nBone: {zBone} MRayl\nFat: {zFat} MRayl\nSkin: {zSkin} MRayl")

#--------------------------------------
# reflection and transmission between materials
# link https://www.omnicalculator.com/physics/acoustic-impedance
def R_T(z1,z2):
    R = (z1-z2)**2/(z1+z2)**2
    T = (4*z1*z2)/(z1+z2)**2
    return R,T

print(f"Air => Skin: Reflected: {R_T(zAir,zSkin)[0]*100}%, Transmitted: {R_T(zAir,zSkin)[1]*100}%")
print(f"Skin => Muscle: Reflected: {R_T(zSkin,zMuscle)[0]*100}%, Transmitted: {R_T(zSkin,zMuscle)[1]*100}%")
print(f"Skin => Fat: Reflected: {R_T(zSkin,zFat)[0]*100}%, Transmitted: {R_T(zSkin,zFat)[1]*100}%")
print(f"Muscle => Bone: Reflected: {R_T(zMuscle,zBone)[0]*100}%, Transmitted: {R_T(zMuscle,zBone)[1]*100}%")