import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

from dataclasses_json import dataclass_json  # type: ignore


class CalculationStatus(Enum):
    UNKNOWN = 0
    INCALCULATION = 1
    INDATABASE = 2
    CALCULATIONSTARTED = 3
    CALCULATIONFAILED = 4


class ResultFileRequirement(Enum):
    """Determines whether specified result files are required or optional. Only
    when a required file is not created by the provider an error is raised."""

    REQUIRED = 0
    OPTIONAL = 1


@dataclass_json
@dataclass
class TimeSeriesRequest:
    simulation_config: str  # provider-specific string defining the requested data
    providername: str  # the provider which shall process the request
    guid: str = ""  # optional unique identifier, can be used to force recalculation of otherwhise identical requests
    # Result files created by the provider that are sent back as result. Throws an error if one of these files is not
    # created. If left empty returns all created files.
    required_result_files: Dict[str, Optional[ResultFileRequirement]] = field(default_factory=dict)  # type: ignore
    # Additional input files to be created in the provider container. Due to a bug in
    # dataclasses_json the 'bytes' type cannot be used here, so the file contents are
    # stored base64-encoded.
    input_files: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.required_result_files, dict):
            raise RuntimeError(
                "Invalid TimeSeriesRequest: the required_result_files attribute must be a dict"
            )
        if not isinstance(self.input_files, dict):
            raise RuntimeError(
                "Invalid TimeSeriesRequest: the input_files attribute must be a dict"
            )

    def get_hash(self) -> str:
        # hash the json representation of the object
        data = self.to_json().encode("utf-8")  # type: ignore
        return hashlib.sha256(data).hexdigest()


@dataclass_json
@dataclass
class ResultDelivery:
    original_request: TimeSeriesRequest
    data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.data.items():
            if isinstance(value, List):
                # bytes are stored as a list in json; convert it back
                self.data[key] = bytes(value)


@dataclass_json
@dataclass
class RestReply:
    result_delivery: Optional[bytes] = None
    status: CalculationStatus = CalculationStatus.UNKNOWN
    request_hash: str = ""
    info: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.status, int):
            # convert status from int to enum
            self.status = CalculationStatus(self.status)
        if isinstance(self.result_delivery, List):
            # bytes are stored as a list in json; convert it back
            self.result_delivery = bytes(self.result_delivery)
