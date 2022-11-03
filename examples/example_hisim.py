"""Requests a file containing KPIs generated from HiSim"""

import os
import time
from utspclient import result_file_filters

from utspclient.client import request_time_series_and_wait_for_delivery
from utspclient.datastructures import TimeSeriesRequest


# load a HiSim system configuration
example_folder = os.path.dirname(os.path.abspath(__file__))
system_config_path = os.path.join(example_folder, "input data\\hisim_config.json")
with open(system_config_path, "r") as config_file:
    system_config = config_file.read()

# Define URL to time Series request
URL = "http://localhost:443/api/v1/profilerequest"
API_KEY = ""

# Save start time for run time calculation
start_time = time.time()

# Call time series request function
request = TimeSeriesRequest(
    system_config,
    "hisim",
    required_result_files=dict.fromkeys(["KPIs.csv"]),
)
result = request_time_series_and_wait_for_delivery(URL, request, API_KEY)

kpi = result.data["KPIs.csv"].decode()

print("Calculation took %s seconds" % (time.time() - start_time))
# Print all results from the request
print("Example HiSim request")
print(f"Retrieved data: {kpi}")
