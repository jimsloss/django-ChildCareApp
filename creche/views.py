from django.contrib.auth import authenticate, login, logout, admin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta
import calendar
from child.views import childview


from child.models import Child
from .models import Menu, Holidays


# Create your views here.

# first page shown
def index(request):
    if not request.user.is_authenticated:
        # if not logged in, show login page
        return render(request, "users/login.html", {"message": "Log in: "})
    context = {
        "user": request.user,
        "kids": Child.objects.all()
        }
   # if is logged in then show home page, for now set to thisweek
    return render(request, 'TheCreche/mainscreen.html', context) 

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    # IF USER IS LOGGED IN SUCCESSFULLY, GO BACK TO INDEX ABOVE
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
        
    else:
        # IF NOT LOGGED IN SUCCESSFULLY, RE-DISPLAY LOG IN SCREEN WITH APPROPRIATE MESSAGE
        return render(request, "Users/login.html", {"message": "Invalid log in"})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Log In"})

def register_view(request):
    return render(request, "users/register.html")

def register(request):
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    user = User.objects.create_user(username,email,password)
    user.save()
    return render(request, 'users/login.html', {"message": "New user log in"})

def main_screen(request):
    return render(request, 'TheCreche/mainscreen.html')

def thisWeek(request):

    #now = datetime.now()
    #today= datetime.today()
    #start = now - timedelta(days=(today.isoweekday() % 7)-1)

    kids = Child.objects.all()
        
    # holder for kids in each slot, starting 8-9, hourly
    monday={8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0}
    tuesday={8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0}
    wednesday={8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0}
    thursday={8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0}
    friday={8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0}
    saturday={8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0}

    # get next child
    for kid in kids:

        if kid.active:

            # get childs times
            days={
                'monday':[kid.mondaystart.strftime("%H"), kid.mondayfinish.strftime("%H"), 
                kid.mondaystart.strftime("%M"), kid.mondayfinish.strftime("%M")],
                'tuesday':[kid.tuesdaystart.strftime("%H"), kid.tuesdayfinish.strftime("%H"), 
                kid.tuesdaystart.strftime("%M"), kid.tuesdayfinish.strftime("%M")], 
                'wednesday':[kid.wednesdaystart.strftime("%H"), kid.wednesdayfinish.strftime("%H"),
                kid.wednesdaystart.strftime("%M"), kid.wednesdayfinish.strftime("%M")],
                'thursday':[kid.thursdaystart.strftime("%H"), kid.thursdayfinish.strftime("%H"),
                kid.thursdaystart.strftime("%M"), kid.thursdayfinish.strftime("%M")],
                'friday':[kid.fridaystart.strftime("%H"), kid.fridayfinish.strftime("%H"),
                kid.fridaystart.strftime("%M"), kid.fridayfinish.strftime("%M")],
                'saturday':[kid.saturdaystart.strftime("%H"), kid.saturdayfinish.strftime("%H"),
                kid.saturdaystart.strftime("%M"), kid.saturdayfinish.strftime("%M")]
                }

            # for each day, get childs start and finish times
            for key, day in days.items():
                    
                # calculate total hours in
                hourin = day[0]
                hourout = day[1]
                hours = int(hourout)-int(hourin)

                # ... and total mins in 
                minin  = day[2]
                minout  = day[3]
                
                if int(minout) == 0:
                    minout = 60
                    hours = hours-1

                mins = (int(minout)-int(minin))/100
                    
                # record how many hourly slots there are
                slots = int((hours+1) + mins)
                
                # record starting time
                time = int(hourin)-1

                # for each hourly slot
                for slot in range(slots+1):

                    if slot > 0:

                    # increment total for this slot 
                        eval(key)[time] +=1  
                    
                    
                    # move on to next slot
                    time +=1

    if request.POST.get("vaccancies"):

        weekdays =['monday','tuesday','wednesday','thursday', 'friday', 'saturday']

        for keys in weekdays: # 'monday', 'tuesday', etc

            for key in eval(keys): # 08, 09 etc

                eval(keys)[key] = 6-eval(keys)[key]

        context = {   
            "kids": kids,
            "monday":monday,
            "tuesday":tuesday,
            "wednesday":wednesday,
            "thursday":thursday,
            "friday":friday,
            "saturday":saturday    
            }
        
        return render(request, 'TheCreche/vaccancies.html', context)

    else:
    
        
        context = {   
            #"start": start.strftime("%A %d %B %Y"),
            #"today": today.strftime("Y-m-d"),
            "kids": kids,
            "monday":monday,
            "tuesday":tuesday,
            "wednesday":wednesday,
            "thursday":thursday,
            "friday":friday,
            "saturday":saturday    
        }
        
        return render(request, 'TheCreche/thisWeek.html', context)

    endif    

def menu(request):

    context = {
        "menu": Menu.objects.all(),
        "monday_morning": Menu.objects.filter(mealtime="AM",day="MON"),
        "monday_meals": Menu.objects.filter(day="MON"),
        "morning_meals": Menu.objects.order_by("id").filter(mealtime='AM'),
        "lunch_meals": Menu.objects.order_by("id").filter(mealtime='MD'),
        "afternoon_meals": Menu.objects.order_by("id").filter(mealtime='PM'),
        "ordered":Menu.objects.order_by("id").filter(mealtime="AM")
    }
    return render(request, 'Menu/menu.html', context)

def updatemenu(request):
    return render(request, 'Menu/update_menu.html')

def newmenu(request):

    day = request.POST["day"].upper() # changes input to upper case
    day = day[:3] ## reduces weekday to 3 letters, as per model
    
    mealtime = request.POST["mealtime"]  
    if mealtime == "morning":
        mealtime = "AM"
    elif mealtime == "lunch":
        mealtime = "MD"
    else:
        mealtime = "PM"

    meal = request.POST["meal"]
    
    try:
        testmeal = Menu.objects.get(day=day, mealtime=mealtime)
        testmeal.content = meal
        testmeal.save()
    except Menu.DoesNotExist:
        testmeal = Menu.objects.create(day=day, mealtime=mealtime, content =meal)

    return HttpResponseRedirect(reverse("menu"))
    return render(request, 'Menu/menu.html')

# HOLIDAYS

def holidays(request):
    
    now = datetime.now()
    year = now.year
    nextyear = year + 1
    display = year

    context = {   
        "year": year,
        "nextyear": nextyear,
        "hols": Holidays.objects.all(),
        "displayYear": display
        
    }
    return render(request, 'Holidays/holidays.html', context)
# holidays - Next year view
def holidaysNextYear(request):
    
    now = datetime.now()
    year = now.year
    nextyear = year + 1
    display = year

    context = {   
        "year": year,
        "nextyear": nextyear,
        "hols": Holidays.objects.all(),
        "displayYear": display
        
    }
    return render(request, 'Holidays/holidaysNextYear.html', context)
# holidays - Update button
def holidaysUpdate(request):
    return render(request, 'Holidays/holidaysUpdate.html')
# holidays - update button - option selection
def holidaysUpdateAction(request):
    userselected = request.POST.get('holidayupdate')
    holidays = Holidays.objects.all()
    
    context = {
        "holidays": holidays
    }
    
    if userselected == 'addholiday':
        return render(request, 'Holidays/addHoliday.html')
    elif userselected == 'removeholiday':
        return render(request, 'Holidays/removeHoliday.html', context)
    else:
        return render(request, 'Holidays/changeHolidayDates.html', context)

# holidays - update button screen - add a holiday form
def addHoliday(request):
    
    datefrom = request.POST["addfrom"]
    dateto = request.POST["addto"]
    holidayname = request.POST["addname"]
        
    newholiday = Holidays(holiday=holidayname, datefrom=datefrom, dateto=dateto)
    newholiday.save()

    return HttpResponseRedirect(reverse("holidays"))
    
# holidays - adding the new holiday to the database
def newHoliday(request):

    datefrom = request.POST["addfrom"]
    dateto = request.POST["addto"]
    holidayname = request.POST["addname"]
        
    newholiday = Holidays(holiday=holidayname, datefrom=datefrom, dateto=dateto)
    newholiday.save()

    return HttpResponseRedirect(reverse("holidays"))
    return render(request, 'Holidays/holidays.html')

# holidays - removing holiday from database
def removeHoliday(request):
    toRemove = request.POST.get("holiday")
    
    holidays = Holidays.objects.all()

    holiday = Holidays.objects.get(id = int(toRemove))
    holiday.delete()

    return HttpResponseRedirect(reverse("holidays")) # use when no 'Context'
    #return render(request, 'holidays.html')  # use to render context

# holidays - changing existing holiday dates - selecting holiday to change
def changeDates(request):
    toChange = request.POST.get("holiday")
    holidays = Holidays.objects.all()

    holiday = Holidays.objects.get(id = int(toChange))
    
    context = {
        "toChange" : toChange,
        "holiday" : holiday
    }

    return render(request, 'Holidays/updateHoliday.html', context)
# holidays - changing existing holiday dates - selecting and saving new dates
def updateHoliday(request):
    
    id = request.POST.get("id")
    
    datefrom = request.POST["fromDate"]
    dateto = request.POST["toDate"]

    holidays = Holidays.objects.all()

    holiday = Holidays.objects.get(id = int(id))

    holiday.datefrom = datefrom
    holiday.dateto = dateto
    holiday.save()

    return HttpResponseRedirect(reverse("holidays"))

def paperwork(request):
    return render(request, 'Documents/paperwork.html')

def popup(request):
    return render(request, 'popup.html')

def vaccancies(request):
    #now = datetime.now()
    #today= datetime.today()

    #start = now - timedelta(days=(today.isoweekday() % 7)-1) 
    
    monday = request.POST["monday"]
    #tuesday = request.POST["tuesday"]
    #wednesday = request.POST["wednesday"]
    #thursday = request.POST["thursday"]
    #friday = request.POST["friday"]
    #saturday = request.POST["saturday"]
    
    context = {   
        #"start": start.strftime("%A %d %B %Y"),
        "monday": monday
     #   "tuesday": tuesday,
      #  "wednesday": wednesday,
       # "thursday": thursday,
        #"friday": friday,
        #"saturday": saturday
    }

    return render(request, 'TheCreche/vaccancies.html', context)

def otherServices(request):
    return render(request, 'otherServices.html')    
