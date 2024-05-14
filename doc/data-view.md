# Data flow

This page describes the data flow from the power meter untill it gets posted to the API.

# Process

## 1 - Read data from the smart-meter using the _IR-Reader_

This produces the data in format like the _raw.json_ file.

```
/LGZ4ZMR120AC.K750
/LGZ4ZMR120AC.K750
F.F.0(00000000)
0.0.2(  175225)
0.0.0(13267131)
0.0.3(        )
1.8.1(026927.015*kWh)
1.8.2(021567.055*kWh)
2.8.1(000000.001*kWh)
2.8.2(000000.000*kWh)
1.8.0(048494.070*kWh)
2.8.0(000000.001*kWh)
15.8.0(048494.072*kWh)
C.7.0(0056)
32.7.0(237)
52.7.0(237)
72.7.0(237)
31.7.0(001.11)
51.7.0(001.78)
71.7.0(000.10)
p
```

## 2 - The relevant information are extracted

We read the `1.8.x` and `2.8.x` where the `.1` is the high-tarif and the `.2` is the low-tarif.

This is achieved using the `parse_powermeter_data(data)` python method.

## 3 - The data are transposed to a json object

This is done by the `transformAndStore()` method.

```json
{"consumedLowTarif": "21567.055", "injectedEnergyTotal": "21567.055", "liveCurrentL3": "001.7", "sampling": "2022-03-25 16:19:54.194134", "liveCurrentL1": "00000", "liveCurrentL2": "001.0", "consumedHighTarif": "26927.047"}
```