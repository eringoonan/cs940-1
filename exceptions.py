# file to define exceptions

# base class exceptions
class TubeError(Exception):
    """ base class for Tube related exceptions """

class DataStructureError(Exception):
    """ base class for data related exceptions """

# tube error sub classes

# handle invalid lat or lon
class InvalidCoordError(TubeError):
    """ raised to handle invalid latitude/longitude, takes in the coordinate (value) and latitude/longitude (field)"""

    COORDINATE_RANGES = {
        "longitude": "-180 to 180°",
        "latitude": "-90 to 90°"
    }

    def __init__(self, value, field, msg=" is not a valid value, must be a number from: "):
        self.value = value
        self.field = field
        self.msg = msg
        super().__init__(f'{self.field} {self.value!r} {self.msg} {self.COORDINATE_RANGES.get(field, "unknown coordinate")}')

# invalid station
class InvalidStationTypeError(TubeError):
    """raised to handle invalid instances of the Station class, takes in object"""
    def __init__(self, obj):
        super().__init__(f'The given object {type(obj).__name__} is not a valid instance of Station')

# invalid ID 
class InvalidIdError(TubeError):
    """exception used to handle invalid errors relating to IDs: branch, next branch, and station"""
    def __init__(self, idType, idValue, reason):
        self.idType = idType
        self.idValue = idValue
        self.reason = reason
        super().__init__(f'{self.idType} {self.idValue!r} is invalid: {self.reason}')

class StationIndexError(TubeError):
    """exception used to handle an invalid index relating to stations/branches"""
    def __init__(self, index):
        super().__init__(f'{index} is an invalid index')

class InvalidDataType(TubeError):
    def __init__(self, data_type, reason):
        self.data_type = data_type
        self.reason = reason
        super().__init__(f'The given datatype {self.data_type} is invalid: {self.reason}')

class DuplicateBranchError(TubeError):
    def __init__(self, branch_id, line_id):
        self.branch_id = branch_id
        self.line_id = line_id
        super().__init__(f'Branch {self.branch_id} already exists in line {self.line_id!r}')

class BranchNotFoundError(TubeError):
    def __init__(self, branch_id, line_id):
        self.branch_id = branch_id
        self.line_id = line_id
        super().__init__(f'Branch {self.branch_id} not found on line {self.line_id!r}')

# data error sub classes
class HeapError(DataStructureError):
    """used to raise errors regarding heap data structure, popping or peeking an empty heap, or passing an invalid k or malformed items"""

class InvalidTrieKeyError(DataStructureError):
    """used to raise errors regarding invalid trie keys, with invalid formatting, empty keys or invalid whitespace"""
    def __init__(self, key, msg):
        self.key = key
        self.msg = msg
        super().__init__(f'The given key {self.key!r} is invalid: {self.msg}')

class InvalidPrefixTypeError(DataStructureError):
    """used to raise errors regarding trie prefixes, including invalid types and invalid formatting"""
    def __init__(self, prefix, msg):
        self.prefix = prefix
        self.msg = msg
        super().__init__(f'The given prefix {self.prefix!r} is invalid: {self.msg}')