from typing import Any, List, Optional
from requests import Response

class Collection:
    def __init__(self, shopify_client) -> None:
        self.client = shopify_client
    
    def list(self, first: int = 250, after: Optional[str] = None) -> Response:
        query = """
        query getCollections($first: Int!, $after: String) {
            collections(first: $first, after: $after) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                edges {
                    cursor
                    node {
                        id
                        title
                        handle                
                    }
                }
            }
        }
        """
        variables = {"first": first, "after": after}
        payload = {
            "query": query,
            "variables": variables
        }
        return self.client.graphql.post(payload)
    
    def create(self, title: str, description: str, seo_title: str, seo_description: str, publication_ids: List[str]) -> Response:
        mutation = """
        mutation collectionCreate($input: CollectionInput!) {
            collectionCreate(input: $input) {
                collection {
                    title
                    description
                    seo {
                        title
                        description
                    }
                }
                userErrors {
                field
                message
                }
            }
        }
        """
        
        variables = {
            "input": {
                "title": title, 
                "descriptionHtml": description, 
                "seo": {
                    "title": seo_title, 
                    "description": seo_description
                }, 
                "publications": [
                    {'publicationId': pid} for pid in publication_ids
                ]
            }
        }
        
        payload = {
            "query": mutation,
            "variables": variables
        }
        return self.client.graphql.post(payload)
    
    def publish(self, collection_id: str, publication_ids: List[str]) -> Response:
        mutation = """
        mutation publishablePublish($id: ID!, $input: [PublicationInput!]!) {
            publishablePublish(id: $id, input: $input) {
               userErrors {
                    field
                    message
                }
            }
        }
        """
        
        variables = {
            "id": collection_id, 
            "input": [
                {'publicationId': pid} for pid in publication_ids
            ]
        }
        
        payload = {
            "query": mutation,
            "variables": variables
        }
        return self.client.graphql.post(payload)
