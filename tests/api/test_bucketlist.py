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
        self.assertEqual(output['message'], "Authentication Error.")

    def test_access_resource_with_invalid_token(self):
        """
        Tests that accessing API resource with invalid token returns error
        """
        # try getting a bucketlist with no invalid token
        response = self.client.get(
            url_for("api.get_bucketlist", bucketlist_id=1),
            headers=self.get_api_headers(self.get_invalid_token(), ''),
        )

        self.assertEqual(response.status_code, 401)

        output = json.loads(response.data)
        self.assertEqual(output['message'], "Authentication Error.")

    def test_unauthorized_access_resource(self):
        """ Test that users CAN view other's bucketlist but CANNOT,
        change another user's bucket list
        It Attempts to change username=test's bucket list
        Remember bucketlist_id=2 belongs to username = test.
        trying to access user 2's bucketlist while logged in as user 1
        """

        # trying to view user 2's bucketlist
        response = self.client.get(
            url_for('api.get_bucketlist', bucketlist_id=3),
            headers=self.get_api_headers(self.get_token(), ''),
        )
        self.assertEqual(response.status_code, 200)

        # try to update data
        data = {
            "title": "Coup D'etat",
            "description": "I'm here to Destroy your Bucketlist",
        }

        response = self.client.put(
            url_for('api.edit_bucketlist', bucketlist_id=3),
            data=json.dumps(data),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 403)
        output = json.loads(response.data)
        self.assertEqual(output['message'], 'Access to resource forbidden.')

        # try do delete bucketlist
        response = self.client.delete(
            url_for("api.delete_bucketlist", bucketlist_id=3),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 403)
        output = json.loads(response.data)
        self.assertEqual(output['message'], 'Access to resource forbidden.')

    def test_get_bucketlist(self):
        response = self.client.get(
            url_for('api.get_bucketlist', bucketlist_id=1),
            headers=self.get_api_headers(self.get_token(), ''),
        )
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.data)
        self.assertEqual(output['title'], 'Food')

    def test_get_bucketlists(self):
        """Tests API returns a list of all bucketlists"""
        response = self.client.get(
            url_for('api.get_bucketlists'),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 200)

        output = json.loads(response.data)
        bucketlist1 = output[0]
        bucketlist2 = output[1]

        # assert Both bucket lists are returned
        self.assertEqual(bucketlist1['title'], "Food")
        self.assertEqual(bucketlist2['title'], "To Learn")

    def test_search_for_bucketlists(self):
        """
        tests that API can be searched to get a bucket list based on the name.
        """
        response = self.client.get(
            url_for('api.get_bucketlists', q="food"),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 200)

        output = json.loads(response.data)
        food_bucketlist = output[0]

        # assert Food bucket list is returned
        self.assertEqual(food_bucketlist['title'], "Food")

    def test_bucketlists_pagination(self):
        """
        tests the implementation of Pagination on the API where,
        a user can specify the number of results they would like to have via
        a GET parameter limit.
        """
        response = self.client.get(
            url_for('api.get_bucketlists', limit=1),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 200)

        output = json.loads(response.data)
        # assert number of bucket lists returned is 1
        self.assertEqual(len(output), 1)

    def test_add_bucketlist_with_incomplete_details(self):
        """ tests that API cannot add bucketlist with incomplete details"""
        new_bucketlist = {
            "title": "",
            "description": "Stuff to try out with HTML/CSS"
        }
        response = self.client.post(
            url_for("api.new_bucketlist"),
            data=json.dumps(new_bucketlist),
            headers=self.get_api_headers(self.get_token(), ''),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)  # bad request
        output = json.loads(response.data)
        self.assertIn(b'error', output)

    def test_add_bucketlist(self):
        new_bucketlist = {
            "title": "Web Design Stuff",
            "description": "Stuff to try out with HTML/CSS",
        }

        response = self.client.post(
            url_for('api.new_bucketlist'),
            data=json.dumps(new_bucketlist),
            headers=self.get_api_headers(self.get_token(), ''),
            content_type='application/json'
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
            url_for('api.edit_bucketlist', bucketlist_id=2),
            data=json.dumps(updated_bucketlist),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertEqual(output['message'], "Bucketlist updated successfully.")

        # Ensure updated data reflects
        response = self.client.get(
            url_for('api.get_bucketlist', bucketlist_id=2),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        # assert the updated description reflects
        self.assertEqual(output['description'], "Never stop learning.")

    def test_delete_bucketlist(self):
        """ Test deleting of items from bucket list"""
        response = self.client.delete(
            url_for("api.delete_bucketlist", bucketlist_id=2),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 204)
