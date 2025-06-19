from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Constants.constant import NOT_FOUND, NOT_NULL_ERROR


class ExceptionHandling:
    def not_null_exception(self,message):
        raise HTTPException(status_code=400, detail=NOT_NULL_ERROR.format(string= message))

    def not_found_exception(self):
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    def success(self,message):
        return JSONResponse(content=message, status_code=201)



