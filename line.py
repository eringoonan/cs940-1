from exceptions import InvalidIdError, InvalidDataType, DuplicateBranchError
from branch import Branch

class Line():

    def __init__(self, line_id:str, line_name:str):
        if not line_id.strip():
            raise InvalidIdError("Line ID", line_id, "Must be a valid string")

        if not line_name.strip():
            raise InvalidIdError("Line name", line_name, "Must be a valid string")

        self.line_id = line_id
        self.line_name = line_name
        self.branches: dict[int, Branch] = {}

    def add_branch(self, branch:Branch) -> None:
        if not isinstance(branch, Branch):
            raise InvalidDataType(type(branch), "Must be an instance of branch")

        if branch.branch_id in self.branches:
            raise DuplicateBranchError(branch.branch_id, self.line_id)