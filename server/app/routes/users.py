from fastapi import APIRouter,Response,status,Cookie
from typing import Annotated
from ..lib.models import UserRequest
from ..lib.crud import create_user
import bcrypt
from ..lib.auth import create_session,verify_jwt,delete_refresh_token_from_db

userRouter = APIRouter(prefix="/api/users")

@userRouter.post("/signup")
async def signup(response: Response,user: UserRequest):
    bytes = user.password.encode('utf-8')
    hashedPassword = bcrypt.hashpw(bytes,bcrypt.gensalt()).decode('utf-8')
    user.password = hashedPassword
    user_id = await create_user(user=user)
    print("User created: ",user_id)

    access_token = await create_session(user_id)

    response.set_cookie(key="access_token",value=str(access_token))
    response.status_code = status.HTTP_201_CREATED
    return {
        "message": "User signed in successfully",
        "success": True
    }

@userRouter.post("/logout")
async def logout(response: Response,access_token: Annotated[str | None,Cookie()] = None):
    try:
        if access_token is None:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {
                "message": "User is already logged out"
            }
        user_id = verify_jwt(access_token)
        deletion = await delete_refresh_token_from_db(user_id)
        response.set_cookie(key="access_token",value="")
        
        response.status_code = status.HTTP_200_OK
        return {
            "message": "User logged out successfully"
        }
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "Error while logging out",
            "error": e
        }
        
    

    



    
