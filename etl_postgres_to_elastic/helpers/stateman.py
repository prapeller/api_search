import datetime
import logging
from typing import AnyStr


class StateManager:
    def __init__(self, state_file: AnyStr):
        """
        :param state_file: file where state will be saved
        """
        self.state_file = state_file
        self.default = datetime.datetime(1970, 1, 1)
        self.state = self.load_state()

    def load_state(self):
        """
        :return: datetime loaded from file. If file not exist, create it with default datetime
        """
        try:
            with open(self.state_file, 'r') as f:
                state = f.read()
                if state:
                    a = state.strip()
                    logging.log(logging.INFO, f"loaded:  {datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')}")
                    self.state = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
                    return self.state
                else:
                    return self.default.strftime('%Y-%m-%d %H:%M:%S')
        except FileNotFoundError:
            return self.default

    def save_state(self):
        """
        save current time to file
        :return:
        """
        with open(self.state_file, 'w') as f:
            logging.log(logging.INFO, f"saved:  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))