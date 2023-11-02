class NoCacheDataError(Exception):
    def __init__(self, message='No cache data available.'):
        self.message = message
        super().__init__(self.message)


class NoDataError(Exception):
    def __init__(self, message='No data available.'):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self, message='User not found.'):
        self.message = message
        super().__init__(self.message)


class ProfileError(Exception):
    def __init__(self, message='Profile error.'):
        self.message = message
        super().__init__(self.message)