import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from dataclasses_json import dataclass_json  # type: ignore


class CalculationStatus(Enum):
    UNKNOWN = 0
    INCALCULATION = 1
    INDATABASE = 2
    CALCULATIONSTARTED = 3
    CALCULATIONFAILED = 4


@dataclass_json
@dataclass
class TimeSeriesRequest:
    simulation_config: str  # json string für die vollständige spezifikation
    providername: str  # welcher time series provider verwendet werden woll
    guid: str = ""  # eindeutiger identifier, optional
    required_result_files: Set[str] = field(default_factory=set)
    # Additional input files to be created in the provider container. Due to a bug in
    # dataclasses_json the 'bytes' type cannot be used here, so the file contents are
    # stored base64-encoded.
    input_files: Dict[str, str] = field(default_factory=dict)

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
