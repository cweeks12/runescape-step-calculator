import garminconnect
import datetime


class RunescapeStepCalculator:
    def __init__(self, credential_path=None):
        if credential_path is None:
            credential_path = '~/.garth'

        self.garmin = garminconnect.Garmin()
        self.garmin.login(credential_path)

    def get_total_steps_for_date(self, date: datetime.date) -> int:
        """
        Gets the number of steps taken on a given date
        :param date: The date you want to know your step count on
        :return: The total step count
        """
        # This returns an array of length 1, so we need to pull the
        return self.garmin.get_daily_steps(date, date)[0]['totalSteps']

    def get_activity_steps_for_date(self, date: datetime.date) -> int:
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
        return total_steps

    def get_walking_steps_for_date(self, date: datetime.date) -> int:
        """
        Calculates non-running steps for a given date. This assumes that all running happened in an activity.
        :param date: The date you want to know your non-activity step count on
        :return: The total non-activity steps
        """
        return self.get_total_steps_for_date(date) - self.get_activity_steps_for_date(date)

    def get_allowed_runescape_steps_for_date(self, date: datetime.date, walking_ratio=5, running_ratio=1) -> int:
        """
        Calculates how many steps are allowed for a certain day in RuneScape given the ratios of real steps to RuneScape
        steps.
        :param date: The date you want to know allowed steps for
        :param walking_ratio: Number of real walking steps you have to take for 1 step in RuneScape
        :param running_ratio: Number of real running steps you have to take for 1 step in RuneScape
        :return: Total allowed RuneScape steps
        """
        walking_steps = self.get_walking_steps_for_date(date) // walking_ratio
        running_steps = self.get_activity_steps_for_date(date) // running_ratio
        return walking_steps + running_steps


if __name__ == "__main__":
    step_calculator = RunescapeStepCalculator()

    interesting_date = datetime.date.today() - datetime.timedelta(days=2)
    print(step_calculator.get_activity_steps_for_date(interesting_date))
    print(step_calculator.get_walking_steps_for_date(interesting_date))
    print(step_calculator.get_allowed_runescape_steps_for_date(interesting_date))
