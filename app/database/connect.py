from mongoengine import connect, disconnect
from ..settings import settings


async def connect_to_mongo():
    connect(
        host=settings.MONGODB_URL,
        name="BookRecommendation",
        tls=True if not settings.DEV else False,
        tlsCAFile=settings.APPLICATION_CERTIFICATE if not settings.DEV else None,
    )

    print("Connection to MongoDB established.")


async def disconnect_from_mongo():
    disconnect()
    print("Connection to MongoDB closed.")
