"""
This module defines relevant output files for typical use cases to avoid transmitting
and storing unneeded files
"""


class LPGFilters:
    """
    Provides result file names for the LPG
    """

    @staticmethod
    def sum_hh1(load_type: str, json: bool = False, no_flex: bool = False) -> str:
        """Returns the file name of the sum load profile for the first simulated household, for the
        specified load type"""
        if json:
            flex = ".NoFlexDevices" if no_flex else ""
            return "Results/Sum{flex}.{load_type}.HH1.json".format(
                load_type=load_type, flex=flex
            )
        else:
            flex = ".NoFlex" if no_flex else ""
            return "Results/SumProfiles{flex}.HH1.{load_type}.csv".format(
                load_type=load_type, flex=flex
            )

    @staticmethod
    def sum_hh1_ext_res(
        load_type: str, resolution_in_s: int, json: bool = False
    ) -> str:
        """Returns the file name of the sum load profile for the first simulated household, for the
        specified load type, in the external resolution. The resolution specified here must match the
        external resolution specified in the LPG request.
        If the resolution is 60 s, the internal resolution file name is returned"""
        assert resolution_in_s != 60, (
            "The external resolution must not be 60s when using this file name, ",
            "because that is the internal resolution of the LPG and extra files for external resolution are not created. ",
            "Use the filename for the internal resolution files instead.",
        )
        # special case: external resolution is the same as the internal resolution of the LPG, so
        # the LPG does not generate extra files
        ext = "json" if json else "csv"
        return "Results/SumProfiles_{resolution_in_s}s.HH1.{load_type}.{ext}".format(
            load_type=load_type, resolution_in_s=resolution_in_s, ext=ext
        )

    class BodilyActivity:
        """Result file names for bodily activity"""

        _template = "Results/BodilyActivityLevel.{level}.HH1.json"
        HIGH = _template.format(level="High")
        LOW = _template.format(level="Low")
        OUTSIDE = _template.format(level="Outside")
        UNKNOWN = _template.format(level="Unknown")


class HiSimFilters:
    RESIDENCE_BUILDING = "Residence_Building.csv"
