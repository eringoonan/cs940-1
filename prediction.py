from exceptions import InvalidDataType, InvalidIdError

class Prediction():

    def __init__(self, vehicle_id:str, naptan_id:str, line_id:str,
                platform_name:str, destination_id:str, time_to_station:int, current_location:str):

        """intialise prediction object, raises invalid data and invalid ID errors for time_to_station"""

        if not isinstance(time_to_station, int) or isinstance(time_to_station, bool):
            raise InvalidDataType(type(time_to_station), "Must be a valid integer")

        if time_to_station < 0:
            raise InvalidIdError("Time to station", time_to_station, "must not be negative")

        self.vehicle_id = vehicle_id
        self.naptan_id = naptan_id
        self.line_id = line_id
        self.platform_name = platform_name
        self.destination_id = destination_id
        self.time_to_station = time_to_station
        self.current_location = current_location

    def __lt__(self, other):
        """compare self to other prediction by time to station with vehicle id tiebreaker, smaller wins"""
        if not isinstance(other, Prediction):
            return NotImplemented
        if self.time_to_station < other.time_to_station:
            return True
        elif self.time_to_station == other.time_to_station:
            if self.vehicle_id < other.vehicle_id:
                return True
        return False

    def __repr__(self):
        return f"Prediction(vehicle_id={self.vehicle_id!r}, naptan_id={self.naptan_id!r}, line_id={self.line_id!r}, time_to_station={self.time_to_station!r})"