from django.db import models
from datetime import date

# Create your models here.

# name='Menu',
# fields=[
# ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
# ('mealtime', models.CharField(choices=[('AM', 'Morning'), ('MD', 'Lunch'), ('PM', 'Afternoon')], default='AM', max_length=2)),
# ('day', models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday')], default='MON', max_length=3)),
# ('content', models.CharField(max_length=64)),

class Menu(models.Model):
    MORNING = 'AM'
    LUNCH = 'MD'
    AFTERNOON = 'PM'
    MEALTIME_CHOICES = [
        (MORNING, 'Morning'),
        (LUNCH, 'Lunch'),
        (AFTERNOON, 'Afternoon')
    ]
    mealtime = models.CharField(
        max_length=2,
        choices=MEALTIME_CHOICES,
        default=MORNING,
    )

    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = "THU"
    FRIDAY = "FRI"
    SATURDAY ="SAT"
    DAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
    ]
    day = models.CharField(
        max_length=3,
        choices=DAY_CHOICES,
        default=MONDAY,
    )

    content = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.day} {self.mealtime}: {self.content} "

class Holidays(models.Model):
    holiday = models.CharField(max_length=20)
    datefrom = models.DateField()
    dateto = models.DateField()
    
    def __str__(self):
       return f"{self.holiday} : {self.datefrom} - {self.dateto}"

class Invoices(models.Model):
    month = models.DateField() # display using datetime functions
    surname = models.CharField(max_length=20)
    firstname =models.CharField(max_length=20)

# class vlinks(models.Model):
    
    # links in Accounts page
 #       PRICING = 'default',
  #      INVOICES = 'tab2',
   #     PURCHASES = 'tab3',
    #    TAXRETURNS = 'tab4',
     #   WHATTOCHARGE = 'tab5',
#
    # links in Paperwork page
 #       PROCEDURES = 'default',
  #      CONTRACTS = 'tab2',
   #     AGREEMENTS = 'tab3',
    #    TRAINING = 'tab4',
     #   INSPECTION = 'tab5',

    # links in Kids page
      #  MAIN = 'default',
       # CONTACTS = 'tab2',
        #DIETRY = 'tab3',
        #MEDICAL = 'tab4',
        #PAPERWORK = 'tab5'
#
 #   VTAB_CHOICES = [
  #      (PRICING, 'default'),
   #     (INVOICES, 'tab2'),
    #    (PURCHASES, 'tab3'),
     #   (TAXRETURNS, 'tab4'),
      #  (WHATTOCHARGE, 'tab5'),
       # (PROCEDURES, 'default'),
        #(CONTRACTS, 'tab2'),
        #(AGREEMENTS, 'tab3'),
        #(TRAINING, 'tab4'),
        #(INSPECTION, 'tab5'),
        #(MAIN, 'default'),
        #(CONTACTS, 'tab2'),
        #(DIETRY, 'tab3'),
        #(MEDICAL, 'tab4'),
        #(PAPERWORK, 'tab5')

    #]
    #vtabchoice = models.CharField(
     #   max_length=20,
      #  choices=VTAB_CHOICES,
       # default=PRICING,
    #)
    

    #def __str__(self):
     #   return f"{self.vtabchoice} "
