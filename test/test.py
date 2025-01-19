import unittest
import requests

BASE_URL = "http://localhost:5123"

class TestAPI(unittest.TestCase):

    # Helper functions
    def login(self):
        response = requests.post(f"{BASE_URL}/login", json={
            "email": "test_user@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        return response.json().get("jwt")

    def test_login(self):
        response = requests.post(f"{BASE_URL}/login", json={
            "email": "test_user@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("jwt", response.json())

    def test_reset_password(self):
        response = requests.post(f"{BASE_URL}/login/resetpassword", json={
            "email": "test_user@example.com",
            "password": "newpassword123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_get_user(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.get(f"{BASE_URL}/users/user123", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.json())

    def test_add_user(self):
        response = requests.post(f"{BASE_URL}/users/add", json={
            "user": {
                "uid": "user123",
                "name": "John Doe",
                "email": "johndoe@example.com",
                "password": "password123",
                "cat": "USER",
                "credit": 0
            }
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_update_user(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.patch(f"{BASE_URL}/users/update", json={
            "user": {
                "uid": "user123",
                "name": "John Updated",
                "email": "johnupdated@example.com",
                "credit": 100
            }
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_suspend_user(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.patch(f"{BASE_URL}/users/suspend", json={"uid": "user123"}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_delete_user(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.delete(f"{BASE_URL}/users/delete", json={"uid": "user123"}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_get_all_items(self):
        response = requests.get(f"{BASE_URL}/items/all")
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.json())

    def test_get_item(self):
        response = requests.get(f"{BASE_URL}/items/item123")
        self.assertEqual(response.status_code, 200)
        self.assertIn("item", response.json())

    def test_add_item(self):
        response = requests.post(f"{BASE_URL}/items/create", json={
            "item": {
                "name": "Test Item",
                "stock": 10,
                "price": 5
            }
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_update_item(self):
        response = requests.patch(f"{BASE_URL}/items/update", json={
            "item": {
                "id": "item123",
                "stock": 15,
                "price": 6
            }
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_delete_item(self):
        response = requests.delete(f"{BASE_URL}/items/delete", json={"id": "item123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_buy_item(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.post(f"{BASE_URL}/items/buy", json={
            "id": "item123",
            "quantity": 2,
            "uid": "user123"
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_preorder_item(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.post(f"{BASE_URL}/items/preorder", json={
            "id": "item123",
            "quantity": 3,
            "uid": "user123"
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_get_all_tasks(self):
        response = requests.get(f"{BASE_URL}/tasks/all")
        self.assertEqual(response.status_code, 200)
        self.assertIn("tasks", response.json())

    def test_create_task(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.post(f"{BASE_URL}/tasks/create", json={
            "task": {
                "name": "New Task",
                "reward": 10,
                "deadline": "2025-02-01T00:00:00Z"
            }
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_update_task(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.patch(f"{BASE_URL}/tasks/update", json={
            "task": {
                "id": "task123",
                "reward": 20
            }
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_delete_task(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.delete(f"{BASE_URL}/tasks/delete", json={"id": "task123"}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_apply_task(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.post(f"{BASE_URL}/tasks/apply", json={
            "id": "task123",
            "uid": "user123"
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_cancel_task_application(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.post(f"{BASE_URL}/tasks/cancel", json={
            "id": "usertask456"
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_get_all_transactions(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.get(f"{BASE_URL}/transactions/all", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("transactions", response.json())

    def test_get_transaction_by_id(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.post(f"{BASE_URL}/transactions/transaction123", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("transaction", response.json())

    def test_get_transactions_by_user(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.post(f"{BASE_URL}/transactions/users/user123", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("transactions", response.json())

    def test_get_all_usertasks(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.get(f"{BASE_URL}/usertasks/all", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("usertask", response.json())

    def test_update_usertask(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.patch(f"{BASE_URL}/usertasks/update", json={
            "usertask": {
                "id": "usertask123",
                "status": "COMPLETED"
            }
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_delete_usertask(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.delete(f"{BASE_URL}/usertasks/delete", json={"id": "usertask123"}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_get_all_itemrequests(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.get(f"{BASE_URL}/itemrequests/all", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("itemrequests", response.json())

    def test_create_itemrequest(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.post(f"{BASE_URL}/itemrequests/create", json={
            "itemrequest": {
                "description": "New item request"
            }
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_update_itemrequest(self):
        jwt = self.login()
        headers = {"Authorization": f"Bearer {jwt}"}
        response = requests.patch(f"{BASE_URL}/itemrequests/update", json={
            "itemrequest": {
                "id": "itemrequest123",
                "description": "Updated item request"
            }
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

if __name__ == "__main__":
    unittest.main()
