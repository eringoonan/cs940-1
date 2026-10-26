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


class InvalidBranchIdError(TubeError):
    """raised to handle invalid branch id numbers, takes in the id"""
    def __init__(self, branch_id):
        super().__init__(f'Branch Id {branch_id} is not a valid integer')

# data error sub classes