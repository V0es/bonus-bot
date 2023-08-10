import unittest


class TestDatabase(unittest.TestCase):

    @staticmethod
    def _create_db():
        
        usr = User(user_id=123124, fullname='Test Test', phone_number='123123', email='mmm@gmail.com', bonus_points=0)
        return db, usr

    def test_add_user(self):
        db, usr = self._create_db()
        db.add_user(usr)
        self.assertEqual(usr, db.get_all_users()[0])

    def test_get_all_users(self):
        db, usr = self._create_db()
        db.add_user(usr)
        usr1 = User(user_id=1231124, fullname='Test Tes123t', phone_number='123123123', email='mmm@gm123ail.com', bonus_points=0)
        db.add_user(usr1)
        self.assertEqual(len(db.get_all_users()), 2)

    def test_get_user_by_phone_number(self):
        db, usr = self._create_db()
        db.add_user(usr)
        self.assertIsNone(db.get_user_by_phone_number('321321'))
        self.assertEqual(usr, db.get_user_by_phone_number(usr.phone_number))
    
    def test_add_bonus_points(self):
        db, usr = self._create_db()
        a = 123
        db.add_user(usr)
        db.add_bonus_points(a, usr)
        self.assertEqual(a, db.get_user_by_phone_number(usr.phone_number).bonus_points)

    def test_delete_user(self):
        db, usr = self._create_db()
        db.add_user(usr)
        usr1 = User(user_id=1231124, fullname='Test Tes123t', phone_number='123123123', email='mmm@gm123ail.com', bonus_points=0)
        db.add_user(usr1)
        db.delete_user(usr)
        self.assertEqual(len(db.get_all_users()), 1)
        db.delete_user(usr1)
        self.assertEqual(len(db.get_all_users()), 0)


if __name__ == '__main__':
    unittest.main()
