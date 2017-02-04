import unittest
import json
from base64 import b64encode
from flask import url_for
from bucky import create_app, db
from bucky.models import User, BucketList, Item


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.app_context()
        self.context.push()
        db.create_all()

        self.prepare_data()
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        """Destroy test Database"""
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def prepare_data(self):
        """ Prepares test data"""
        users = [
            ('fawazfarid', 'fawwazally@gmail.com', 'fawaz123'),
            ('test', 'test@gmail.com', 'test-password'),
        ]
        for username, email, password in users:
            user = User(username=username, email=email)
            if password:
                user.password = password
            db.session.add(user)

        # add bucketlists
        bucketlist1 = BucketList(
            title="Food",
            description="Resturants i'd like to visit, \
                                     cuisines I would like to try out.",
            created_by=1
        )
        bucketlist2 = BucketList(
            title="To Learn",
            description="Stuff to learn.",
            created_by=1
        )
        # bucketlist created by a different user
        bucketlist3 = BucketList(
            title="Travelling",
            description="Awesome places to visit.",
            created_by=2
        )
        # populate bucketlist with items
        item1 = Item(
            title="Indian Dishes",
            description="Tasty spicy and hot indian dishes.",
            status="pending",
            bucketlist_id=1
        )
        item2 = Item(
            title="Hawaii",
            description="travel to the special island in the USA.",
            status="done",
            bucketlist_id=3
        )

        db.session.bulk_save_objects([
            bucketlist1,
            bucketlist2,
            bucketlist3,
            item1,
            item2,
        ])
        db.session.commit()

    def get_token(self):
        """ Returns authentication token """
        response = self.client.post(
            url_for('api.login'),
            data=json.dumps({
                'email': 'fawwazally@gmail.com',
                'password': 'fawaz123'
            }),
            content_type='application/json'
        )
        output = json.loads(response.data.decode('utf-8'))
        token = output.get("token")
        return token

    def get_api_headers(self, email, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (email + ':' + password).encode('utf-8')).decode('utf-8'),
            'Content-Type': 'application/json'
        }

    def get_invalid_token(self):
        """Returns an invalid token for testing purposes"""
        return 'invalidtok123'
