from fastapi import FastAPI
app = FastAPI(
    title="Ubooking",
    description="API para la administracion de salones de la universidad del magdalena",
    openapi_tags=[
        {
        "name": "users",
        "description": "Operations with users"
        },
        {
        "name": "courses",
        "description": "Operations with products",
        },
        {
        "name": "edificios",
        "description": "orders operation"
        },
        {
        "name": "orders",
        "description": "obtain order details by order id"
        },
        {
        "name": "login",
        "description": "login authentication"
        }
        ]
)