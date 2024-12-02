import uuid

from django.db import models

class accounts(models.Model):
    accounts_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_num = models.IntegerField()
    bank_code = models.IntegerField()
    transaction_type = models.CharField(max_length=45)
    balance = models.IntegerField()
    user_id = models.ForeignKey('users.id', on_delete=models.CASCADE)

class transactions(models.Model):
    transaction_id = models.BigIntegerField(primary_key=True)
    after_balance = models.IntegerField()
    transaction_detail = models.CharField(max_length=45)
    transaction_type = models.CharField(max_length=45)
    transaction_method = models.CharField(max_length=45)
    transaction_time = models.DateTimeField()
    account_num = models.ForeignKey('accounts.accounts_id', on_delete=models.CASCADE)
