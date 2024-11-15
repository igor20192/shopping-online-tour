import requests
from rest_framework.views import APIView
from rest_framework.response import Response
import environ


class NovaPoshtaAPIBase(APIView):
    """
    Base class for interacting with the Nova Poshta API.

    Attributes:
    - `env`: Object for working with the environment, used for reading the .env file.
    - `api_key`: API key for authenticating requests to the Nova Poshta API.
    - `url`: URL for making requests to the Nova Poshta API.

    Methods:
    - `make_request(payload)`: Sends a POST request to the API with the given payload and processes the response.

    Example usage:
    ```python
    class MyAPI(NovaPoshtaAPIBase):
        def my_method(self):
            payload = {"apiKey": self.api_key, ...}
            result = self.make_request(payload)
            # ... further processing of the result
    ```

    Note: To use this class, replace the value of `NOVA_POSHTA_API_KEY` with your own API key in the .env file.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = environ.Env()
        self.env.read_env()

        # Replace with your API key
        self.api_key = self.env("NOVA_POSHTA_API_KEY")
        self.url = "https://api.novaposhta.ua/v2.0/json/"

    def make_request(self, payload):
        """
        Sends a POST request to the Nova Poshta API with the given payload.

        Args:
        - `payload`: Dictionary containing request parameters.

        Returns:
        Dictionary with the results of the request or a dictionary with the key "error" if an error occurs.

        Example usage:
        ```python
        result = self.make_request({"apiKey": self.api_key, ...})
        # ... further processing of the result
        ```
        """
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()  # Raises an exception in case of an error
            return response.json()
        except requests.exceptions.RequestException as e:
            # Handling request errors
            return {"error": str(e)}


class NovaPoshtaWarehousesAPIView(NovaPoshtaAPIBase):
    """
    Class for handling requests to the Nova Poshta API to get warehouses for a specific city.

    Methods:
    - `get(request, *args, **kwargs)`: Processes a GET request and returns a list of warehouses in the specified city.
    """

    def get(self, request, *args, **kwargs):
        """
        Processes a GET request and returns a list of warehouses in the specified city.

        Args:
        - `request`: Django request object.
        - `kwargs`: Additional parameters passed in the URL.

        Returns:
        Response object with data about the warehouses in the specified city.

        Example usage:
        ```python
        class MyView(NovaPoshtaWarehousesAPIView):
            def my_method(self, request):
                result = self.get(request, city="Kyiv")
                # ... further processing of the result
        ```
        """
        city = kwargs.get("city")

        # Example request to get warehouses for a city
        payload = {
            "apiKey": self.api_key,
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {"CityName": city},
        }

        warehouses = self.make_request(payload)
        return Response({"warehouses": warehouses})


class NovaPoshtaCityAPIView(NovaPoshtaAPIBase):
    """
    Class for handling requests to the Nova Poshta API to get a list of cities.

    Methods:
    - `get(request, *args, **kwargs)`: Processes a GET request and returns a list of cities.
    """

    def get(self, request, *args, **kwargs):
        """
        Processes a GET request and returns a list of cities.

        Args:
        - `request`: Django request object.
        - `kwargs`: Additional parameters passed in the URL.

        Returns:
        Response object with data about the cities.

        Example usage:
        ```python
        class MyView(NovaPoshtaCityAPIView):
            def my_method(self, request):
                result = self.get(request)
                # ... further processing of the result
        ```
        """
        # Request to get a list of cities
        payload = {
            "apiKey": self.api_key,
            "modelName": "Address",
            "calledMethod": "getCities",
        }

        cities = self.make_request(payload).get("data", [])
        city_names = [city["Description"] for city in cities]
        return Response({"cities": city_names})
