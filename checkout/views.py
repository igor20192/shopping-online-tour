from django.shortcuts import render

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from pathlib import Path
import environ
import os


class NovaPoshtaWarehousesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        city = kwargs.get("city")
        env = environ.Env()
        BASE_DIR = Path(__file__).resolve().parent.parent

        environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

        # ВАШ_КЛЮЧ_API - замените на ваш ключ API
        api_key = env("NOVA_POSHTA_API_KEY")
        url = "https://api.novaposhta.ua/v2.0/json/"

        # Пример запроса на получение отделений по городу
        payload = {
            "apiKey": api_key,
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {"CityName": city},
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Поднимает исключение в случае ошибки
            warehouses = response.json()
            return Response({"warehouses": warehouses})
        except requests.exceptions.RequestException as e:
            # Обработка ошибок запроса
            return Response({"error": str(e)}, status=500)


class NovaPoshtaCityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        env = environ.Env()
        BASE_DIR = Path(__file__).resolve().parent.parent

        environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

        # ВАШ_КЛЮЧ_API - замените на ваш ключ API
        api_key = env("NOVA_POSHTA_API_KEY")
        url = "https://api.novaposhta.ua/v2.0/json/"

        payload = {
            "apiKey": api_key,
            "modelName": "Address",
            "calledMethod": "getCities",
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Поднимает исключение в случае ошибки
            cities = response.json().get("data", [])
            city_names = [city["Description"] for city in cities]
            return Response({"cities": city_names})
        except requests.exceptions.RequestException as e:
            # Обработка ошибок запроса
            return Response({"error": str(e)}, status=500)
