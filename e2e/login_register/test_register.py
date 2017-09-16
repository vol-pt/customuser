from ..base import FunctionalTest


class UserRegisterTest(FunctionalTest):
    def test_whole(self):
        self.log_in_user('kamil@wp.pl', 'zaqmko123321')
