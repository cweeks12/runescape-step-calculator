import json

import garminconnect
import datetime


class RunescapeStepCalculator:
    def __init__(self, credential_path=None):
        if credential_path is None:
            credential_path = '~/.garth'

        self.garmin = garminconnect.Garmin()
        self.garmin.login(credential_path)

        self.walking_ratio = 5
        self.running_ratio = 2

    def get_total_steps_for_date(self, date: datetime.date) -> str:
        """
        Gets the number of steps taken on a given date
        :param date: The date you want to know your step count on
        :return: The total step count
        """
        # This returns an array of length 1, so we need to pull the first value out
        return self.garmin.get_daily_steps(date, date)[0]['totalSteps']

    def get_activity_steps_for_date(self, date: datetime.date) -> str:
        """
        Gets the total number of steps taken during activities on a given date.
        :param date: The date you want to know your activity step count on
        :return: The total activity step count
        """
        full_activity_summary = self.garmin.get_activities_fordate(str(date))
        activities = full_activity_summary['ActivitiesForDay']['payload']

        total_steps = 0
        for activity in activities:
            total_steps += activity['steps']
        return str(total_steps)

    def get_walking_steps_for_date(self, date: datetime.date) -> str:
        """
        Calculates non-running steps for a given date. This assumes that all running happened in an activity.
        :param date: The date you want to know your non-activity step count on
        :return: The total non-activity steps
        """
        return str(int(self.get_total_steps_for_date(date)) - int(self.get_activity_steps_for_date(date)))

    def get_allowed_runescape_steps_for_date(self, date: datetime.date) -> str:
        """
        Calculates how many steps are allowed for a certain day in RuneScape given the ratios of real steps to RuneScape
        steps.
        :param date: The date you want to know allowed steps for
        :param walking_ratio: Number of real walking steps you have to take for 1 step in RuneScape
        :param running_ratio: Number of real running steps you have to take for 1 step in RuneScape
        :return: Total allowed RuneScape steps
        """
        walking_steps = int(self.get_walking_steps_for_date(date)) // self.walking_ratio
        running_steps = int(self.get_activity_steps_for_date(date)) // self.running_ratio
        return str(walking_steps + running_steps)

    def get_running_step_ratio(self) -> str:
        """
        Returns the set ratio for running steps to RuneScape steps
        :return: Current running step ratio
        """
        return str(self.running_ratio)

    def get_walking_step_ratio(self) -> str:
        """
        Returns the set ratio for walking steps to RuneScape steps
        :return: Current walking step ratio
        """
        return str(self.walking_ratio)

    def get_activites_for_date(self, date: datetime.date) -> list[dict[str]]:
        parsed_activities = []
        for activity in self.garmin.get_activities_fordate(str(date))['ActivitiesForDay']['payload']:
            parsed_activities.append(self._parse_activity(activity))
        return parsed_activities

    @staticmethod
    def _parse_activity(activity: dict[str]) -> dict[str]:
        keys_to_return = [
            'distance',
            'duration',
            'calories',
            'steps',
            'duration'
        ]
        parsed_dictionary = dict()

        for key in keys_to_return:
            parsed_dictionary[key] = activity[key]

        return parsed_dictionary


if __name__ == '__main__':
    calc = RunescapeStepCalculator()
    print(json.dumps(calc.get_activites_for_date(datetime.date.today()), indent=2))

