from typing import Dict, List

from heap import Heap
from line import Line
from prediction import Prediction
from station import Station
from trie import Trie

from exceptions import InvalidDataType, LineNotFoundError, StationNotFoundError, InvalidIdError, StationNotOnLineError


class Network():

    def __init__(self):
        """intialise the network class, create several dictionaries and a trie used to store classes and datastructures on the network"""
        self._lines: Dict[str, Line] = {}
        self._stations: Dict[str, Station] = {}

        self._name_trie: Trie = Trie()

        self._pred_by_station: Dict[str, Heap] = {}
        self._pred_by_line: Dict[str, Heap] = {}
        self._pred_by_station_line: Dict[tuple[str, str], Heap] = {}
        self._pred_by_train: Dict[str, Heap] = {}


    def add_line(self, line: Line) -> None:
        """take in an instance of the line class, verify the type and add it to the network line dictionary by line_id"""
        if not isinstance(line, Line):
            raise InvalidDataType(type(line), "Must be a valid instance of the line class")

        if line.line_id in self._lines: return

        self._lines[line.line_id] = line


    def get_line(self, line_id: str) -> Line:
        """take in a line id, verify the existence in lines and then return the instance of the line class associated with it"""
        if not isinstance(line_id, str):
            raise InvalidDataType(type(line_id), "Must be a valid instance of string")

        if line_id not in self._lines:
            raise LineNotFoundError(line_id)

        return self._lines[line_id]
    

    def add_station(self, station: Station) -> None:
        """take in an instance of the station class, verify the type and add it to the network station dictionary by station_id, normalise the station name then push it to the trie"""
        if not isinstance(station, Station):
            raise InvalidDataType(type(station), "Must be a valid instance of the station class")

        if station.station_id in self._stations: return

        self._stations[station.station_id] = station

        normalised_station = self._normalise_text(station.station_name)
        if normalised_station != "":
            self._name_trie.insert(normalised_station, station)


    def get_station(self, station_id: str) -> Station:
        """take in a station id, verify the existence in stations and then return the instance of the station class associated with it"""
        if not isinstance(station_id, str):
            raise InvalidDataType(type(station_id), "Must be a valid instance of string")

        if station_id not in self._stations:
            raise StationNotFoundError(station_id)

    def add_prediction(self, prediction: Prediction) -> None:
        """take in an instance of the prediction class, extract key details and use them to insert the prediction into related heap structures"""
        if not isinstance(prediction, Prediction):
            raise InvalidDataType(type(prediction), "Must be a valid instance of the predicition class")

        station = prediction.naptan_id
        line = prediction.line_id
        station_line = (prediction.naptan_id, prediction.line_id)
        train = f"{prediction.vehicle_id}{prediction.line_id}"

        if station not in self._pred_by_station:
            heap = Heap()
            self._pred_by_station[station] = heap

        self._pred_by_station[station].push(prediction.time_to_station, prediction)

        if line not in self._pred_by_line:
            heap = Heap()
            self._pred_by_line[line] = heap

        self._pred_by_line[line].push(prediction.time_to_station, prediction)

        if station_line not in self._pred_by_station_line:
            heap = Heap()
            self._pred_by_station_line[station_line] = heap

        self._pred_by_station_line[station_line].push(prediction.time_to_station, prediction)

        if train not in self._pred_by_train:
            heap = Heap()
            self._pred_by_train[train] = heap

        self._pred_by_train[train].push(prediction.time_to_station, prediction)


    def search_by_prefix(self, prefix: str) -> List[Station]:
        """takes in a prefix, normalises it and then calls the trie search by prefix method to retrieve relevant objects"""

        if not isinstance(prefix, str):
            raise InvalidDataType(type(prefix), "Must be a valid instance of string")

        normalised_prefix = self._normalise_text(prefix)
        results = self._name_trie.search_by_prefix(normalised_prefix)

        sorted(results, key=lambda s: s.station_name)
        return results


    def next_arrivals_by_station(self, station_id: str, k: int) -> List[Prediction]:
        """take in a station id and a number of requested values (k) and return the ksmallest list of predictions from the appropriate heap"""
        self._validate_k(k)

        if not isinstance(station_id, str):
            raise InvalidDataType(type(station_id), "Must be a valid instance of string")

        if station_id not in self._stations:
            raise StationNotFoundError(station_id)

        if station_id not in self._pred_by_station: return []

        return self._pred_by_station[station_id].ksmallest(k)

    
    def next_arrivals_by_line(self, line_id: str, k: int) -> List[Prediction]:
        """take in a line id and a number of requested values (k) and return the ksmallest list of predictions from the appropriate heap"""

        self._validate_k(k)

        if not isinstance(line_id, str):
            raise InvalidDataType(type(line_id), "Must be a valid instance of string")

        if line_id not in self._lines:
            raise LineNotFoundError(line_id)

        if line_id not in self._pred_by_line: return []

        return self._pred_by_line[line_id].ksmallest(k)
    

    def next_arrivals_by_station_and_line(self, station_id: str, line_id: str, k:int) -> List[Prediction]:
        """take in a station id, a line id, and a number of requested values (k) and return the ksmallest list of predictions from the appropriate heap"""
        self._validate_k(k)

        if not isinstance(station_id, str): raise InvalidDataType(type(station_id), "Must be a valid instance of string")
        if not isinstance(line_id, str): raise InvalidDataType(type(line_id), "Must be a valid instance of string")

        if station_id not in self._stations: raise StationNotFoundError(station_id)
        if line_id not in self._lines:raise LineNotFoundError(line_id)

        if station_id not in self._lines[line_id].get_stations(): raise StationNotOnLineError(station_id, line_id)

        if (station_id, line_id) not in self._pred_by_station_line: return []

        return self._pred_by_station_line[(station_id, line_id)].ksmallest(k)


    def next_stations_by_train(self, vehicle_id: str, line_id: str, k: int) -> List[Prediction]:
        """take in a vehicle id, a line id, and a number of requested values (k) and return the ksmallest list of predictions from the appropriate heap"""
        self._validate_k(k)

        if not isinstance(vehicle_id, str): raise InvalidDataType(type(vehicle_id), "Must be a valid instance of string")
        if not isinstance(line_id, str): raise InvalidDataType(type(line_id), "Must be a valid instance of string")

        if line_id not in self._lines: raise LineNotFoundError(line_id)

        train = f'{vehicle_id}{line_id}'

        if train not in self._pred_by_train: return []

        return self._pred_by_train[train].ksmallest(k)

    def _validate_k(self, k):
        """take in an int k and validate the datatype and the range"""
        if not isinstance(k, int) or isinstance(k, bool):
            raise InvalidDataType(type(k), k, "Must be a valid integer -1 or greater")

        if k < -1:
            raise InvalidDataType(type(k), k, "Must be a valid integer -1 or greater")

    @staticmethod
    def _normalise_text(text: str):
        """take in a string, turn it to lower case, remove /- and extra whitespace and return a new cleaned string"""
        text = text.lower()

        text = text.replace('/', ' ').replace('-', ' ')

        new_text = "".join(char for char in text if char.isalnum() or char == " ")

        new_text = " ".join(new_text.split())

        return new_text

