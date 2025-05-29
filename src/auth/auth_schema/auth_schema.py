from pydantic import BaseModel, EmailStr, constr

class userSignup(BaseModel):
    name : str
    phone : str
    email : EmailStr
    status : bool
    role : str
    password : constr(min_length=6) # type: ignore
    confirm_password: constr(min_length=6) # type: ignore
    