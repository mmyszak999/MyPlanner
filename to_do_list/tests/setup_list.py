from to_do_list.models import List
from to_do_list.tests.setup_login import TestLoginSetUp


class TestListSetUp(TestLoginSetUp):
    def setUp(self):
        self.lists = List.objects.bulk_create([
            List(title="shopping_list", owner=self.test_user),
            List(title="business_objectives", owner=self.super_user),
            List(title="black_list", owner=self.super_user),
            List(title="job_tasks", owner=self.test_user),
            List(title="weekly_goals", owner=self.test_user)
        ])
        return super().setUp()