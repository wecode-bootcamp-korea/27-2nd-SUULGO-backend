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

class Stack(models.Model): 
    name   = models.CharField(max_length=20)
    number = models.IntegerField()

    class Meta: 
        db_table = 'stacks'
        
class AlcoholLimit(models.Model): 
    name   = models.CharField(max_length=20)
    number = models.IntegerField()

    class Meta: 
        db_table = 'alcohol_limits'

class Meeting(TimeStampModel):
    requester  = models.ForeignKey('User', on_delete=models.CASCADE, related_name='requester')
    respondent = models.ForeignKey('User', on_delete=models.CASCADE, related_name='respondent')
    time       = models.DateTimeField()
    is_accept  = models.BooleanField(default=False)
    
    class Meta: 
        db_table = 'meetings'

class SurveyDrinkingMethod(models.Model):
    drinking_method = models.ForeignKey('DrinkingMethod', on_delete=models.CASCADE)
    survey          = models.ForeignKey('Survey', on_delete=models.CASCADE)

    class Meta:
        db_table = 'survey_drinking_methods'

class DrinkingMethod(models.Model):
    name    = models.CharField(max_length=10)
    surveys = models.ManyToManyField('Survey', through=SurveyDrinkingMethod, related_name="drinking_methods")

    class Meta:
        db_table = 'drinking_methods'

class SurveyFlavor(models.Model):
    flavor = models.ForeignKey('Flavor', on_delete=models.CASCADE)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)

    class Meta:
        db_table = 'survey_flavors'

class Flavor(models.Model):
    name    = models.CharField(max_length=10)
    surveys = models.ManyToManyField('Survey', through=SurveyFlavor, related_name="flavors")

    class Meta:
        db_table = 'flavors'

class SurveyAlcoholCategory(models.Model):
    alcohol_category = models.ForeignKey('AlcoholCategory', on_delete=models.CASCADE)
    survey           = models.ForeignKey('Survey', on_delete=models.CASCADE)

    class Meta:
        db_table = 'survey_alcohol_categories'

class AlcoholCategory(models.Model):
    name    = models.CharField(max_length=10)
    surveys = models.ManyToManyField('Survey', through=SurveyAlcoholCategory, related_name="alcohol_categories")

    class Meta:
        db_table = 'alcohol_categories'

class Survey(TimeStampModel):
    gender                  = models.ForeignKey('Gender', on_delete=models.CASCADE)
    mbti                    = models.ForeignKey('Mbti', on_delete=models.CASCADE)
    class_number            = models.PositiveSmallIntegerField()
    stack                   = models.ForeignKey('Stack', on_delete=models.CASCADE)
    alcohol_limit           = models.ForeignKey('AlcoholLimit', on_delete=models.CASCADE)
    alcohol_level           = models.CharField(max_length=100)
    comment                 = models.CharField(max_length=500)
    favorite_place          = models.CharField(max_length=200)
    favorite_food           = models.CharField(max_length=200)
    hobby                   = models.CharField(max_length=200)
    deleted_at              = models.DateTimeField(null=True)
    user                    = models.ForeignKey('User', on_delete=models.CASCADE, unique=True)
    drinking_method_weight  = models.DecimalField(max_digits = 5, decimal_places = 2, default=0.2)
    alcohol_category_weight = models.DecimalField(max_digits = 5, decimal_places = 2, default=0.2)
    alcohol_limit_weight    = models.DecimalField(max_digits = 5, decimal_places = 2, default=0.2)
    alcohol_level_weight    = models.DecimalField(max_digits = 5, decimal_places = 2, default=0.2)
    flavor_weight           = models.DecimalField(max_digits = 5, decimal_places = 2, default=0.2)

    class Meta:
        db_table = 'surveys'

class User(TimeStampModel):
    kakao_id          = models.CharField(max_length=100)
    name              = models.CharField(max_length=50)
    profile_image_url = models.URLField(max_length=500)
    email             = models.CharField(max_length=200, null=True)
    deleted_at        = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'
