from flask import Flask
from runescape_step_calculator import RunescapeStepCalculator


if __name__ == "__main__":
    app = Flask(__name__)
    step_calculator = RunescapeStepCalculator()

    @app.route('/steps/<date>')
    def total_steps_on_date(date):
        return step_calculator.get_total_steps_for_date(date)

    @app.route('/activity-steps/<date>')
    def get_date_data(date):
        return step_calculator.get_activity_steps_for_date(date)

    @app.route('/walking-steps/<date>')
    def get_non_activity_steps(date):
        return step_calculator.get_walking_steps_for_date(date)

    @app.route('/allowed-steps/<date>')
    def get_allowed_steps(date):
        return step_calculator.get_allowed_runescape_steps_for_date(date)

    @app.route('/ratio/walk')
    def get_walking_ratio():
        return step_calculator.get_walking_step_ratio()

    @app.route('/ratio/run')
    def get_running_ratio():
        return step_calculator.get_running_step_ratio()

    app.run()
