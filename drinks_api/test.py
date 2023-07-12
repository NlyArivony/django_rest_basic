from django.test import TestCase, Client
from rest_framework import status
from .models import Drink
from .serializers import DrinkSerializer


data = {
    "name": "Test Drink",
    "description": "Test description",
}


class DrinkTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_drink_list(self):
        response = self.client.get("/drinks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        self.assertEqual(response.json(), {"drinks": serializer.data})

    def test_drink_list_post(self):
        response = self.client.post("/drinks/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drink.objects.count(), 1)
        drink = Drink.objects.first()
        serializer = DrinkSerializer(drink)
        self.assertEqual(response.json(), serializer.data)

    def test_drink_detail(self):
        drink = Drink.objects.create(name=data["name"], description=data["description"])
        response = self.client.get(f"/drinks/{drink.pk}")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = DrinkSerializer(drink)
        self.assertEqual(response.json(), serializer.data)

    def test_drink_detail_put(self):
        drink = Drink.objects.create(name=data["name"], description=data["description"])
        data_updated = {
            "name": "Updated Drink",
            "description": "Updated description",
        }
        response = self.client.put(
            f"/drinks/{drink.pk}", data=data_updated, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        drink.refresh_from_db()
        serializer = DrinkSerializer(drink)
        self.assertEqual(response.json(), serializer.data)

    def test_drink_detail_delete(self):
        drink = Drink.objects.create(name=data["name"], description=data["description"])
        response = self.client.delete(f"/drinks/{drink.pk}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Drink.objects.count(), 0)
