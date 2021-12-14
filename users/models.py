from django.db   import models

from core.models import TimeStampModel

class Mbti(models.Model): 
    name        = models.CharField(max_length=20)
    information = models.CharField(max_length=200)

    class Meta: 
        db_table = 'mbtis'
        
class Gender(models.Model): 
    name = models.CharField(max_length=20)

    class Meta: 
        db_table = 'genders'

class Meeting(TimeStampModel): 
    requester  = models.ForeignKey('User', on_delete=models.CASCADE, related_name='requester')
    respondent = models.ForeignKey('User', on_delete=models.CASCADE, related_name='respondent')
    time       = models.DateTimeField()

    class Meta: 
        db_table = 'meetings'

class UserDrinkingMethod(models.Model): 
    drinking_method = models.ForeignKey('DrinkingMethod', on_delete=models.CASCADE)
    user            = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'user_drinking_methods'

class DrinkingMethod(models.Model): 
    name  = models.CharField(max_length=10)
    users = models.ManyToManyField('User', through=UserDrinkingMethod)

    class Meta: 
        db_table = 'drinking_methods'

class UserFlavor(models.Model):
    flavor = models.ForeignKey('Flavor', on_delete=models.CASCADE)
    user   = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_flavors'

class Flavor(models .Model):
    name  = models.CharField(max_length=10)
    users = models.ManyToManyField('User', through=UserFlavor)

    class Meta:
        db_table = 'flavors'

class UserAlcoholCategory(models.Model):
    alcohol_category = models.ForeignKey('AlcoholCategory', on_delete=models.CASCADE)
    user             = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_alcohol_categories'

class AlcoholCategory(models.Model):
    name  = models.CharField(max_length=10)
    users = models.ManyToManyField('User', through=UserAlcoholCategory)

    class Meta:
        db_table = 'alcohol_categories'

class User(TimeStampModel):
    name              = models.CharField(max_length=20)
    profile_image_url = models.URLField(max_length=500)
    gender            = models.ForeignKey('Gender', on_delete=models.CASCADE)
    mbti              = models.ForeignKey('Mbti', on_delete=models.CASCADE)
    stack             = models.IntegerField()
    alcohol_limit     = models.IntegerField()
    alcohol_level     = models.IntegerField()
    comment           = models.CharField(max_length=500)
    favorite_place    = models.CharField(max_length=200)
    favorite_food     = models.CharField(max_length=200)
    hobby             = models.CharField(max_length=200)
    email             = models.CharField(max_length=200)
    kakao_login       = models.CharField(max_length=100)
    deleted_at        = models.DateTimeField(null=True)
    class_number      = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'users'
