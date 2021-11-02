from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

import calendar

from accounts.models import Purchase, Pricing, Invoice, Invoices
from child.models import Child, Parent
 
### accounts screen ###

def accounts(request):
    purchases = Purchase.objects.all()
    prices = Pricing.objects.all()
    gettab = request.GET.get("name") 
    invoices = Invoice.objects.all()
    total = 0

    months= []
    years = []
    parents = []

   
    for invoice in invoices:
        total += invoice.total

        if invoice.month not in months:
            months.append(invoice.month)
        
        if invoice.year not in years:
            years.append(invoice.year)

        if invoice.parentName not in parents:
            parents.append(invoice.parentName)


    context = {
        "gettab": gettab,
        "purchases": purchases,
        "prices": prices,
        "invoices": invoices,
        "total": total,
        "months": months,
        "years": years,
        "parents": parents,
    }

    return render(request, 'Accounts/accounts.html',context)

# use to hold invoice period obtained in getmondays but used later
period = ""  # global variable

# usee in newInvoice to get first day of the month and the total number of days
def getMondays(month, year): # eg nov 2021 
    
        mondays = []

        months=["January","February","March","April", "May","June","July","August","September","October","November","December"]
        
        monthasnumber=months.index(month)+1 # returns first day of month and number days in month
        monthdetail = calendar.monthrange(int(year),monthasnumber)

        firstdayname = calendar.day_name[monthdetail[0]]

        firstday = monthdetail[0] # sunday = 6 monday = 0, tuesday = 1
        
        # getting the first monday of the month

        firstmonday = 8

        if firstday == 0: # if the firstday of the month is a monday
            firstmonday = 1  # set first monday to 1st
        else:
            for x in range(6):  # 0 1 2 3 4 5
                if firstday == x + 1:
                    print("firstday :", firstday)
                    firstmonday -= 1
                    print("firstmonday :", firstmonday)
                    break
                else:
                    firstmonday -= 1

        # use firstmonday, month and year to get dates for each monday in month

        monday1 = str(firstmonday) + " " + month + " " + str(year)
        monday2 = str(firstmonday + 7) + " " + month + " " + str(year)
        monday3 = str(firstmonday + 14) + " " + month + " " + str(year)
        monday4 = str(firstmonday + 21) + " " + month + " " + str(year)

        # for billing period (shown in grey) on the filling invoice 
        firstbillingday = "Monday " + str(firstmonday) + " " + month
        lastbillingday = "Friday " + str(firstmonday + 25) + " " + month

        global period
        period = firstbillingday + " - " + lastbillingday

        # get number of days in month picked
        num_days = calendar.monthrange(int(year), monthasnumber)[1]

        monday5 = ""

        if (firstmonday + 28) <= num_days:
            monday5 = str(firstmonday + 28) + " " + month + " " + str(year)
        

        mondays.append(monday1)
        mondays.append(monday2)
        mondays.append(monday3)
        mondays.append(monday4)

        if monday5 != "":
            mondays.append(monday5)

        return mondays

# Accounts | Invoice tab | Create Invoice

def newInvoice(request):
    
    page = request.POST.get("page")  
    
    kids = Child.objects.all()
    parents = Parent.objects.all()
    invoices = Invoices.objects.all()
    rates = Pricing.objects.first()

    ####  children childtype provides rate as eg "Full Time"
    ####  pricing attributes eg "fullday"

    # this is to provide a link between childtype and pricing for the final invoice
    childrate = {}
            
    childrate["Full Time"] = rates.fullday
    childrate["Full Time Retainer"] = rates.fulldayretainer
    childrate["Part Time"] = rates.parttime
    childrate["Part Time Retainer"] = rates.parttimeretainer
    childrate["Late Payment"] = rates.latepayment
    childrate["Evening Care"] = rates.eveningcare

    # remove duplicates from list of parents
    parentlist = []
    for parent in parents:
        if parent not in parentlist:
            parentlist.append(parent)
    
    ####### Invoices Tab | click on button: Create invoice ##########
            
    if page == "CreateInvoiceButton":

        context={"parents" : parentlist}

        return render(request, 'Accounts/newInvoice.html', context)
        
    #######  Create invoice  | New Invoice first Page | Next Button  ##########

    elif page == "NewInvoicePage1":
        
        if 'cancel' in request.POST:
             return redirect('accounts') 
        
        else:
            # From newInvoice.html get:
            parentID    =   request.POST["selectParent"]  # numberical id of parent selected
            month       =   request.POST["month"]
            year        =   request.POST["year"]
            
            parent = Parent.objects.get(pk=parentID)  # full parent object

            invoice = Invoice() # starting point of invoice
            
            # and create the invoice for this child
            invoice.parentName = parent.firstname + " " + parent.surname
            invoice.parentID = parent.id
            invoice.month = month
            invoice.year = year

            # use month and year above to get start date of each week in the month   
            mondays= getMondays(month,year)
            
            invoice.week1, invoice.week2, invoice.week3, invoice.week4 = mondays[0], mondays[1], mondays[2], mondays[3]
            

            if len(mondays)>4:

                invoice.week5 = mondays[4]

            invoice.period = period
            
            invoice.save()
            
            #  update - editWeekInvoice template - on invoice childs times.. clicking on one of them takes to edit page
            update = request.POST.get("update")
                    
            if update == "yes":
                    
                kidID= request.session['updateID']
                # kidID= request.POST.get("childid")
            
                kid = Child.objects.get(pk=kidID)

                # get all times from editWeekInvoice.html
                    
                kid.mondaystart = request.POST["MonS"]
                kid.mondayfinish = request.POST["MonF"]  
                kid.tuesdaystart = request.POST["TueS"]
                kid.tuesdayfinish = request.POST["TueF"]
                kid.wednesdaystart = request.POST["WedS"]
                kid.wednesdayfinish = request.POST["WedF"]
                kid.thursdaystart = request.POST["ThuS"]
                kid.thursdayfinish = request.POST["ThuF"]
                kid.fridaystart = request.POST["FriS"]
                kid.fridayfinish = request.POST["FriF"]
                kid.saturdaystart = request.POST["SatS"]
                kid.saturdayfinish = request.POST["SatF"]

                kid.save()
                        
                # iterate kids
            
            children = {}
            
            for kid in kids:
                
                # if kid has parent selected
                
                if kid.parent.id == parent.id:

                    #invoice.children = invoice.children + "," + kid.firstname
                    if len(invoice.children) > 0:
                        invoice.children = invoice.children + "," + str(kid.id) # concatenate children ids
                    else:
                        invoice.children = invoice.children + str(kid.id) # concatenate children ids
                    totalHours = 0
                    totalMins = 0

                    # get their scheduled times for each day
                    days={
                        'monday':[kid.mondaystart.strftime("%H"), kid.mondayfinish.strftime("%H"), kid.mondaystart.strftime("%M"), kid.mondayfinish.strftime("%M")],
                        'tuesday':[kid.tuesdaystart.strftime("%H"), kid.tuesdayfinish.strftime("%H"), kid.tuesdaystart.strftime("%M"), kid.tuesdayfinish.strftime("%M")], 
                        'wednesday':[kid.wednesdaystart.strftime("%H"), kid.wednesdayfinish.strftime("%H"), kid.wednesdaystart.strftime("%M"), kid.wednesdayfinish.strftime("%M")], 
                        'thursday':[kid.thursdaystart.strftime("%H"), kid.thursdayfinish.strftime("%H"), kid.thursdaystart.strftime("%M"), kid.thursdayfinish.strftime("%M")], 
                        'friday':[kid.fridaystart.strftime("%H"), kid.fridayfinish.strftime("%H"), kid.fridaystart.strftime("%M"), kid.fridayfinish.strftime("%M")],
                        'saturday':[kid.saturdaystart.strftime("%H"), kid.saturdayfinish.strftime("%H"), kid.saturdaystart.strftime("%M"), kid.saturdayfinish.strftime("%M")]
                        }

                    # from scheduled times, calculate their total hours and mins
                    for key, day in days.items():
                                
                        # calculate total hours in
                        hourin = day[0]
                        hourout = day[1]
                                
                        hours = int(hourout)-int(hourin)
                            
                        # ... and total mins in 
                        minin  = day[2]      
                        minout  = day[3]     
                        if int(minout) == 0 and int(minin)>0:
                            minout = 60
                            hours = hours-1
                                    
                        mins = (int(minout)-int(minin))
                        
                        totalHours += hours
                        totalMins += mins
                        
                    # change the total mins to hours and mins, and update totals
                    if totalMins > 60:
                        totalHours += totalMins / 60
                        totalMins = totalMins % 60

                    # update kids totalHours and totalMins attributes
                    kid.totalHours = totalHours
                    kid.totalMins = totalMins

                    invoice.week1Hours = invoice.week1Hours + "," + str(totalHours)
                    invoice.week1mins = invoice.week1mins + "," + str(totalMins)
                    invoice.week2Hours = invoice.week2Hours + "," + str(totalHours)
                    invoice.week2mins = invoice.week2mins + "," + str(totalMins)
                    invoice.week3Hours = invoice.week3Hours + "," + str(totalHours)
                    invoice.week3mins = invoice.week3mins + "," + str(totalMins)
                    invoice.week4Hours = invoice.week4Hours + "," + str(totalHours)
                    invoice.week4mins = invoice.week4mins + "," + str(totalMins)
                    invoice.week5Hours = invoice.week5Hours + "," + str(totalHours)
                    invoice.week5mins = invoice.week5mins + "," + str(totalMins)

                    invoice.rate = invoice.rate + "," + kid.childtype
                    
                    
                    # compares mapped childtype to fee in childrates, adds matched fee
                    for rate, fee in childrate.items():
                        if kid.childtype == rate:
                            kid.childtypefee = fee

                    #test to get childs days per month.. number of weeks in month should be number of mondays (weeks com monday)
                    
                    if invoice.week5 == "":
                        weeksinmonth =4
                    else:
                        weeksinmonth = 5
                    
                    kid.invoicesub = kid.childtypefee*kid.dayspermonth
                    
                   
                    kid.dayspermonth = kid.daysperweek *weeksinmonth 
                    
                    invoice.save()                 
                    kid.save()
                    
                    children[kid.firstname]=[kid.id, kid.totalHours, kid.totalMins, kid.childtype]
                        
            context={
                "children" : children,
                "invoice" : invoice,
            }
            
            return render(request, 'Accounts/newInvoice2.html', context)
            
    elif page == "p2":
        
        id = request.POST["invoice"]
        newInvoice = Invoice.objects.get(pk=id)
                
        if 'cancel' in request.POST:
            newInvoice.delete()
            return redirect('accounts') 
    
        else:
            # next step: any other charges?
            parentname = request.POST["parentName"]
            month = request.POST["month"]
            year = request.POST["year"]
            invoices = Invoices.objects.all()
            children = request.POST["children"]              
           
            context={
                "invoice": newInvoice,
                "invoices": invoices,
                "children" : children,
                "month" : month,
                "year" : year,
                "parentname" : parentname,
                }
                        
            return render(request, 'Accounts/newInvoice3.html',context)     
        
    elif page == "p3": 

        id = request.POST["invoice"]
        newInvoice = Invoice.objects.get(pk=id)    

        latePayment     =   request.POST.get("latepayment")
        latePickup      =   request.POST.get("latepickup")
        reason      =   request.POST.get("reason")
                
        if 'cancel' in request.POST:
            newInvoice.delete()
            return redirect('accounts') 
    
        else:
            
            month = request.POST["month"]
            year = request.POST["year"]
            parentName = request.POST["parentname"]
            
            parentKids = []

            #kids = Child.objects.all()

            newInvoice.total = 0
            
            for child in newInvoice.children.split(","):
                childDetails = Child.objects.get(pk=child) 
                parentKids.append(childDetails)
                newInvoice.total += childDetails.invoicesub 
            
            newInvoice.save()

            other = "No"

            if latePayment =="yes":
                other = "Yes"
                newInvoice.latepayment = rates.latepayment
                newInvoice.total += rates.latepayment
           
            if latePickup == "yes":
                other = "Yes"
                newInvoice.latepickup = rates.latepickup
                newInvoice.total += rates.latepickup
            
            if latePayment == "no" and latePickup == "no":
                other ="No"
            
            newInvoice.reason = reason
            
            newInvoice.save()

            context = {
                "month": month,
                "year": year,
                "parentName": parentName,
                "children": parentKids,  
                "invoice": newInvoice,
                "other" : other,
                "due" : date.today() + relativedelta(weeks=+1),
                #"week2" : week2,
                #"week3" : week3,
                #"week4" : week4,
                    
                #"totalhours": totalHours,
                #"totalmins" : totalMins,
                #"childid": id,
            }
            return render(request, 'Accounts/finalInvoice.html', context)

        
    else:
        return redirect('accounts') 


def editWeekInvoice(request, id, month, year, parentname):

    week = request.GET.get("name") 
    
    month= month
    #invoices=request.POST["invoices"]
    year = year
    parentname = parentname
    kids = Child.objects.all()
    child = Child.objects.get(pk=id)
    
    request.session['updateID']= id

    #invoices = {}
    #invoices = invoice.objects.all()
    
    #for invoice in invoices:
     #   if invoice.childID = id:
      #      invoices[child.firstname]=invoice
           
    rate = child.childtype
    #assert rate == 0, rate
    rates=["Full Time", "Part Time", "After School", "Under 5", "Sat Only"]
    if rate in rates:
        rates.remove(rate)
        rates.insert(0, rate)

    context = {
        "week": week,
        "rates": rates,
        "parentname": parentname,
        "child": child,
        "month": month,
        "year": year,
        "id": id,
        #"invoices": invoices,
    }

    return render(request, 'Accounts/editWeekInvoice.html',context)


def invoiceview(request):

    id = request.GET.get("name")     
    theInvoice = Invoice.objects.get(pk=id)
    
    parentKids = []

    for child in theInvoice.children.split(","):
        childDetails = Child.objects.get(pk=child) 
        parentKids.append(childDetails)
    
    context = {
        "invoice": theInvoice,
        "children": parentKids,
    }
 
    return render(request, 'Accounts/invoiceview.html', context)


def addPurchase(request):
    
    task = request.POST.get("task")

    purchases = Purchase.objects.all()
    
    if task =="purchases":
        
        context={
            "purchases" : purchases
            }
            
        return render(request, 'Accounts/addPurchase.html', context)
    
    if task =="addpurchase":

        date = request.POST.get("dateOfPurchase")
        category = request.POST.get("category")
        name = request.POST.get("name")
        purchase = request.POST.get("purchase")
        payment = request.POST.get("payment")
        
        newPurchase = Purchase(date=date, category=category, name=name, purchase = purchase, amount = payment)
        newPurchase.save()

        return HttpResponseRedirect(reverse("accounts"))
    
def changefees(request):
    
    charges = Pricing.objects.all()

    if charges:  # adversly, this means if no instances exist
        
        charges = Pricing()
        charges.fullday= 25
        charges.fulldayretainer= 12
        charges.parttime = 12
        charges.parttimeretainer = 6
        charges.latepayment = 5
        charges.latepickup = 5

        charges.save()
        
    choices ={"fullday":charges.fullday,  "parttime":charges.parttime, "latepayment":charges.latepayment, "latepickup":charges.latepickup }

    
    context={
        "choices": choices,
        #"charges": charges
    }
        
    return render(request, 'Accounts/changefees.html',context)
    
    
def changefees2(request):

    # in change fees if no instance exists, one is created, so an instance should exist here
    prices = Pricing.objects.first()
   
    change = request.POST["feechange"]
    amount = request.POST["newfee"]
      
    setattr(prices, change, amount)

    if change == "fullday":    
        setattr(prices, "fulldayretainer", int(amount)/2)
    elif change == "parttime":
        setattr(prices, "parttimeretainer", int(amount)/2)
    
    prices.save()

    ## somehow is creating more instances, need to see how this is happening, or code to delete in this view
    return HttpResponseRedirect(reverse("accounts"))

