from typing import List
from exceptions import InvalidIdError

class Branch():

    def __init__(self, branch_id:int, next_branch_ids:List[int]):
        if not isinstance(branch_id, int):
            raise InvalidIdError("Branch ID", branch_id, "must be an int")

        for id in next_branch_ids:
            if not isinstance(id, int):
                raise InvalidIdError("Next branch ID", id, "must be an int")

        self.branch_id = branch_id
        self.next_branch_ids = next_branch_ids
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
        