from django.db import models
from passlib.hash import pbkdf2_sha256
# Create your models here.

    # def verify_password(self,raw_password):
    #     return pbkdf2_sha256.verify(self.raw_password)