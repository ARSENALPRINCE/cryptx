from random import randint
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
TOKEN = [
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
    ('LTC', 'Litecoin'),
    ('DOGE', 'Dogecoin'),
]
GENDER =(
    ("M",'Male'),
    ("F", 'Female'),
    ("U",'Unidentified')
)
ESCROW_SALE_STATUS = (
    ('P', 'Pending'),
    ('C', 'Cancelled'),
    ('S', 'Sold')
)





class Asset(models.Model):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length = 5, unique=True, choices=TOKEN, null= False)
    description = models.TextField(default='')
    price = models.DecimalField(decimal_places=3, max_digits=9)
    #quantity = models.DecimalField(decimal_places=10, max_digits=10, default=550.50000000000)

    def __str__(self):
        return self.name

class Tradxtar(models.Model):
    trader = models.ForeignKey(to=User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=GENDER,default='u')
    balance = models.DecimalField(decimal_places=3, max_digits=10, default=10000)
    Quantity = models.DecimalField(decimal_places=10, max_digits=12, default=10000.0)

    def __str__(self):
        return self.trader.username

class Wallet(models.Model):
    holder = models.ForeignKey(to=Tradxtar, on_delete= models.CASCADE)
    asset = models.ForeignKey(Asset,on_delete= models.CASCADE)
    address = models.CharField(max_length=15,default='')
    Quantity = models.DecimalField(decimal_places=10, max_digits=10, default=0.0)

    def generateAddress(self):
        starting_address = self.asset.symbol
        return f'{starting_address}{randint(10000000000000,9999999999999999)}'
    
    def save(self):
        if len(self.address) < 8 or self.address == '' or not self.address.startswith(self.asset.symbol):
            self.address = self.generateAddress()
        super().save()
        def __str__(self):
            return f'{self.holder} {self.asset} {self.address}'
        
class Escrowsale(models.Model):
        rate = models.DecimalField(decimal_places=3, max_digits=12, blank=False) 
        quantity = models.DecimalField(decimal_places=3, max_digits=10, blank=False)
        status = models.CharField(max_length=10, choices=ESCROW_SALE_STATUS,default='P')
        wallet_seller = models.ForeignKey(to= Wallet, on_delete=models.CASCADE,)
        wallet_receiver = models.CharField(max_length=20, default="")


        

            


    

