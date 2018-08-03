import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        # with self.client as c:
        #     with c.session_transaction() as session:
        #         session['RSVP'] = False

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        result = self.client.get("/")
        self.assertIn(b"Please RSVP", result.data)
        self.assertNotIn(b"Party Details", result.data)
        # print("FIXME")

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        
        # Test that session was updated
        # with self.client as c:
        #     with c.session_transaction() as session:
        #         print(session['RSVP'])

        self.assertNotIn(b"Please RSVP", result.data)
        self.assertIn(b"Party Details", result.data)
        # print("FIXME")


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        with self.client as c:
            with c.session_transaction() as session:
                session['RSVP'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        # FIXME: test that the games page displays the game from example_data()
        result = self.client.get("/games")

        self.assertIn(b"Clue", result.data)
        self.assertIn(b"Solve a mystery", result.data)



        # print("FIXME")


if __name__ == "__main__":
    unittest.main()
