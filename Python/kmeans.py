import numpy as np
import math as math
import pandas as pd

#headers for csv data
HEADERS = ["ID", "Timestamp", "groupid",
            "Column 4", "Column 5", "sensor_x",
              "sensor_y", "sensor_z", "Column 9",
                "Column 10", "sensor_dir"]
mydata = pd.read_csv("data1.csv", sep=",", header=1, names=HEADERS)
#mytable numpy taulukko csv tiedoston datalle
mytable = np.ones((len(mydata), 3))

'''
sensor index locations to use with pandas
x = 5
y = 6
z = 7
dir = 10
'''

#lasketaan pisteiden etäisyys
def calclenght(centerpoint,datapoint):
    x = centerpoint[0] - datapoint[0]
    y = centerpoint[1] - datapoint[1]
    z = centerpoint[2] - datapoint[2]

    lenght = math.sqrt((x**2) + (y**2) + (z**2))

    #print ("length:",lenght)
    return lenght

def newcp(cumul, lkm):
    newcp = np.zeros((1,3))
    #print("newcp val/lkm: ",cumul, " ", lkm)
    #print("lkm: ",np.dtype(lkm))
    
    for i in range(3):
        newcp[0,i] = cumul[0,i] / lkm
    #print(newcp[0])
    return newcp

#selvitetään millä pisteellä on lyhin etäisyys
def lenghtcheck(cp0,datapoint):
    result0 = calclenght(cp0[0], datapoint)
    result1 = calclenght(cp0[1], datapoint)
    result2 = calclenght(cp0[2], datapoint)
    result3 = calclenght(cp0[3], datapoint)
    result4 = calclenght(cp0[4], datapoint)
    result5 = calclenght(cp0[5], datapoint)
    result_value = result0
    cpwin = 0
    #selvitetään lyhin pituus näistä tuloksista
    if result_value > result1:
        result_value = result1
        cpwin = 1
    if result_value > result2:
        result_value = result2
        cpwin = 2
    if result_value > result3:
        result_value = result3
        cpwin = 3
    if result_value > result4:
        result_value = result4
        cpwin = 4
    if result_value > result5:
        result_value = result5
        cpwin = 5
           
    return cpwin

#np.seterr(divide='ignore', invalid='ignore')
#haetaan csv taulukosta omaan numpy taulukkoon dataa
for i in range(len(mytable)):
    mytable[i,0] = mydata.iloc[i,5]
    mytable[i,1] = mydata.iloc[i,6]
    mytable[i,2] = mydata.iloc[i,7]



# määritellään arvottu keskipiste muuttuja, kumulatiivinen muuttuja ja lukumäärä 
# centerpoint
cp0 = np.ones((6,3))

cumul_cp0 = np.zeros((1,3))
cumul_cp1 = np.zeros((1,3))
cumul_cp2 = np.zeros((1,3))
cumul_cp3 = np.zeros((1,3))
cumul_cp4 = np.zeros((1,3))
cumul_cp5 = np.zeros((1,3))


#lukumäärää seuraavat arvot
lkm = np.zeros((1,6))


min_value = 10000
max_value = 0
# selvitetään minimi ja maksimi arvot datasta
for i in range(len(mytable)):
    for x in range(3):
        data_value = mytable[i,x]
        if data_value <= min_value:
            min_value = data_value
        if data_value >= max_value:
            max_value = data_value
print(min_value, " ",max_value)

# arvotaan satunnainen luku minimi ja maksimi arvojen väliltä
for y in range(0,6,1):
    for x in range(0,3,1):
        cp0[y,x] = np.random.randint(min_value, max_value)

print("rand cp: ",cp0)
#cp0[0,0] = max_value
#cp0[1,0] = min_value
#cp0[2,1] = max_value
#cp0[3,1] = min_value
#cp0[4,2] = max_value
#cp0[5,2] = min_value
#print(cp0)
#looppi koko datan läpi käymiseen
for i in range(1000):
    for x in range(len(mytable)-1):
        
# voittaja arvoon lisätään datapisteen arvo
        cpwin = lenghtcheck(cp0, mytable[x])
        #print(cpwin)
        if cpwin == 0:
            cumul_cp0[0,0] += mytable[x,0] 
            cumul_cp0[0,1] += mytable[x,1] 
            cumul_cp0[0,2] += mytable[x,2] 
            lkm[0,0] += 1
        if cpwin == 1:
            cumul_cp1[0,0] += mytable[x,0]
            cumul_cp1[0,1] += mytable[x,1]
            cumul_cp1[0,2] += mytable[x,2]
            lkm[0,1] += 1
        if cpwin == 2:
            cumul_cp2[0,0] += mytable[x,0]
            cumul_cp2[0,1] += mytable[x,1]
            cumul_cp2[0,2] += mytable[x,2]
            lkm[0,2] += 1
        if cpwin == 3:
            cumul_cp3[0,0] += mytable[x,0]
            cumul_cp3[0,1] += mytable[x,1]
            cumul_cp3[0,2] += mytable[x,2]
            lkm[0,3] += 1
        if cpwin == 4:
            cumul_cp4[0,0] += mytable[x,0]
            cumul_cp4[0,1] += mytable[x,1]
            cumul_cp4[0,2] += mytable[x,2]
            lkm[0,4] += 1
        if cpwin == 5:
            cumul_cp5[0,0] += mytable[x,0]
            cumul_cp5[0,1] += mytable[x,1]
            cumul_cp5[0,2] += mytable[x,2]
            lkm[0,5] += 1
            
    
    
    #jos joku piste ei saanut yhtään datapisteitä, arvotaan sille uusi keskipiste
    for n in range(6):
        if lkm[0,n] == 0:
            for x in range(0,3,1):
                cp0[n,x] = np.random.randint(min_value, max_value)
    #uusi keskipiste
    cp0[0] = newcp(cumul_cp0, lkm[0,0])
    cp0[1] = newcp(cumul_cp1, lkm[0,1])
    cp0[2] = newcp(cumul_cp2, lkm[0,2])
    cp0[3] = newcp(cumul_cp3, lkm[0,3])
    cp0[4] = newcp(cumul_cp4, lkm[0,4])
    cp0[5] = newcp(cumul_cp5, lkm[0,5])

    #jos joku piste ei saanut yhtään datapisteitä, arvotaan sille uusi keskipiste
    for n in range(6):
        if lkm[0,n] <= 20:
            for x in range(0,3,1):
                cp0[n,x] = np.random.randint(min_value, max_value)



#keskipisteiden järjestäminen
# otetaan jokaiselta cp0 sarake kaikki arvot, jotka järjestetään suuruusjärjestykseen
sorted_by_x = cp0[np.argsort(cp0[:, 0])[::-1]]
sorted_by_y = cp0[np.argsort(cp0[:, 1])[::-1]]
sorted_by_z = cp0[np.argsort(cp0[:, 2])[::-1]]

# lisätään uuteen arrayhin korkein ja pienin arvo haluttuun tapaan
# [-1] antaa käänteisessä järjestyksessä, eli pienin ensin
sorted_cp0 = np.array([
    sorted_by_x[0],  # highest x
    sorted_by_x[-1],  # lowest x
    sorted_by_y[0],  # highest y
    sorted_by_y[-1],  # lowest y
    sorted_by_z[0],  # highest z
    sorted_by_z[-1]   # lowest z
])


# lopullinen tallennus .h tiedostoon
# Convert the NumPy array to a C-style array string
result_str = "{\n" + ",\n".join("{" + ", ".join(map(str, row)) + "}" for row in sorted_cp0) + "\n}"

# Write the array to a .h file
with open('keskipisteet.h', 'w') as f:
    f.write("#ifndef KESKIPISTEET_H\n#define KESKIPISTEET_H\n\n")
    f.write(f"int CP[{sorted_cp0.shape[0]}][{sorted_cp0.shape[1]}] = {result_str};\n")
    f.write("\n#endif // KESKIPISTEET_H\n")

print("Header file 'keskipisteet.h' has been created.")
