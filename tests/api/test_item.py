from flask import json, url_for
from base import BaseTestCase


class ItemTestCase(BaseTestCase):

    def test_access_resource_without_token(self):
        """Tests that accessing API resource with no token returns error"""
        # try getting an item from a bucketlist with no access token
        response = self.client.get(
            url_for("api.get_bucketlist_item", bucketlist_id=1, item_id=1)
        )

        self.assertEqual(response.status_code, 401)

        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output['message'], "Authentication Error.")

    def test_access_resource_with_invalid_token(self):
        """
        Tests that accessing API resource with invalid token returns error
        """
        item = {
            "title": "Chinese Dishes",
            "description": "Try out Sushi in some fancy chinese restaurant"
        }
        # try getting an item from a bucketlist with no invalid token
        response = self.client.get(
            url_for("api.get_bucketlist_items", bucketlist_id=1),
            data=json.dumps(item),
            headers=self.get_api_headers(self.get_invalid_token(), ''),
        )

        self.assertEqual(response.status_code, 401)

        output = json.loads(response.data)
        self.assertEqual(output['message'], "Authentication Error.")

    def test_unauthorized_change_to_resource(self):
        """ Test that users CAN view other's bucketlist items but CANNOT,
        change another user's bucket list items.
        It Attempts to change username=test's bucket list item
        Remember bucketlist_id=2 belongs to username = test.
        trying to access user 2's bucketlist items while logged in as user 1
        """

        # trying to view user 2's bucketlist items
        response = self.client.get(
            url_for('api.get_bucketlist_item', bucketlist_id=3, item_id=2),
            headers=self.get_api_headers(self.get_token(), ''),
        )
        self.assertEqual(response.status_code, 200)

        # try to update data
        data = {
            "title": "Coup D'etat",
            "description": "I'm here to Destroy your Bucketlist",
            "status": "I'm sooo gonna fail",
        }

        response = self.client.put(
            url_for('api.edit_bucketlist_item', bucketlist_id=3, item_id=2),
            data=json.dumps(data),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 403)
        output = json.loads(response.data)
        self.assertEqual(output['message'], 'Access to resource forbidden.')

        # try do delete item from bucketlist
        response = self.client.delete(
            url_for("api.delete_bucketlist_item", bucketlist_id=3, item_id=2),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 403)
        output = json.loads(response.data)
        self.assertEqual(output['message'], 'Access to resource forbidden.')

    def test_get_item(self):
        """ Test that a specific bucket list item is displayed """
        # Get bucket list item by ID.
        response = self.client.get(
            url_for('api.get_bucketlist_item', bucketlist_id=1, item_id=1),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertEqual(
            output['description'],
            'Tasty spicy and hot indian dishes.'
        )

    def test_add_item_with_incomplete_details(self):
        """
        tests that API cannot add item with incomplete details
        """
        item = {"title": "",
                "description": "Try out Sushi in some fancy chinese restaurant"
                }
        response = self.client.post(
            url_for("api.add_bucketlist_item", bucketlist_id=1),
            data=json.dumps(item),
            headers=self.get_api_headers(self.get_token(), ''),
        )
        self.assertEqual(response.status_code, 400)  # bad request
        output = json.loads(response.data)
        self.assertIn(b'error', output)

    def test_add_item(self):
        """ Test adding items to bucketlist """
        item = {"title": "Chinese Dishes",
                "description": "Try out Sushi in some fancy chinese restaurant"
                }
        response = self.client.post(
            url_for("api.add_bucketlist_item", bucketlist_id=1),
            data=json.dumps(item),
            headers=self.get_api_headers(self.get_token(), ''),
        )
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data)
        self.assertEqual(
            output["message"],
            "Item successfully added in bucketlist."
        )

    def test_update_item(self):
        """ Test edit/update of an item"""
        # updating the description
        item = {
            "title": "Indian Dishes",
            "description": "I'd love to try Indian Dishes."
        }
        response = self.client.put(
            url_for(
                'api.edit_bucketlist_item',
                bucketlist_id=1,
                item_id=1,
            ),
            data=json.dumps(item),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertEqual(output["message"], "Item updated successfully.")

        # Ensure updated data reflects
        response = self.client.get(
            url_for(
                'api.get_bucketlist_item',
                bucketlist_id=1,
                item_id=1
            ),
            headers=self.get_api_headers(self.get_token(), ''),
        )

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        # assert the updated description reflects
        self.assertEqual(
            output['description'],
            "I'd love to try Indian Dishes."
        )

    def test_delete_item(self):
        """ Test deleting of items from bucket list"""
        response = self.client.delete(
            url_for(
                "api.delete_bucketlist_item",
                bucketlist_id=1,
                item_id=1
            ),
            headers=self.get_api_headers(self.get_token(), ''),
        )
        # successful but does not return any content
        self.assertEqual(response.status_code, 204)
