from typing import List, Optional

from .base import BaseApi


class OrdersApi(BaseApi):
    ORDERS = "/api/orders"

    def create_order(self, ingredient_ids: List[str], token: Optional[str] = None):
        return self.request("POST", self.ORDERS, json={"ingredients": ingredient_ids}, token=token)
