import json
from flask import url_for
from base import BaseTestCase


class BucketListTestCase(BaseTestCase):
    """ Test Bucketlist API Operations """

    def test_access_resource_without_token(self):
        """Tests that accessing API resource with no token returns error"""
        # try getting a bucketlist with no access token
        response = self.client.get(
            url_for("api.get_bucketlist", bucketlist_id=1),
        )

        self.assertEqual(response.status_code, 401)

        output = json.loads(response.data)
        self.assertEqual(output['error'], "Token not present.")

    def test_access_resource_with_invalid_token(self):
        """
        Tests that accessing API resource with invalid token returns error
        """
        # try getting a bucketlist with no invalid token
        response = self.client.get(
            url_for("api.get_bucketlist", bucketlist_id=1),
            headers=self.get_invalid_token()
        )

        self.assertEqual(response.status_code, 401)

        output = json.loads(response.data)
        self.assertEqual(output['error'], "Invalid Token.")

    def test_unauthorized_access_resource(self):
        """ Test that users cannot access another user's bucketlists."""

        # trying to access user2's bucketlist with user1
        response = self.client.get(
            url_for('api.get_bucketlist', bucketlist_id=2),
            headers=self.get_token()
        )
        self.assertEqual(response.status_code,  403)
        output = json.loads(response.data)
        self.assertEqual(output['error'], 'Access to resource forbidden.')

    def test_get_bucketlist(self):
        response = self.client.get(
            url_for('api.get_bucketlist', bucketlist_id=1),
            headers=self.get_token()
        )
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.data)
        self.assertEqual(output['title'], 'Food')

    def test_get_bucketlists(self):
        """Tests API returns a list of all bucketlists"""
        response = self.client.get(
            url_for('api.get_bucketlists'),
            headers=self.get_token()
        )

        self.assertEqual(response.status_code, 200)

        output = json.loads(response.data)
        bucketlist1 = output[0]
        bucketlist2 = output[1]

        # assert Both bucket lists are returned
        self.assertEqual(bucketlist1['title'], "Food")
        self.assertEqual(bucketlist2['title'], "To Learn")

    def test_add_bucketlist_with_incomplete_details(self):
        """ tests that API cannot add bucketlist with incomplete details"""
        new_bucketlist = {
            "title": "",
            "description": "Stuff to try out with HTML/CSS"
        }
        response = self.client.post(url_for("api.get_bucketlists"),
                                    data=new_bucketlist,
                                    headers=self.get_token())
        self.assertEqual(response.status_code, 400)  # bad request
        output = json.loads(response.data)
        self.assertIn(b'error', output)

    def test_add_bucketlist(self):
        new_bucketlist = {
            "title": "Web Design Stuff",
            "description": "Stuff to try out with HTML/CSS"
        }

        response = self.client.post(
            url_for('api.get_bucketlists'),
            data=new_bucketlist,
            headers=self.get_token()
        )

        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output['message'], "Bucketlist created successfully.")

    def test_update_bucketlist(self):
        updated_bucketlist = {
            "title": "To Learn",
            "description": "Never stop learning."
        }
        # update item
        response = self.client.put(
            url_for('api.get_bucketlist', bucketlist_id=2),
            data=updated_bucketlist,
            headers=self.get_token()
        )

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertEqual(output['message'], "Bucketlist updated successfully.")

        # Ensure updated data reflects
        response = self.client.get(
            url_for('api.get_bucketlist', bucketlist_id=2),
            headers=self.get_token()
        )

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        # assert the updated description reflects
        self.assertEqual(output['description'], "Never stop learning.")

    def test_delete_bucketlist(self):
        """ Test deleting of items from bucket list"""
        response = self.client.delete(
            url_for("api.get_bucketlist", bucketlist_id=2),
            headers=self.get_token()
        )

        self.assertEqual(response.status_code, 204)
