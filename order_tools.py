ORDERS = {"A100": "shipped", "A200": "processing"}


def get_order_status(order_id: str) -> str:
    return ORDERS.get(order_id, "not found")


TOOLS = [
    {
        "name": "get_order_status",
        "description": "Look up the current status of a customer order by its order ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID, for example A100"},
            },
            "required": ["order_id"],
        },
    }
]