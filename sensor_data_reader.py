import os, datetime, time
from configparser import ConfigParser
from pathlib import Path
from sensor import Sensor
import smtplib, ssl
from email.message import EmailMessage


class SensorDataReader:
    def __init__(self, config_file="config.ini"):
        self._read_config_file(config_file)
        self._sensors = [Sensor(d) for d in self._sensors_details]

    def _read_config_file(self, config_file):
        cp = ConfigParser()
        cp.read(config_file)
        self._sensors_details = [
            {"ip": i[0], "name": i[1]} for i in cp["sensors"].items()
        ]
        self._sample_interval = cp.getint("settings", "sensor read interval")
        self._data_file_location = cp.get("settings", "data file location")
        self._timeout_value = cp.getint("settings", "warning timeout")

    def _get_today(self):
        return datetime.date.today().strftime("%Y%m%d")

    def _make_dir_if_needed(self, filename):
        directory, _ = os.path.split(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _generate_todays_filename(self):
        return self._data_file_location + os.sep + self._get_today() + "_sensors.csv"

    def _make_todays_csv_file_if_necessary(self):
        filename = self._generate_todays_filename()
        if not Path(filename).is_file():
            first_line_in_file = (
                "ip,name,Time,Temperature,Relative humidity,Dew point,CO2 level\n"
            )
            self._make_dir_if_needed(filename)
            with open(filename, "w") as f:
                f.write(first_line_in_file)
        return filename

    def _start_sensors(self):
        for sensor in self._sensors:
            sensor.start_data_collection(self._sample_interval)

    def _check_sensor_status(self, sensor):
        if sensor.seconds_since_successful_read > self._timeout_value:
            print(
                "{} (ip: {}) hasn't been read for {} seconds".format(
                    sensor.name, sensor.ip, sensor.seconds_since_successful_read
                )
            )
        else:
            print(
                "{} (ip: {}) read {} seconds ago".format(
                    sensor.name, sensor.ip, sensor.seconds_since_successful_read
                )
            )

    def start(self):
        self._start_sensors()
        while True:
            csv_file = self._make_todays_csv_file_if_necessary()
            with open(csv_file, "a") as f:
                for s in self._sensors:
                    f.write(s.ip + "," + s.name + "," + s.latest_csv_data)
                    self._check_sensor_status(s)
            time.sleep(self._sample_interval)


if __name__ == "__main__":
    sdr = SensorDataReader("config.ini")
    sdr.start()

