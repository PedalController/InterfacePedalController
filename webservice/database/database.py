from webservice.properties import WSProperties


class UsersDatabase(object):
    """
    Management of username
    """

    def __init__(self, controller):
        """
        :param ComponentDataController controller:
        """
        self._controller = controller

        self._users = self._read_data(controller)

    def _read_data(self, controller):
        if WSProperties.USER not in controller[WSProperties.DATA_KEY]:
            self._save_users({'pedal pi': 'pedal pi'})

        return controller[WSProperties.DATA_KEY][WSProperties.USER]

    def _save_users(self, users):
        data = self._controller[WSProperties.DATA_KEY]
        data[WSProperties.USER] = users
        self._controller[WSProperties.DATA_KEY] = data

    def auth(self, username, password):
        return username in self._users \
           and self._users[username] == password

    def update(self, username, new_password):
        """
        Updates the user password

        :param string username:
        :param string new_password:
        """
        if username in self._users:
            raise KeyError('Username "{}" not registered'.format(username))

        self._users[username] = new_password
        self._save_users(self._users)
