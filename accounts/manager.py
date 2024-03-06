from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, user_phone, user_id, Full_name, password, email):
        if not user_phone:
            raise ValueError("user must have phone number")
        if not user_id:
            raise ValueError("user must have email")
        if not Full_name:
            raise ValueError("user must have full name")
        if not password:
            raise ValueError("user must have password")
        user = self.model(user_phone=user_phone, user_id=user_id, Full_name=Full_name, email=email)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_phone, user_id, Full_name, password,email):
        user = self.create_user(user_phone, user_id, Full_name, password, email)
        user.is_admin = True
        user.save(using=self._db)
        return user
