from abc import ABC, abstractmethod

import bcrypt
import datetime
import jwt

from pdsecurity.models import ApplicationUser


class Authenticator(ABC):

    @abstractmethod
    def login(self, name, password):
        pass


class BcryptAuthenticator(Authenticator):

    @abstractmethod
    def get_user(self, name):
        pass

    @abstractmethod
    def generate_security_token(self, user_id=None, name=None, role='User'):
        pass

    def login(self, name, password):
        user = self.get_user(name)
        if not user or not bcrypt.checkpw(password, user.password.encode("utf-8")):
            raise PermissionError("Invalid credentials")

        return self.generate_security_token(user.id, user.name)


class JwtAuthenticator(Authenticator):

    def __init__(self, jwt_config={}):
        self.jwt_issuer = jwt_config['issuer']
        self.jwt_expire_secs = jwt_config['expire_seconds']
        self.jwt_algorithm = jwt_config['algorithm']
        self.jwt_secret_key = jwt_config['secret_key']

    @abstractmethod
    def get_user(self, name):
        pass

    def generate_jwt_token(self, user_id=None, name=None, role='User'):
        return jwt.encode({
            'userId': user_id,
            'role': role,
            'sub': name,
            'iat': int((datetime.datetime.now()).timestamp()),
            'iss': self.jwt_issuer,
            'exp': int((datetime.datetime.now() + datetime.timedelta(seconds=self.jwt_expire_secs)).timestamp())
        }, self.jwt_secret_key, algorithm=self.jwt_algorithm).decode('utf-8')


class JwtBcryptAuthenticator(JwtAuthenticator, BcryptAuthenticator):

    def __init__(self, jwt_config={}):
        super().__init__(jwt_config)
        super(JwtAuthenticator, self).__init__()

    @abstractmethod
    def get_user(self, name):
        pass

    def generate_security_token(self, user_id=None, name=None, role='User'):
        print("Generating security token for user " + name + " with id " + str(user_id))
        return self.generate_jwt_token(user_id, name, role)


class NoAuthJwtAuthenticator(JwtAuthenticator):
    """Dummy/example class that doesn't actually do any auth check, but will still provide a valid JWT token that
    will pass this library's security checks (valid issuer, time, etc). This should really only be used as an example
    or placeholder until your application has actual user entitlements set up.
    """

    def get_user(self, name):
        return ApplicationUser(user_id=1, name=name)

    def login(self, name, password):
        user = self.get_user(name);
        return self.generate_jwt_token(user_id=user.id, name=user.name)
