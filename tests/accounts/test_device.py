from core.response import Response
from core.testcase import TestCase
from utils.datautils import search_dict


class DeviceTest(TestCase):
    def setUp(self):
        self.create_user()
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        self.login_device = self.data.get('login_device')

    def test_device_register(self):
        assert not self.login_device.get('is_registered')

        device_id = self.login_device.get('id')
        response = self.post(
            '/api/accounts/device/%d/register/' % device_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.get(
            '/api/accounts/devices/',
            auth=True
        )
        device = search_dict('id', device_id, self.data)
        assert device.get('is_registered')

    def test_device_register_different_device(self):
        device_id = self.login_device.get('id')
        self.client = self.get_client('PC')
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )

        response = self.post(
            '/api/accounts/device/%d/register/' % device_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_400

    def test_device_delete(self):
        device_id = self.login_device.get('id')
        response = self.delete(
            '/api/accounts/device/%d/delete/' % device_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_204

        response = self.get(
            '/api/accounts/devices/',
            auth=True
        )
        assert not self.data

    def test_device_logout(self):
        response = self.post(
            '/api/accounts/logout/',
            auth=True
        )
        assert response.status_code == Response.HTTP_204

        response = self.get(
            '/api/accounts/devices/',
            auth=True
        )
        assert not self.data
