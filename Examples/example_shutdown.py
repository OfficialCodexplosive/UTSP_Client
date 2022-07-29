"""
This example shows how to shutdown all UTSP workers
"""

import requests

URL = "http://localhost:443/api/v1/shutdown"
API_KEY = "OrjpZY93BcNWw8lKaMp0BEchbCc"
requests.post(URL, headers={"Authorization": API_KEY})
