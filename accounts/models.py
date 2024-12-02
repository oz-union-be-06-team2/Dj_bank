from django.db import models

class accounts(models.Model):
    account_num = models.IntegerField()
    bank_code = models.IntegerField()
    account_type = models.CharField(max_length=45)
    balance = models.IntegerField()
    user = models.ForeignKey('users.id', on_delete=models.CASCADE)

class transactions(models.Model):
    balance = models.IntegerField()
    transaction_detail = models.CharField(max_length=45)
    transaction_type = models.CharField(max_length=45)
    transaction_method = models.CharField(max_length=45)
    transaction_time = models.DateTimeField()
    account = models.ForeignKey(accounts, on_delete=models.CASCADE)
