from fastapi.responses import JSONResponse


class CustomResponse(JSONResponse):
    def __init__(self, message: str,  status_code: int=200, status: bool = True, data=None):

        response = {"status": status, "message": message, "data": data}

        super().__init__(status_code=status_code, content=response)
