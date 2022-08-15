"""
Helper functions for creating requests for the LPG
"""
import inspect
from typing import Dict, List
from utspclient.helpers.lpgadapter import LPGExecutor
from utspclient.helpers.lpgdata import Households
from utspclient.helpers.lpgpythonbindings import (
    CalcOption,
    HouseCreationAndCalculationJob,
    HouseholdData,
    HouseholdDataSpecificationType,
    HouseholdNameSpecification,
    JsonReference,
)


def collect_lpg_households() -> Dict[str, JsonReference]:
    """
    Collects the JsonReferences of all predefined LPG household
    """
    members = inspect.getmembers(Households)
    predefined_households = {
        name: value for name, value in members if isinstance(value, JsonReference)
    }
    return predefined_households


def create_lpg_request(
    year: int,
    householdref: JsonReference,
    housetype: str,
    startdate: str = None,
    enddate: str = None,
    external_resolution: str = None,
    geographic_location: JsonReference = None,
    energy_intensity: str = "Random",
    calc_options: List[str] = None,
) -> HouseCreationAndCalculationJob:
    """
    Creates a basic LPG request from the most relevant parameters, using a default
    configuration for everything else.
    """
    request = LPGExecutor.make_default_lpg_settings(year, 0, 0)
    assert request.House is not None, "HouseData was None"
    assert request.CalcSpec is not None, "CalcSpec was None"
    request.CalcSpec.RandomSeed = -1
    request.CalcSpec.EnergyIntensityType = energy_intensity
    request.CalcSpec.StartDate = startdate
    request.CalcSpec.EndDate = enddate
    request.CalcSpec.ExternalTimeResolution = external_resolution
    request.CalcSpec.GeographicLocation = geographic_location
    if calc_options:
        request.CalcSpec.CalcOptions = calc_options
    request.House.HouseTypeCode = housetype
    hhnamespec = HouseholdNameSpecification(householdref)
    hhn = HouseholdData(
        None,
        None,
        hhnamespec,
        "hhid",
        "hhname",
        HouseholdDataSpecification=HouseholdDataSpecificationType.ByHouseholdName,
    )
    request.House.Households.append(hhn)
    return request
