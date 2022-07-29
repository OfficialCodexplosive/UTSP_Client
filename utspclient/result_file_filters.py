"""
This module defines relevant output files for typical use cases to avoid transmitting
and storing unneeded files
"""


class LPGFilters:
    ELECTRICITY = "Results/Sum.Electricity.HH1.json"
    HOT_WATER = "Results/Sum.Hot Water.HH1.json"
    INNER_DEVICE_HEAT_GAINS = "Results/Sum.Innter Device Heat Gains.HH1.json"
    ACTIVITY_LEVEL_HIGH = "Results/BodilyActivityLevel.High.HH1.json"


class HiSimFilters:
    ELECTRICITY_SMART_1 = "ElectricityOutput_SmartDevice1.csv"


class PredefinedResultCollections:
    LPG_FOR_HISIM = [LPGFilters.ELECTRICITY, LPGFilters.INNER_DEVICE_HEAT_GAINS]
