import glob
import os
import random
import subprocess
from pathlib import Path
from typing import Any, List, Optional

import pandas as pd  # type: ignore

import utspclient.helpers.lpgdata as lpgdata


class LPGExecutor:
    def excute_lpg_locally(
        self,
        year: int,
        number_of_households: int,
        number_of_people_per_household: int,
        working_directory: str,
        startdate: Optional[str] = None,
        enddate: Optional[str] = None,
        loadtypes: Optional[List[str]] = None,
        transportation: bool = False,
    ) -> Optional[pd.DataFrame]:
        calculation_directory = Path(working_directory, "LPG")
        request = self.make_default_lpg_settings(
            year,
            number_of_households,
            number_of_people_per_household,
        )
        if request.CalcSpec is None:
            raise Exception("Failed to initialize the calculation spec")
        if startdate is not None:
            request.CalcSpec.set_StartDate(startdate)
        if enddate is not None:
            request.CalcSpec.set_EndDate(enddate)
        calcspecfilename = Path(calculation_directory, "calcspec.json")
        if transportation:
            request.CalcSpec.EnableTransportation = True
            request.CalcSpec.CalcOptions.append(
                lpgdata.CalcOption.TansportationDeviceJsons
            )
        if loadtypes is not None and len(loadtypes) > 0:
            request.CalcSpec.LoadtypesForPostprocessing = loadtypes
        with open(calcspecfilename, "w+") as calcspecfile:
            jsonrequest = request.to_json(indent=4)  # type: ignore
            calcspecfile.write(jsonrequest)
        self.execute_lpg(calculation_directory)
        resultsdir = Path(calculation_directory, "results", "Results")
        return self.read_all_json_results_in_directory(str(resultsdir))

    @staticmethod
    def execute_lpg(calculation_directory: Path) -> Any:
        # execute LPG
        pathname = Path(calculation_directory, "simulationengine.exe")
        os.chdir(str(calculation_directory))
        print("executing in " + str(calculation_directory))
        subprocess.run([str(pathname), "processhousejob", "-j", "calcspec.json"])

    @staticmethod
    def make_default_lpg_settings(
        year: int,
        number_of_households: int,
        number_of_people_per_household: int,
    ) -> lpgdata.HouseCreationAndCalculationJob:
        hj = lpgdata.HouseCreationAndCalculationJob()
        hj.set_Scenario("S1").set_Year(str(year)).set_DistrictName("district")
        hd = lpgdata.HouseData()
        hj.House = hd
        hd.Name = "House"
        hd.HouseGuid = lpgdata.StrGuid("houseguid")
        hd.HouseTypeCode = (
            lpgdata.HouseTypes.HT01_House_with_a_10kWh_Battery_and_a_fuel_cell_battery_charger_5_MWh_yearly_space_heating_gas_heating
        )
        hd.TargetCoolingDemand = 10000
        hd.TargetHeatDemand = 0
        hd.Households = []
        for idx in range(number_of_households):
            hhd: lpgdata.HouseholdData = lpgdata.HouseholdData()
            hhd.HouseholdDataSpecification = (
                lpgdata.HouseholdDataSpecificationType.ByPersons
            )
            hhd.HouseholdDataPersonSpec = lpgdata.HouseholdDataPersonSpecification()
            hhd.HouseholdDataPersonSpec.Persons = []
            hhd.ChargingStationSet = (
                lpgdata.ChargingStationSets.Charging_At_Home_with_03_7_kW_output_results_to_Car_Electricity
            )
            hhd.TravelRouteSet = (
                lpgdata.TravelRouteSets.Travel_Route_Set_for_30km_Commuting_Distance
            )
            hhd.TransportationDeviceSet = (
                lpgdata.TransportationDeviceSets.Bus_and_two_30_km_h_Cars
            )
            for person_idx in range(number_of_people_per_household):
                if person_idx % 2 == 0:
                    gender = lpgdata.Gender.Male
                else:
                    gender = lpgdata.Gender.Female
                age = 100 * random.random()

                persondata = lpgdata.PersonData(int(age), gender)
                hhd.HouseholdDataPersonSpec.Persons.append(persondata)
            hd.Households.append(hhd)
        cs: lpgdata.JsonCalcSpecification = lpgdata.JsonCalcSpecification()
        hj.CalcSpec = cs
        cs.LoadTypePriority = lpgdata.LoadTypePriority.All
        cs.DefaultForOutputFiles = lpgdata.OutputFileDefault.NoFiles
        cs.CalcOptions = [
            lpgdata.CalcOption.JsonHouseholdSumFiles,
            lpgdata.CalcOption.BodilyActivityStatistics,
        ]
        cs.EnergyIntensityType = lpgdata.EnergyIntensityType.Random
        cs.OutputDirectory = "/results"
        hj.PathToDatabase = "profilegenerator.db3"
        return hj

    @staticmethod
    def read_all_json_results_in_directory(
        results_directory: str,
    ) -> Optional[pd.DataFrame]:
        df: pd.DataFrame = pd.DataFrame()

        if not os.path.exists(str(results_directory)):
            return None

        # self.print("reading files in " + str(results_directory))
        potential_files = glob.glob(str(results_directory) + "/*.json")
        isFirst = True
        for file in potential_files:
            #                self.print("Reading json file " + str(file))
            print("Reading file " + str(file))
            with open(file) as json_file:
                filecontent: str = json_file.read()  # type: ignore
                sumProfile: lpgdata.JsonSumProfile = lpgdata.JsonSumProfile.from_json(filecontent)  # type: ignore
            if sumProfile.LoadTypeName is None:
                raise Exception("Empty load type name on " + file)
            if (
                sumProfile is None
                or sumProfile.HouseKey is None
                or sumProfile.HouseKey.HHKey is None
            ):
                raise Exception("empty housekey")
            key: str = (
                sumProfile.LoadTypeName + "_" + str(sumProfile.HouseKey.HHKey.Key)
            )
            df[key] = sumProfile.Values
            if isFirst:
                isFirst = False
                ts = sumProfile.StartTime
                timestamps = pd.date_range(ts, periods=len(sumProfile.Values), freq="T")
                df["Timestamp"] = timestamps
        return df
