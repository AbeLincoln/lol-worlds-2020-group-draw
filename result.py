from itertools import permutations
from teams import pool1


class SameRegionError(Exception):
    """Raised when attempting to add a Team to a Group which already has a team from that Region."""
    pass


class SamePoolError(Exception):
    """Raised when attempting to add a Team to a Group which already has a team from that Pool."""
    pass


class NoValidGroupError(Exception):
    """Raised when attempting to add a Team to a list of Groups where none of the Groups are valid options."""
    pass


class FutureRegionError(Exception):
    """Raised when attempting to add a Team to a Group which would leave a later Team without a valid Group."""
    pass


class Group:
    teams = []

    def __init__(self, teams=None):
        self.teams = []
        self.add_teams(teams)

    def add_teams(self, teams=None):
        """
        Validates, then adds the teams to the group in the order specified
        :param teams: Tuple of teams to add to the Group
        :return: None
        """
        if teams is None:
            return
        for team in teams:
            self.add_team(team)

    def add_team(self, team):
        """
        Validates, then adds the team to the group
        :param team: Team to be added
        :return: True if team was added without raising an Exception
        """
        result = self.validate(team)

        def get_pool(t):
            return t.pool

        teams = self.teams

        teams.append(team)
        self.teams = sorted(teams, key=get_pool)

        return result

    def validate(self, team):
        """
        Validate that the team can be placed in this group, ignoring outside groups
        :param team: Team to be placed
        :return: True if the team is a valid option
        :raises SameRegionError: A team from the same region already exists in this group.
        :raises SamePoolError: A team from the same pool already exists in this group.
        """
        for t in self.teams:
            if t.region == team.region:
                raise SameRegionError(f"A team from {t.region} already exists in this group.")
            elif t.pool == team.pool:
                raise SamePoolError(f"A team from pool {t.pool} already exists in this group.")
        return True

    def __repr__(self):
        return f"({', '.join(map(str, self.teams))})"


class Result:
    groups = []
    perm1 = ()
    perm2 = ()
    perm3 = ()
    perm4 = ()
    neededSwap = False
    invalid = False

    def __init__(self, perm1, perm2, perm3, perm4):
        self.groups = []
        self.perm1 = perm1
        self.perm2 = perm2
        self.perm3 = perm3
        self.perm4 = perm4
        self.neededSwap = False
        self.invalid = False

        self._simulate_(perm1, perm2, perm3, perm4)

    def _simulate_(self, perm1, perm2, perm3, perm4):
        """
        NOTE: This method would greatly benefit from Memoization.  This is left as an exercise for the dedicated.
        :param perm1: Pick order for Pool 1
        :param perm2: Pick order for Pool 2
        :param perm3: Pick order for Pool 3
        :param perm4: Pick order for Pool 4
        :return: True if the simulation is valid for this pick order.
        """
        group_a = Group()
        group_b = Group()
        group_c = Group()
        group_d = Group()
        self.groups = [group_a, group_b, group_c, group_d]

        # Pool 1 is easy
        for i in range(4):
            self.groups[i].add_team(perm1[i])
        # Pool 2 is when we must start checking for region duplicates in groups
        for i in range(4):
            remaining_teams = perm2[i+1:]
            self.add_pool_2_team(perm2[i], self.groups, remaining_teams)
        # Pool 3 is when we must start checking for enough space for remaining teams in later groups as well
        for i in range(4):
            remaining_teams = perm3[i+1:]
            self.add_pool_3_team(perm3[i], self.groups, remaining_teams)
        # Pool 4 is similar to Pool 2, where we no longer care about future pools
        for i in range(4):
            remaining_teams = perm4[i+1:]
            self.add_pool_2_team(perm4[i], self.groups, remaining_teams)

    def add_pool_2_team(self, team, group_priority, remaining_teams):
        """
        Attempts to add the given team to the groups specified.  It stops once the team is added.
        This is only valid for Pool 1, 2, and 4 teams.
        :param team: Team to add to a group
        :param group_priority: Tuple of Groups team should be added to, in order of preference
        :param remaining_teams: Tuple of Teams left from Pool 3 which need to be added later
        :return: Group which we added the team to
        :raises NoValidGroupError: We could not add the team to any groups
        """

        for group in group_priority:
            try:
                # Confirm that the remaining groups will not be a problem
                group.validate(team)
                remaining_groups = []
                for test_group in group_priority:
                    has_pool = False
                    for test_team in test_group.teams:
                        if test_team.pool == team.pool:
                            has_pool = True
                    if (not has_pool) and (test_group is not group):
                        remaining_groups.append(test_group)
                self.validate_remaining_pool(remaining_teams, remaining_groups)
                if group.add_team(team):
                    return group
            except SamePoolError:
                # Group was filled already
                continue
            except (SameRegionError, FutureRegionError):
                self.neededSwap = True
        # raise NoValidGroupError(f"Could not find a valid group to place {team} into.")
        self.invalid = True

    def add_pool_3_team(self, team, group_priority, remaining_teams):
        """
        Attempts to add the given team to the groups specified.  It stops once the team is added.
        This is only useful for Pool 3 teams.
        :param team: Team to add to a group
        :param group_priority: Tuple of Groups team should be added to, in order of preference
        :param remaining_teams: Tuple of Teams left from Pool 3 which need to be added later
        :return: Group which we added the team to
        :raises NoValidGroupError: We could not add the team to any groups
        """

        for group in group_priority:
            try:
                self.validate_pool_3_team(team, group, group_priority, remaining_teams)
                if group.add_team(team):
                    return group
            except SamePoolError:
                # Group was filled already
                continue
            except FutureRegionError:
                # There will not be enough room for all
                continue
            except SameRegionError:
                self.neededSwap = True
        # raise NoValidGroupError(f"Could not find a valid group to place {team} into.")
        self.invalid = True

    def validate_pool_3_team(self, team, group, group_priority, remaining_teams):
        """
        Validate that the Pool 3 Team can be placed in this Group
        :param team: Team to add to a group
        :param group: Group to add the Team to
        :param group_priority: Tuple of Groups team should be added to, in order of preference
        :param remaining_teams: Tuple of Teams left from Pool 3 which need to be added after this one
        :return: True if the placement is valid
        :raises SameRegionError: A team from the same region already exists in this group.
        :raises SamePoolError: A team from the same pool already exists in this group.
        :raises FutureRegionError: A future team will have no valid Groups if this team is placed in this Group.
        """

        # First, easily validate the group locally
        group.validate(team)

        if len(remaining_teams) == 0:
            return True

        # Validate the future, ignoring Pool 4
        unfilled_groups = []
        for test_group in group_priority:
            has_pool = False
            for test_team in test_group.teams:
                if test_team.pool == 3:
                    has_pool = True
            if (not has_pool) and test_group != group:
                unfilled_groups.append(test_group)
        self.validate_remaining_pool(remaining_teams, unfilled_groups)

        # Validate that Pool 4 causes no conflicts (NOTE: hardcoded for 2020)
        # 1) If placing the last Pool 3 CN/EU team, every other group must have a CN/EU seed in it
        if (team.region == "Europe") or (team.region == "China"):
            # TODO: confirm
            is_last = True
            for test_team in remaining_teams:
                if (test_team.region == "Europe") or (test_team.region == "China"):
                    is_last = False
            if is_last:
                all_meet_criteria = True
                for test_group in group_priority:
                    team_meets_criteria = False
                    if test_group is group:
                        continue
                    for test_team in test_group.teams:
                        if (test_team.region == "Europe") or (test_team.region == "China"):
                            team_meets_criteria = True
                    if not team_meets_criteria:
                        all_meet_criteria = False
                if not all_meet_criteria:
                    raise FutureRegionError("Pool 4 will not have room for both a CN and EU team")
        # 2) If placing a non-CN/EU team, there must be a CN/EU team already present
        else:
            meets_criteria = False
            for test_team in group.teams:
                if (test_team.region == "Europe") or (test_team.region == "China"):
                    meets_criteria = True
                    break
            if not meets_criteria:
                raise FutureRegionError("Pool 4 will not have room for both a CN and EU team")
        # If we made it this far, the pick is valid!
        return True

    @staticmethod
    def validate_remaining_pool(remain_teams, remain_groups):
        """
        Validates that there exist room for the given Teams from the same Pool to fit into the remaining Groups
        :param remain_teams: Tuple of Teams from the current Pool which need to be added
        :param remain_groups: List of Groups which do not have a team from the current Pool
        :return: True if there exists a single valid future combination
        :raises FutureRegionError: The given Teams and Groups have no valid placements.
        :raises SamePoolError: At least one of the given Groups already has a team from the current Pool.
        """
        if len(remain_teams) == 0:
            return True
        elif len(remain_groups) != len(remain_teams):
            raise Exception(f"Can not fit {len(remain_teams)} teams into {len(remain_groups)} groups after this one.")

        team_permutations = list(permutations(remain_teams))
        for teams in team_permutations:
            try:
                for i in range(len(teams)):
                    remain_groups[i].validate(teams[i])
            except SameRegionError:
                continue
            # If we get here, it must be possible.
            return True
        # If we get here, we did not find a valid permutation
        raise FutureRegionError(f"There is no way to fit {remain_teams} in {remain_groups}")

    def sort_groups(self):
        """
        Sorts the list of Groups to be in Pool 1 order
        :return: None
        """
        temp_groups = []
        for i in range(len(self.groups)):
            for group in self.groups:
                if group.teams[0] == pool1[i]:
                    temp_groups.append(group)
        self.groups = temp_groups

    def __repr__(self):
        return f"{'invalid' if self.invalid else ''}{self.groups} - draws: ({self.perm1}, {self.perm2}, {self.perm3}, {self.perm4})"
