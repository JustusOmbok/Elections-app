import sys
import unittest
print(sys.path)
import os
os.chdir('..')
from app import app, db
from app.models import Admin, President, Governor, Voter, Vote_president, Vote_governor
sys.path.insert(0, '/home/ombok/Elections-app')

class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use an in-memory SQLite database for testing
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Scenario 1: Authenticated access
    def test_admin_dashboard_authenticated(self):
        with self.client.session_transaction() as sess:
            sess['admin_logged_in'] = True
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_unauthenticated(self):
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirects to admin login page

    def test_voting_president_unauthenticated(self):
        response = self.client.get('/vote/president')
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    # Scenario 3: Error handling
    def test_delete_president_nonexistent(self):
        response = self.client.post('/admin/delete_president', data={'name': 'Nonexistent', 'party_name': 'Unknown'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"President does not exist.", response.data)

    # Scenario 2: Unauthenticated access
    def test_voting_president_unauthenticated(self):
        response = self.client.get('/vote/president')
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_voting_governor_unauthenticated(self):
        response = self.client.get('/vote/governor')
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    # Scenario 3: Error handling
    def test_delete_president_nonexistent(self):
        response = self.client.post('/admin/delete_president', data={'name': 'Nonexistent', 'party_name': 'Unknown'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"President does not exist.", response.data)

    def test_check_vote_invalid_voter(self):
        response = self.client.get('/check_vote')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"false", response.data)

    def test_voting_president_unauthenticated(self):
        response = self.client.get('/vote/president')
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_voting_governor_unauthenticated(self):
        response = self.client.get('/vote/governor')
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    # Scenario 3: Error handling
    def test_delete_president_nonexistent(self):
        response = self.client.post('/admin/delete_president', data={'name': 'Nonexistent', 'party_name': 'Unknown'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"President does not exist.", response.data)

    def test_check_vote_invalid_voter(self):
        response = self.client.get('/check_vote')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"false", response.data)

    # Scenario 4: Successful operation
    def test_register_voter_success(self):
        data = {'national_id': '1234567890', 'county': 'Test County', 'name': 'Test Voter'}
        response = self.client.post('/voter/register', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)  # Check if redirected to login page after successful registration

    # Scenario 5: Form submission
    def test_admin_login_submit_valid_credentials(self):
        with app.app_context():
            admin = Admin(work_id='123', station='Test Station', name='Admin', phone_number='1234567890', email='admin@test.com')
            db.session.add(admin)
            db.session.commit()

        data = {'station': 'Test Station', 'work_id': '123'}
        response = self.client.post('/admin/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)  # Check if redirected to admin dashboard after successful login

    # Add more tests for each route, covering different scenarios

if __name__ == '__main__':
    unittest.main()