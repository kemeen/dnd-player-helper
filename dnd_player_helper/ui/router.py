from typing import Callable, Any
import flet as ft
from enum import Enum


class DataStrategyEnum(Enum):
    QUERY = 0
    ROUTER_DATA = 1
    CLIENT_STORAGE = 2
    STATE = 3


class Router:
    def __init__(self, data_strategy=DataStrategyEnum.QUERY):
        self.data_strategy = data_strategy
        self.data = dict()
        self.routes = dict()
        self.body = ft.Container()

    def set_route(self, stub: str, view: Callable, label: str, icon):
        self.routes[stub] = (view, label, icon)

    def set_routes(self, route_dictionary: dict):
        """Sets multiple routes at once. Ex: {"/": IndexView }"""
        self.routes.update(route_dictionary)
        for r, v in self.routes.items():
            print(r, v)

    def route_change(self, route):
        print("ROTE CHANGE EVENT")
        _page = route.route.split("?")[0]
        queries = route.route.split("?")[1:]
        print(_page)
        print(queries)
        print(self.routes)

        for item in queries:
            key = item.split("=")[0]
            value = item.split("=")[1]
            self.data[key] = value.replace("+", " ")

        self.body.content = self.routes[_page][0]
        self.body.update()

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key)

    def get_query(self, key):
        return self.data.get(key)
