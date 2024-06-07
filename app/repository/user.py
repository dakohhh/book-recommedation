from ..database.models import User




class UserRepository:

    @staticmethod
    async def create_user(user):
        query = User(**user.dict())
        query.save()
        return query
    
    @staticmethod
    async def get_user(email):
        query = User.objects(email=email).first()
        return query

    @staticmethod
    async def get_user_by_id(id):
        query = User.objects(id=id).first()
        return query
    
    @staticmethod
    async def update_user(id, user):
        user = User.objects(id=id).update(**user.dict())
        return user
    
    @staticmethod
    async def delete_user(id):
        user = User.objects(id=id).delete()
        return user
    
    @staticmethod
    async def does_email_exist(email):
        query = User.objects(email=email).first()
        return query is not None