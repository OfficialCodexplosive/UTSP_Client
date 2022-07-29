def request_profiles(open_requests: List[str], url: str) -> None:
    for x in range(29):
        with open("t1.json", "r") as myfile:
            data = myfile.read()
        # tsdef = json.load(data)

        myrequest = TimeSeriesRequest(
            profiledefinition=data,
            providername="LPG",
            guid="myguid" + str(x),
            loadtype="Electricity",
        )
        request_json_str = myrequest.to_json()  # type: ignore
        response = requests.post(url, json=request_json_str)
        jsonrsp = response.json()
        rspstr = json.dumps(jsonrsp)
        myreply: RestReply = RestReply.from_json(rspstr)  # type: ignore
        with open("t2.json", "w") as myfile:
            myfile.write(myreply.to_json())  # type: ignore

        if myreply.CurrentStatus != ProfileStatus.InDatabase:
            open_requests.append(request_json_str)
        else:
            write_profiles(myreply)

        time.sleep(0.1)


if __name__ == "__main__":
    testurl = "http://127.0.0.1:5000/api/v1/profilerequest"
    all_open_requests: List[str] = []
    request_profiles(all_open_requests, testurl)
    wait_for_finish(all_open_requests, testurl)
