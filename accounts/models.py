from django.db import models

# Create your models here.
class Purchase(models.Model):
    date = models.DateField() # "yyyy-mm-dd"
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=64)
    amount = models.CharField(max_length=64)
    purchase = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.date}: {self.category} - {self.name} - Purchase : {self.purchase} - £ {self.amount}"

class Pricing(models.Model):
    fullday = models.IntegerField(default=0)
    fulldayretainer = models.IntegerField(default=0)
    parttime = models.IntegerField(default=0)
    parttimeretainer = models.IntegerField(default=0)
    
    latepayment = models.IntegerField(default=0)
    latepickup = models.IntegerField(default=0)

    eveningcare = models.IntegerField(default=0)
      

    def __str__(self):
        return f"Full day: {self.fullday}, Full day retainer: {self.fulldayretainer}, Part-Time: {self.parttime}, \
            Part time retainer: {self.parttimeretainer}, Late Payment: {self. latepayment}, Late Pickup: {self. latepickup}, \
                Evening Care: {self.eveningcare}"


# invoice for single child, later to be added to invoices

class Invoice(models.Model):
    
    parentName = models.CharField(max_length=64)
    parentID = models.IntegerField(default = 0)    
    #month = models.CharField(max_length=64)

    #year = models.IntegerField(default = 0)

    week1= models.CharField(max_length=64, default="")
    week2= models.CharField(max_length=64, default="")
    week3= models.CharField(max_length=64, default="")
    week4= models.CharField(max_length=64, default="")
    week5= models.CharField(max_length=64, default="")
    
    # date range of the invoice
    period = models.CharField(max_length=64, default="")
    
    # this should hold all kids firstnames as a single comma delimited string

    children = models.CharField(max_length=64)

    # these are string instead of integer as to collect string list of all kids hours

    week1Hours= models.CharField(max_length=64, default="")
    week2Hours= models.CharField(max_length=64, default="")
    week3Hours= models.CharField(max_length=64, default="")
    week4Hours= models.CharField(max_length=64, default="")
    week5Hours= models.CharField(max_length=64, default="")

    week1mins= models.CharField(max_length=64, default="")
    week2mins= models.CharField(max_length=64, default="")
    week3mins= models.CharField(max_length=64, default="")
    week4mins= models.CharField(max_length=64, default="")
    week5mins= models.CharField(max_length=64, default="")

    rate = models.CharField(max_length=64, default="")
    

    total = models.IntegerField(default = 0.00)

    latepayment = models.IntegerField(default = 0.00)
    latepickup = models.IntegerField(default = 0.00)
    reason = models.CharField(max_length=64, default="")


    
    #total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

                    
    STATUS_CHOICES = [
        ("OS","outstanding"),
        ("PD", "paid"),

    ]

    status = models.CharField(
        choices = STATUS_CHOICES,
        default= "OS",
        max_length=20,
    )


    YEAR_CHOICES = [
        (2021, 2021),
        (2022, 2022)
    ]

    year = models.IntegerField(
        choices = YEAR_CHOICES,
        default=2021,
    )
    MONTH_CHOICES = [
        ("January", "January"),
        ("February", "February"),
        ("March", "March"),
        ("April", "April"),
        ("May", "May"),
        ("June", "June"),
        ("July", "July"),
        ("August", "August"),
        ("September", "September"),
        ("October", "October"),
        ("November", "November"),
        ("December", "December"),
    ]

    month = models.CharField(
        choices = MONTH_CHOICES,
        default="January",
        max_length=10,
    )
   
       
    
    
    def __str__(self):
        return f"parentName: {self.parentName}, children: {self.children}, month: {self.month}, year: {self.year}, week1: {self.week1}, \
            week2: {self.week2}, week3: {self.week3}, week4: {self.week4}, week1Hours: {self.week1Hours}, \
                week2Hours: {self.week2Hours}, week3Hours: {self.week3Hours}, week4Hours: {self.week4Hours}, \
                    week1mins: {self.week1mins}, week2mins: {self.week2mins}, week3mins: {self.week3mins}, \
                        week4mins: {self.week4mins}, rate: {self.rate}, total: {self.total}, status: {self.status},\
                            latepayment: {self.latepayment}, latepickup: {self.latepickup}"
    

    
# to hold all invoices generated
class Invoices(models.Model):

    #childsInvoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
        
    name = models.CharField(max_length=64)
        
    def __str__(self):
        return f"{self.name}"
