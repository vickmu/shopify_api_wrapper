from typing import List, Any, Optional
from ..client import ShopifyClient
from requests import Response

class Inventory:
    
    def __init__(self, shopify_client: ShopifyClient): 
        self.client = shopify_client
    
    def _validate_quantities_list(self, set_quantities_list: List[Any]):
        if not isinstance(set_quantities_list, list):
            raise ValueError("set_quantities_list must be a list type")
    
    def _validate_reason(self, reason: str):
        if not isinstance(reason, str):
            raise ValueError("reason must be a string type")

    def update_quantities(self, reason: str, set_quantities_list: List[Any], api_version: Optional[str] = None) -> Response:
        
        self._validate_reason(reason)
        self._validate_quantities_list(set_quantities_list)

        api_version = api_version or self.client.api_version
        
        mutation = """
            mutation inventorySetOnHandQuantities($input: InventorySetOnHandQuantitiesInput!) {
                inventorySetOnHandQuantities(input: $input) {
                    userErrors {
                        field
                        message
                    }
                }
            }
        """
        
        payload = {
            "query": mutation,
            "variables": {
                "input": {
                    "reason": reason,
                    "setQuantities": set_quantities_list,
                }
            }
        }
        
        return self.client.graphql.post(data=payload, version=api_version)