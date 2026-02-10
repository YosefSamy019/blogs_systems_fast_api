from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class Hash:
    def bcrypt(self, password: str):
        hashed = pwd_context.hash(password[:72])
        return hashed

    def verify(self, password: str, hashed: str):
        return pwd_context.verify(password[:72], hashed)
