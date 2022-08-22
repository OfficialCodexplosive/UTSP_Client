import json
import time
from typing import Dict, List, Optional, Set, Union
import zlib

import requests
from pandas import DataFrame  # type: ignore
from utspclient.datastructures import (
    CalculationStatus,
    RestReply,
    ResultDelivery,
    TimeSeriesRequest,
)


def decompress_result_data(data: bytes) -> ResultDelivery:
    json_data = zlib.decompress(data).decode()
    return ResultDelivery.from_json(json_data)  # type: ignore


def send_request(
    url: str, request: Union[str, TimeSeriesRequest], api_key: str = ""
) -> RestReply:
    """
    Sends the request to the utsp and returns the reply

    :param url: URL of the utsp server
    :type url: str
    :param request: the request to send
    :type request: Union[str, TimeSeriesRequest]
    :param api_key: the api key to use, defaults to ""
    :type api_key: str, optional
    :raises Exception: if the server reported an error
    :return: the reply from the utsp server
    :rtype: RestReply
    """
    if isinstance(request, TimeSeriesRequest):
        request = request.to_json()  # type: ignore
    response = requests.post(url, json=request, headers={"Authorization": api_key})
    if not response.ok:
        raise Exception(f"Received error code: {str(response)}")
    response_dict = response.json()
    # don't use dataclasses_json here, it has bug regarding bytes
    reply = RestReply(**response_dict)  # type: ignore
    return reply


def get_result(reply: RestReply) -> Optional[ResultDelivery]:
    """
    Helper function for getting a time series out of a rest reply if it was delivered.
    Raises an exception when the calculation failed

    :param reply: the reply from the utsp server to check for a time series
    :type reply: RestReply
    :raises Exception: if the calculation failed
    :return: the delivered time series, or None
    :rtype: Optional[TimeSeriesDelivery]
    """
    status = reply.status
    # parse and return the time series if it was delivered
    if status == CalculationStatus.INDATABASE:
        return decompress_result_data(reply.result_delivery)  # type: ignore
    # if the time series is still in calculation, return None
    if status in [
        CalculationStatus.CALCULATIONSTARTED,
        CalculationStatus.INCALCULATION,
    ]:
        return None
    # the calculation failed: raise an error
    if status == CalculationStatus.CALCULATIONFAILED:
        raise Exception("Calculation failed: " + (reply.info or ""))
    raise Exception("Unknown status")


def request_time_series_and_wait_for_delivery(
    url: str,
    request: Union[str, TimeSeriesRequest],
    api_key: str = "",
) -> ResultDelivery:
    """
    Requests a single time series from the UTSP server from the specified time series provider

    :param url: URL of the UTSP server
    :type url: str

    :param time_series_definition: JSON string containing a definition of the requested time series
    :type time_series_definition: str

    :param providername: Name of the desired time series provider (e.g. LPG)
    :type providername: str

    :param load_type: Requested load type
    :type load_type: str

    :param guid: Self-chosen GUID for identification of the request. Choose a different GUID to
                 receive a new time series. Defaults to ""
    :type guid: str, optional

    :param api_key: API key for accessing the UTSP, defaults to ""
    :type api_key: str, optional

    :param input_files: dict of names and content of additional input files, defaults to None
    :type input_files: Dict[str, str], optional

    :raises Exception: Raises an exception if the calculation failed or if the request status
                       is unknown

    :return: The requested time series
    :rtype: TimeSeriesDelivery
    """
    if isinstance(request, TimeSeriesRequest):
        request = request.to_json()  # type: ignore
    status = CalculationStatus.UNKNOWN
    wait_count = 0
    while status not in [
        CalculationStatus.INDATABASE,
        CalculationStatus.CALCULATIONFAILED,
    ]:
        reply = send_request(url, request, api_key)
        status = reply.status
        wait_count += 1
        if status != CalculationStatus.INDATABASE:
            time.sleep(1)
            print("waiting for " + str(wait_count))
    ts = get_result(reply)
    assert ts is not None, "No time series was delivered"
    print("finished")
    return ts


def write_profiles(reply: RestReply) -> None:
    tsdstr = reply.result_delivery
    if tsdstr is not None and len(tsdstr) > 0:
        tsd: ResultDelivery = ResultDelivery.from_json(tsdstr)  # type: ignore
        if tsd.original_request is not None:
            print(tsd.original_request.guid)
    else:
        print("got a in database but empty reply")


def request_lpg_pandas_dataframe(
    url: str, housejob: str, guid: str, loadtypes: List[str]
) -> DataFrame:
    myrequest = TimeSeriesRequest(
        simulation_config=housejob,
        providername="LPG",
        guid=guid,
        required_result_files="Electricity",
    )
    request_json_str = myrequest.to_json()  # type: ignore
    reply: CalculationStatus = CalculationStatus.UNKNOWN
    waitCountIdx = 0
    myreply = None
    while (
        reply != CalculationStatus.INDATABASE
        and reply != CalculationStatus.CALCULATIONFAILED
    ):
        response = requests.post(url, json=request_json_str)
        jsonrsp = response.json()
        rspstr = json.dumps(jsonrsp)
        myreply = RestReply.from_json(rspstr)  # type: ignore
        reply = myreply.CurrentStatus
        waitCountIdx += 1
        if reply != CalculationStatus.INDATABASE:
            time.sleep(1)
        print("waiting for " + str(waitCountIdx))
    if reply == CalculationStatus.INDATABASE and myreply is not None:
        tsd: ResultDelivery = ResultDelivery.from_json(myreply.TimeSeriesDelivery)  # type: ignore
        return tsd
    if reply == CalculationStatus.CALCULATIONFAILED:
        print("calculation failed")
        raise Exception("Calculation failed")
    print("unknown status")
    raise Exception("unknown status")


def wait_for_finish(open_requests: List[str], url: str) -> None:
    waitcount = 1
    while len(open_requests) > 0:
        request_json_str = open_requests[0]
        response = requests.post(url, json=request_json_str)
        jsonrsp = response.json()
        rspstr = json.dumps(jsonrsp)

        myreply: RestReply = RestReply.from_json(rspstr)  # type: ignore
        if myreply.status == CalculationStatus.INDATABASE:
            write_profiles(myreply)
            open_requests.remove(request_json_str)

        waitcount += 1
        print("waiting for " + str(waitcount))
        time.sleep(1)
