from mongoengine import connect,disconnect
from ..settings import settings


async def connect_to_mongo():
    connect(
        host=settings.MONGODB_URL,
        # name="BookRecommendation",
        tls=True,
        tlsCAFile=settings.APPLICATION_CERTIFICATE,
    )

    print("Connection to MongoDB established.")



async def disconnect_from_mongo():  
    disconnect()
    print("Connection to MongoDB closed.")