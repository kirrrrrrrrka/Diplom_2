from .base import BaseApi


class IngredientsApi(BaseApi):
    INGREDIENTS = "/api/ingredients"

    def get_ingredients(self):
        return self.request("GET", self.INGREDIENTS)
