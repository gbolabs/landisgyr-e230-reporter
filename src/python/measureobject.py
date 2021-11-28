import persistent
import json


class Measure(persistent.Persistent):

    # Constructor
    def __init__(self, samplingdatetime, liveL1, liveL2, liveL3, consumptionLow, consumptionHigh):
        super().__init__()
        self.samplingdatetime = samplingdatetime
        self.liveL1 = liveL1
        self.liveL2 = liveL2
        self.liveL3 = liveL3
        self.consumptionLow = consumptionLow
        self.consumptionHigh = consumptionHigh
    
    def __init__(self, jsonData):
        super().__init__()
        obj = json.loads(jsonData)
        self.samplingdatetime = obj["samplingdatetime"]
        self.liveL1 = obj["liveL1"]
        self.liveL2 = obj["liveL2"]
        self.liveL3 = obj["liveL3"]
        self.consumptionLow = obj["consumptionLow"]
        self.consumptionHigh = obj["consumptionHigh"]
        
    def ToJson(self):
        return json.dump(self)
        
        
