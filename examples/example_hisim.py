"""Requests a load profile that is generated using HiSim"""

import time
from utspclient import result_file_filters

from utspclient.client import request_time_series_and_wait_for_delivery

# Create a simulation configuration
simulation_config = """{
    "predictive": false,
    "prediction_horizon": 86400,
    "pv_included": false,
    "smart_devices_included": true,
    "boiler_included": "electricity",
    "heatpump_included": false,
    "battery_included": false,
    "chp_included": false
}"""

# Define URL to time Series request
URL = "http://localhost:443/api/v1/profilerequest"

API_KEY = "OrjpZY93BcNWw8lKaMp0BEchbCc"

# Save start time for run time calculation
start_time = time.time()

# Call time series request function
result = request_time_series_and_wait_for_delivery(
    URL,
    simulation_config,
    "hisim",
    API_KEY,
    required_result_files={result_file_filters.HiSimFilters.ELECTRICITY_SMART_1},
)

ts = result.data[result_file_filters.HiSimFilters.ELECTRICITY_SMART_1].decode()

print("Calculation took %s seconds" % (time.time() - start_time))
# Print all results from the request
print("Example sme-lpg request")
print("Retrieved data: {ts.split(os.linesep)[0]}")
