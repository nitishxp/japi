from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=20,
                            unique=True,
                            help_text='Name of company')

    class Meta:
        db_table = 'company'

    def __str__(self):
        return self.name


class CompanyAddress(models.Model):

    building_number = models.CharField(max_length=30,
                                       help_text='Building number eg. 10/12')
    postal_code = models.IntegerField(help_text='6 Digit postal code')
    locality = models.CharField(max_length=30, help_text='Locality')
    city = models.CharField(max_length=30, help_text='Name of city')
    state = models.CharField(max_length=30, help_text='Name of state')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'company_address'