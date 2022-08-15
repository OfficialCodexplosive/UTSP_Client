"""
This module defines relevant output files for typical use cases to avoid transmitting
and storing unneeded files
"""


class LPGFilters:
    def __init__(self, resolution_in_s: int = 900) -> None:
        self.resolution_in_s = resolution_in_s

        self.ELECTRICITY = (
            "Results/SumProfiles_{resolution_in_s}s.HH1.Electricity.json".format(
                resolution_in_s=resolution_in_s
            )
        )
        self.HOT_WATER = "Results/SumProfiles_{resolution_in_s}s.HH1.Hot Water.json".format(
            resolution_in_s=resolution_in_s
        )
        self.INNER_DEVICE_HEAT_GAINS = "Results/SumProfiles_{resolution_in_s}s.HH1.Innter Device Heat Gains.json".format(
            resolution_in_s=resolution_in_s
        )
        self.ACTIVITY_LEVEL_HIGH = (
            "Results/SumProfiles_{resolution_in_s}s.HH1.High.json".format(
                resolution_in_s=resolution_in_s
            )
        )


class HiSimFilters:
    ELECTRICITY_SMART_1 = "ElectricityOutput_SmartDevice1.csv"


class PredefinedResultCollections:
    LPG_FOR_HISIM = [LPGFilters(60).ELECTRICITY, LPGFilters(60).INNER_DEVICE_HEAT_GAINS]
