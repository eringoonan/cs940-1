from typing import List
from exceptions import InvalidIdError

class Branch():

    def __init__(self, branch_id:int, next_branch_ids:List[int]):
        if not isinstance(branch_id, (int)):
            raise InvalidIdError("Branch ID", branch_id, "must be an int")

        for id in next_branch_ids:
            if not isinstance(id(int)):
                raise InvalidIdError("Next branch ID", id, "must be an int")

        self.branch_id = branch_id
        self.next_branch_ids = next_branch_ids
        self.stations : List[str] = []

    # def add_station(self, station:str):
    
    # def station_edges(self) -> List[tuple[str, str]]: returns the edges between stations on this branch;

    # def branch_edges(self) -> List[tuple[int, int]]:  returns the edges between this branch and its next branches.

    # magic methods
        