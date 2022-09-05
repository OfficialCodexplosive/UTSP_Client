"""Requests a load profile that is generated using HiSim"""

import time
from utspclient import result_file_filters

from utspclient.client import request_time_series_and_wait_for_delivery
from utspclient.datastructures import TimeSeriesRequest

# Create a simulation configuration
simulation_config = """{
    "location": "Aachen",
    "occupancy_profile": "CH01",
    "building_code": "DE.N.SFH.05.Gen.ReEx.001.002",
    "predictive": true,
    "prediction_horizon": 86400,
    "pv_included": true,
    "pv_peak_power": 10000,
    "smart_devices_included": true,
    "water_heating_system_installed": "HeatPump",
    "heating_system_installed": "HeatPump",
    "buffer_included": true,
    "buffer_volume": 500,
    "battery_included": true,
    "battery_capacity": 10000,
    "chp_included": true,
    "chp_power": 10000,
    "h2_storage_size": 100,
    "electrolyzer_power": 5000,
    "current_mobility": "NoCar",
    "mobility_distance": "rural"
}"""

# Define URL to time Series request
URL = "http://localhost:443/api/v1/profilerequest"

API_KEY = ""

# Save start time for run time calculation
start_time = time.time()

# Call time series request function
request = TimeSeriesRequest(
    simulation_config,
    "hisim",
    required_result_files=dict.fromkeys(
        [result_file_filters.HiSimFilters.RESIDENCE_BUILDING]
    ),
)
result = request_time_series_and_wait_for_delivery(URL, request, API_KEY)

ts = result.data[result_file_filters.HiSimFilters.RESIDENCE_BUILDING].decode()

print("Calculation took %s seconds" % (time.time() - start_time))
# Print all results from the request
print("Example sme-lpg request")
print(f"Retrieved data: {ts[:100]}")
