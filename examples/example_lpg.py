"""Requests a load profile that is generated using the Load Profile Generator (LPG)"""
#%% imports
from utspclient.datastructures import TimeSeriesRequest
from utspclient.helpers.lpgadapter import LPGExecutor
import utspclient.client as utsp_client
from utspclient import result_file_filters
from utspclient.helpers.lpgpythonbindings import CalcOption


#%% Create a simulation configuration for the LPG
simulation_config = LPGExecutor.make_default_lpg_settings(2020, 1, 2)
assert simulation_config.CalcSpec is not None
simulation_config.CalcSpec.EndDate = "2020-01-3"
simulation_config.CalcSpec.StartDate = "2020-01-01"
simulation_config.CalcSpec.ExternalTimeResolution = "00:15:00"
simulation_config.CalcSpec.CalcOptions.append(
    CalcOption.SumProfileExternalIndividualHouseholdsAsJson
)

simulation_config_json = simulation_config.to_json(indent=4)  # type: ignore

#%% Define connection parameters
REQUEST_URL = "http://localhost:443/api/v1/profilerequest"
API_KEY = "OrjpZY93BcNWw8lKaMp0BEchbCc"

#%% Prepare the time series request
request = TimeSeriesRequest(
    simulation_config_json,
    "LPG",
    required_result_files={result_file_filters.LPGFilters(900).ELECTRICITY},
)

#%% Request the time series
result = utsp_client.request_time_series_and_wait_for_delivery(
    REQUEST_URL, request, api_key=API_KEY
)

#%% Decode result data
file_content = result.data[result_file_filters.LPGFilters(900).ELECTRICITY].decode()
print(file_content)
