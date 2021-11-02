from django.db import models
from django.db.models.deletion import SET_NULL


# Create your models here.


class Attendance(models.Model):
    
    #child = models.ForeignKey(Child, on_delete=models.CASCADE)
    
    mondaystart = models.TimeField(default='00:00')
    mondayfinish = models.TimeField(default='00:00')
    
    tuesdaystart = models.TimeField(default='00:00')
    tuesdayfinish = models.TimeField(default='00:00')
    
    wednesdaystart = models.TimeField(default='00:00')
    wednesdayfinish = models.TimeField(default='00:00') 
    
    thursdaystart = models.TimeField(default='00:00')
    thursdayfinish = models.TimeField(default='00:00')
    
    fridaystart = models.TimeField(default='00:00')
    fridayfinish = models.TimeField(default='00:00')
    
    saturdaystart = models.TimeField(default='00:00')
    saturdayfinish = models.TimeField(default='00:00')

    #totalHours = models.IntegerField(default=0)
    #totalMins = models.IntegerField(default=0)

    

    def __str__(self):
        return f"{self.id}:: Monday: {self.mondaystart} - {self.mondayfinish} \
            Tuesday: {self.tuesdaystart} - {self.tuesdayfinish} \
                Wednesday: {self.wednesdaystart} - {self.wednesdayfinish} \
                    Thursday: {self.thursdaystart} - {self.thursdayfinish} \
                        Friday: {self.fridaystart} - {self.fridayfinish} \
                            Saturday: {self.saturdaystart} - {self.saturdayfinish} \\"
                            #    Total: {self.totalHours} Hrs- {self.totalMins} Mins\\"


class Parent(models.Model):
    surname = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    relation = models.CharField(max_length=20)
   # child = models.ForeignKey(Kids, on_delete=models.CASCADE, related_name="Child")
    # change field type for phone number entry only
    mainNumber = models.CharField(max_length=11)
    altNumber = models.CharField(max_length=11)
    otherNumber = models.CharField(max_length=11)

    class Meta:
        db_table = "Parent"
        
    def __str__(self):
        return f"{self.id}: {self.surname} - {self.firstname} Relation: {self.relation}" #To: {self.child}"

class Child(models.Model):
    surname = models.CharField(max_length=64)
    firstname = models.CharField(max_length=64)
    # parent = models.CharField(max_length=64)
    parent = models.ForeignKey(Parent, null=True, blank=True, on_delete=models.CASCADE)
    dateofbirth = models.DateField() # "yyyy-mm-dd"
    childgender = models.CharField(max_length=10)
    maincontact = models.CharField(max_length=64)
    c1 = models.CharField(max_length=11)
    c2 = models.CharField(max_length=11)
    othercontact = models.CharField(max_length=64)
    c3 = models.CharField(max_length=11)
    childphoto = models.ImageField(upload_to='images/', default='images/no_boy_photo.png', max_length=100) # **options)
    active = models.BooleanField(default=False)

    address = models.CharField(max_length=1024)

    medical = models.CharField(max_length=100)
    dietry = models.CharField(max_length=100)

       
    mondaystart = models.TimeField(default='00:00')
    mondayfinish = models.TimeField(default='00:00')
    
    tuesdaystart = models.TimeField(default='00:00')
    tuesdayfinish = models.TimeField(default='00:00')
    
    wednesdaystart = models.TimeField(default='00:00')
    wednesdayfinish = models.TimeField(default='00:00') 
    
    thursdaystart = models.TimeField(default='00:00')
    thursdayfinish = models.TimeField(default='00:00')
    
    fridaystart = models.TimeField(default='00:00')
    fridayfinish = models.TimeField(default='00:00')
    
    saturdaystart = models.TimeField(default='00:00')
    saturdayfinish = models.TimeField(default='00:00')
    
    totalHours = models.IntegerField(default=0)
    totalMins = models.IntegerField(default=0)

    daysperweek = models.IntegerField(default = 0)

    dayspermonth = models.IntegerField(default = 0)
 
    # for invoice
    childtype = models.CharField(max_length=64)
    childtypefee = models.IntegerField(default=0)
    invoicesub = models.IntegerField(default = 0)
       
    def __str__(self):
        return f"{self.id}: {self.surname} - {self.firstname} DOB: {self.dateofbirth} GENDER: {self.childgender} \
            PARENT: {self.parent} TYPE: {self.childtype} FEE: {self.childtypefee} MAIN CONTACT: {self.maincontact} : {self.c1} or {self.c2} \
                OTHER CONTACT: {self.othercontact} : {self.c3} PHOTO URL: {self.childphoto} ACTIVE: {self.active} \
                    monS: {self.mondaystart} DAYS PER WEEK: {self.daysperweek} \\" 



