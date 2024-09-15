from core.tests import BaseTestCase


class GroupTestCase(BaseTestCase):

    def test_join_group(self):
        self.authenticate_user_2()
        self.join_group(self.user_2, self.group)

    def test_leave_group(self):
        pass
