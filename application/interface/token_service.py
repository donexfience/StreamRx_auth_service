from abc import ABC, abstractmethod
from domain.entities.user import User


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, user: User) -> str: pass

    @abstractmethod
    def create_refresh_token(self, user: User) -> str: pass

    @abstractmethod
    def verify_token(self, token: str) -> dict: pass
