import json
import datetime

def parse_powermeter_data(rsPayload):
    # Find index of 1.8.0
    idx180 = rsPayload.index("1.8.0")
    idx181 = rsPayload.index("1.8.1")
    idx182 = rsPayload.index("1.8.2")
    idx280 = rsPayload.index("2.8.0")
    idx281 = rsPayload.index("2.8.1")
    idx282 = rsPayload.index("2.8.2")
    idxIL1 = rsPayload.index("31.7.0")
    idxIL2 = rsPayload.index("51.7.0")
    idxIL3 = rsPayload.index("71.7.0")


    # 1.8.1(025139.058*kWh)
    energyValueLength=21

    # 31.7.0(000.71)
    currentValueLength=14
    
    parsedData =[]
    parsedData.append(rsPayload[idx180:(idx180+energyValueLength)])
    parsedData.append(rsPayload[idx181:(idx181+energyValueLength)])
    parsedData.append(rsPayload[idx182:(idx182+energyValueLength)])
    parsedData.append(rsPayload[idx280:(idx280+energyValueLength)])
    parsedData.append(rsPayload[idx281:(idx281+energyValueLength)])
    parsedData.append(rsPayload[idx282:(idx282+energyValueLength)])
    parsedData.append(rsPayload[idxIL1:(idxIL1+currentValueLength)])
    parsedData.append(rsPayload[idxIL2:(idxIL2+currentValueLength)])
    parsedData.append(rsPayload[idxIL3:(idxIL3+currentValueLength)])
    

    return transformAndStore(parsedData)


# Expects an array with the read values in sequence order;
# [0] -> 1.8.0, total consumed energy [kWh]
# [1] -> accumulated consumed energy high-tarif [KWh]
# [2] -> accumulated consumed energy low-tarif [kWh]
# [3] -> accumulated injected energy total [kWh]
# [4] -> accumulated injected energy high-tarif [kWh]
# [5] -> accumulated injected energy low-tarif [kWh]
# [6] -> currently delivered current L1 [A]
# [7] -> currently delivered current L2 [A]
# [8] -> currently delivered current L3 [A]
def transformAndStore(readData):
    try:
        # read file
        with open('/home/pi/read_data.json', 'r') as last_read:
            data_json=last_read.read()

        # parse file
        data = json.loads(data_json)
    except:
        print('Unable to read_data history assumes none existed.')
        defaults = '{"sampling":"'+str(datetime.datetime.now())+'", "consumedHighTarif":0,"injectedEnergyTotal":0,"consumedLowTarif":0,"liveCurrentL1":0,"liveCurrentL2":0,"liveCurrentL3":0}'
        data = json.loads(defaults)

    # Stored consumed energy
    # data['sampling']= str(datetime.datetime.now())
    data['sampling'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    data['consumedEnergyTotal'] = extractEnergy(readData[0])
    data['consumedHighTarif'] = extractEnergy(readData[1])
    data['consumedLowTarif'] = extractEnergy(readData[2])
    data['injectedEnergyTotal'] = extractEnergy(readData[3])
    data['injectedEnergyHighTarif'] = extractEnergy(readData[4])
    data['injectedEnergyLowTarif'] = extractEnergy(readData[5])

    data['liveCurrentL1'] = extractLiveCurrent(readData[6])
    data['liveCurrentL2'] = extractLiveCurrent(readData[7])
    data['liveCurrentL3'] = extractLiveCurrent(readData[8])

    try:
        jsonString = json.dumps(data)
        jsonFile = open("/home/pi/read_data.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
    except:
        print('Unable to write_data history. will not be able to compute delta consumption.')

    return jsonString

# 1.8.1(025139.058*kWh)
def extractEnergy(consumedEnergy):
    return consumedEnergy[7:16]


# 31.7.0(000.71)
def extractLiveCurrent(liveCurrent):
    return liveCurrent[7:12]