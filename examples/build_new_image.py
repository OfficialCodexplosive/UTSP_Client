"""
This example shows how to send a tar file containing the build context for a docker image
to the server, so that the server builds the new provider image.
This is done because the build context is usually significantly smaller than 
the built docker image file.
"""

import requests

URL = "http://134.94.131.167:443/api/v1/buildimage"
API_KEY = ""

file_path = r"examples\hisim.tar"
files = {"hisim-0.1.0": open(file_path, "rb")}

reply = requests.post(URL, files=files, headers={"Authorization": API_KEY})
print(reply.text)
