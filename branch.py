from typing import List
from exceptions import InvalidIdError, StationIndexError, InvalidBranchDataType

class Branch():

    def __init__(self, branch_id:int, next_branch_ids:List[int]):
        if not isinstance(branch_id, int) or isinstance(branch_id, bool):
            raise InvalidIdError("Branch ID", branch_id, "must be an int")

        if not isinstance(next_branch_ids, list):
            raise InvalidDataType(type(next_branch_ids), "must be a valid list of integers")

        for next_id in next_branch_ids:
            if not isinstance(next_id, int) or isinstance(next_id, bool):
                raise InvalidIdError("Next branch ID", id, "must be an int")

        self.branch_id = branch_id
        self.next_branch_ids = list(next_branch_ids)
        self.stations : List[str] = []

    def add_station(self, station:str):
        """function to add station string to list of stations within an instance of branch"""
        if not isinstance(station, str):
            raise InvalidIdError("Station ID", station, "must be a valid string")

        if not station.strip():
            raise InvalidIdError("Station ID", station, "must be a valid string")

        self.stations.append(station)
    
    def station_edges(self) -> List[tuple[str, str]]: 
        """returns the edges between stations on this branch"""
        edges = []
        for i in range(len(self.stations) - 1):
            edges.append((self.stations[i], self.stations[i+1]))
        return edges
            

    def branch_edges(self) -> List[tuple[int, int]]:  
        """returns the edges between this branch and its next branches"""
        edges = []
        for i in range(len(self.next_branch_ids)):
            edges.append((self.branch_id, self.next_branch_ids[i]))
        return edges

    # magic methods
    def __len__(self):
        return len(self.stations)

    def __iter__(self):
        return iter(self.stations)

    def __contains__(self, station_id):
        return station_id in self.stations  

    def __getitem__(self, index):
        if not isinstance(index, int) or isinstance(index, bool):
            raise InvalidIdError("Index", index, "given type is not valid, must be an int")
        
        try:
            return self.stations[index]
        except IndexError as err:
            raise StationIndexError(index) from err

    def __repr__(self):
        return f"Branch(branch_id={self.branch_id!r}, next_branch_ids={self.next_branch_ids!r}, stations={self.stations!r})"