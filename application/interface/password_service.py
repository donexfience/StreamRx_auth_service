from abc import ABC, abstractmethod


class PasswordService(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str: pass
    @abstractmethod
    def verify_password (self,plain_password:str,hashed_password:str) -> bool: pass
