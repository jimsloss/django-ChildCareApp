from django.shortcuts import render, redirect
from django.urls import reverse
from child.models import Child
from child.models import Parent
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
import datetime
from datetime import date
import os #to use opening file path

def childview(request):

    id = request.GET.get("name") 

    child = Child.objects.first()
    child = Child.objects.get(pk=id)
    
    field_object = Child._meta.get_field('firstname')
    field_value1 = field_object.value_from_object(child)
   
    field_object = Child._meta.get_field('surname')
    field_value2 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('dateofbirth')
    field_value3 = field_object.value_from_object(child)
    
    field_object = Child._meta.get_field('childphoto')
    field_value4 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('maincontact')
    field_value5 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('c1')
    field_value6 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('c2')
    field_value7 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('othercontact')
    field_value8 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('c3')
    field_value9 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('childgender')
    field_value10 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('childtype')
    field_value11 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('active')
    field_value12 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('dietry')
    field_value13 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('medical')
    field_value14 = field_object.value_from_object(child)

    field_object = Child._meta.get_field('address')
    field_value15 = field_object.value_from_object(child)

    # photo = request.POST["photo"]

    tab1 = "Main"
    tab2 = "Contacts"
    tab3 = "Dietry"
    tab4 = "Medical"
    tab5 = "Paperwork"

    def calculateAge(birthDate): 
        today = date.today() 
        age = today.year - birthDate.year - \
            ((today.month, today.day) < \
            (birthDate.month, birthDate.day)) 
        return age 
        
    age = calculateAge(field_value3)#, "years") 

    context = {
        "kids": Child.objects.all(),
        "child":child.pk,
        "id": id,
        "mondayS": child.mondaystart,
        "mondayF": child.mondayfinish,
        "tuesdayS": child.tuesdaystart,
        "tuesdayF": child.tuesdayfinish,
        "wednesdayS": child.wednesdaystart,
        "wednesdayF": child.wednesdayfinish,
        "thursdayS": child.thursdaystart,
        "thursdayF": child.thursdayfinish,
        "fridayS": child.fridaystart,
        "fridayF": child.fridayfinish,
        "saturdayS": child.saturdaystart,
        "saturdayF": child.saturdayfinish,
        
        "firstname": field_value1,
        "secondname": field_value2,
        "dob": field_value3,
        "age": age,
        
        "maincontact": field_value5,
        "c1": field_value6,
        "c2": field_value7,
        "othercontact": field_value8,
        "c3": field_value9,
        "gender": field_value10,
        "type": field_value11,
        "active": field_value12,
        #"photo": photo,
        "tab1": tab1,  # need these as list, didnt work
        "tab2": tab2,
        "tab3": tab3,
        "tab4": tab4,
        "tab5": tab5,
        "photo": field_value4.url,
        "dietry": field_value13,
        "medical": field_value14,
        "address": field_value15,
    }

    return render(request, 'Kids/viewChild.html', context)

def addChild(request):
    
    context = {
        "kids": Child.objects.all(),
        "parents": Parent.objects.all()
    }

    if 'addChild' in request.POST:
        return render(request, 'Kids/addChild.html', context)
    elif 'removeChild' in request.POST:
        request.session.get('kids')
        return render(request, 'Kids/removeChild.html', context)

def removeChild(request):

    toRemove = request.POST.get("child")
    
    kids = Child.objects.all()

    child = Child.objects.get(id = int(toRemove))
    child.delete()

    return HttpResponseRedirect(reverse("kids"))
    
def kids(request):
    context = {
        "kids": Child.objects.all()
        
    }
    return render(request, 'Kids/kids.html', context)
 

    # use 2 diff url/view


def newChild(request):
    if 'cancel' in request.POST:
        #return render(request, 'TheCreche/mainscreen.html')
        return redirect('/main') 

   # elif 'newPhoto' in request.POST:
    #    return render(request, 'media/images')
     #   module_dir = os.path.dirname(__file__)  # get current directory
        #file_path = os.path.join(module_dir, 'baz.txt')
      #  file = open(module_dir)

    elif 'continue' in request.POST:

        parent = Parent()
        parent.surname="blank"
        parent.save()

        newchild = Child(surname="surname", firstname="firstname", dateofbirth=date.today(), childgender="gender", childtype="type", \
        address="address", maincontact= "main", c1="c1", c2="c2", c3="c3", othercontact="other", active =True, parent=parent)#, childphoto="images/"+photo)
        
        newchild.surname = request.POST["surname"]
        newchild.firstname = request.POST["firstname"]
        newchild.dateofbirth = request.POST["dob"]
        newchild.childgender = request.POST["childgender"]
        
        address = request.POST["address"]
        
        if address == "":
            address ="Address not provided"
        
        newchild.address = address

        photo = request.POST["newPhoto"]

        if photo =="":
            photo = "no boy photo"
       
        newchild.childphoto = "images/" + photo
    
        newchild.save()

        context = {
            "id" : newchild.id
        }
        
        return render(request, 'Kids/addChildpart2.html', context)
       
def newChild2(request):

    newchild = request.POST["childID"]
    child = Child.objects.get(pk=newchild)

    if 'cancel' in request.POST:
        
        child.delete()
        parent = Parent.objects.get(pk=child.parent.id)
        parent.delete()
        
        #return render(request, 'TheCreche/mainscreen.html')
        return redirect('/main') 
        
    elif 'continue' in request.POST:
        
        maincontact = request.POST["maincontact"]
        c1 = request.POST["c1"]
        c2 = request.POST["c2"]
        othercontact = request.POST["othercontact"]
        c3 = request.POST["c3"]    

        if maincontact == "": maincontact = 00000000000
        if c1 == "": c1 = 00000000000
        if c2 == "": c2 = 00000000000
        if othercontact == "": othercontact = 00000000000
        if c3 == "": c3 = 00000000000

        child.maincontact = maincontact
        child.c1 = c1
        child.c2 = c2
        child.othercontact = othercontact
        child.c3 = c3    

        context = {
            "id" : child.id
        }
        
        child.save()
        return render(request, 'Kids/addChildpart3.html', context)

def newChild3(request):
    
    newchild = request.POST["childID"]
    child = Child.objects.get(pk=newchild)

    if 'cancel' in request.POST:
        
        child.delete()
        parent = Parent.objects.get(pk=child.parent.id)
        parent.delete()
        
        #return render(request, 'TheCreche/mainscreen.html')
        return redirect('/main') 
        
    elif 'continue' in request.POST:

        monstart = child.mondaystart = request.POST["MonS"]
        monfinish = child.mondayfinish = request.POST["MonF"]
        tuestart = child.tuesdaystart = request.POST["TueS"]
        tuefinish = child.tuesdayfinish = request.POST["TueF"]
        wedstart = child.wednesdaystart = request.POST["WedS"]
        wedfinish = child.wednesdayfinish = request.POST["WedF"]
        thustart = child.thursdaystart = request.POST["ThuS"]
        thufinish = child.thursdayfinish = request.POST["ThuF"]
        fristart = child.fridaystart = request.POST["FriS"]
        frifinish = child.fridayfinish = request.POST["FriF"]
        satstart = child.saturdaystart = request.POST["SatS"]
        satfinish = child.saturdayfinish = request.POST["SatF"]
        
        days = [monstart,monfinish,tuestart,tuefinish,wedstart,wedfinish,thustart,thufinish,fristart,frifinish,satstart,satfinish]
        
        totaldays = 0

        for day in days:
            if day != "00:00":
                totaldays += 1
        
        child.daysperweek = totaldays/2

        childtype = request.POST["childtype"]
            
        #if childtype == "Full Time":
        #   childtype = "FT"
        #elif childtype == "Part Time":
        #   childtype = "PT"
        #elif childtype == "After School":
        #   childtype = "AS"
        #elif childtype == "Under 5":
        #   childtype = "U5"
        #else:
        #   childtype = "SO"

        child.childtype =childtype
        
            
        #attendance.save()
        #child.attendance = attendance

        child.save()
        
        parents = Parent.objects.all()
        totalparents = 0
        for parent in parents:
            totalparents +=1


        context={
            "id" : child.id,
            "parents": parents,
            "totalparents": totalparents,
        }

        return render(request, 'Kids/addChildpart4.html', context)

def newChild4(request):

    newchild = request.POST["childID"]
    child = Child.objects.get(pk=newchild)


    if 'cancel' in request.POST:
        
        child.delete()
        parent = Parent.objects.get(pk=child.parent.id)
        parent.delete()
        
        #return render(request, 'TheCreche/mainscreen.html')
        return redirect('/main') 
        
    elif 'continue' in request.POST:
        
        theParent = request.POST["parent"]


        context={
            "id" : child.id
            }
        
       
        if theParent == "New Parent":
            return render(request, 'Kids/addParent.html', context)    

        if theParent =="": 
            parent = "not supplied"
        
        parent = Parent.objects.get(pk=theParent)

        
        child.parent=parent
        child.save()

        parents = Parent.objects.all()
        for parent in parents:
            if parent.surname == "blank":
                parent.delete()
        
        

        return render(request, 'Kids/addChildpart5.html', context)

def newChild5(request):
    
    newchild = request.POST["childID"]
    print("#### newChild5 ID returned from html #####", newchild)
    
    
    child = Child.objects.get(pk=newchild)

    print("### view, newChild5 starting ###",child.id, child.firstname, child.surname, child.parent)

    if 'cancel' in request.POST:
        
        child.parent.delete()       
        
        #return render(request, 'TheCreche/mainscreen.html')
        return redirect('/main') 
        
    elif 'submit' in request.POST:
    
        medical = request.POST["medical"]

        dietry = request.POST["dietry"]
        
        context={
            "id" : child.id
        }
        
        child.medical=medical
        child.dietry=dietry        
        
        child.save()
        print("### after newChild5 finished ###",child.id, child.firstname, child.surname, child.parent)
    #   return render(request, 'TheCreche/mainscreen.html')
        
    return HttpResponseRedirect(reverse("kids"))
    #return render(request, 'Kids/kids.html')

def updateChild(request):

    id = request.POST["id"]
    
    child = Child.objects.get(pk=id)
    

    context = {
        "child": child,
        "id": id
        
    }
    return render(request, 'Kids/updateChild.html', context)

def updateChildPersonal(request):

    id = request.POST["childID"]

    child = Child.objects.get(pk=id)

    child.surname = request.POST["surname"]
    child.firstname = request.POST["firstname"]
    child.dateofbirth = request.POST["dob"]
    child.childgender = request.POST["gender"]
    
    child.childphoto = "images/" + request.POST["photo"]

    child.save()

    context = {
        "id": id,
        "child": child,
       
    }
    return render(request, 'Kids/updateContacts.html', context)

def updateChild3(request):

    id = request.POST["childID"]

    child = Child.objects.get(pk=id)

    child.childtype = request.POST["childtype"]

    child.mondaystart = request.POST["MonS"]
    child.mondayfinish = request.POST["MonF"]
    child.tuesdaystart = request.POST["TueS"]
    child.tuesdayfinish = request.POST["TueF"]
    child.wednesdaystart = request.POST["WedS"]
    child.wednesdayfinish = request.POST["WedF"]
    child.thursdaystart = request.POST["ThuS"]
    child.thursdayfinish = request.POST["ThuF"]
    child.fridaystart = request.POST["FriS"]
    child.fridayfinish = request.POST["FriF"]
    child.saturdaystart = request.POST["SatS"]
    child.saturdayfinish = request.POST["SatF"]
    
    child.save()

    context = {
        "child": child,
        "id": id,
    }
    return render(request, 'Kids/updateContacts.html', context)

def updateContacts(request):

    id = request.POST["childID"]

    child = Child.objects.get(pk=id)

    child.maincontact = request.POST["maincontact"]
    child.c1 = request.POST["c1"]
    child.c2 = request.POST["c2"]
    child.othercontact = request.POST["othercontact"]
    child.c3 = request.POST["c3"]
    
    
    
    child.save()

    context = {
        "child": child,
        "id": id,
        "mondayS": child.mondaystart,
        "mondayF": child.mondayfinish,
        "tuesdayS": child.tuesdaystart,
        "tuesdayF": child.tuesdayfinish,
        "wednesdayS": child.wednesdaystart,
        "wednesdayF": child.wednesdayfinish,
        "thursdayS": child.thursdaystart,
        "thursdayF": child.thursdayfinish,
        "fridayS": child.fridaystart,
        "fridayF": child.fridayfinish,
        "saturdayS": child.saturdaystart,
        "saturdayF": child.saturdayfinish
    }
    return render(request, 'Kids/updateAttendance.html', context)

def updateChildComplete(request):

    id = request.POST["childID"]
    
    child = Child.objects.get(pk=id)
    
    child.childtype = request.POST["childtype"]

    child.mondaystart = request.POST["MonS"]
    child.mondayfinish = request.POST["MonF"]
    child.tuesdaystart = request.POST["TueS"]
    child.tuesdayfinish = request.POST["TueF"]
    child.wednesdaystart = request.POST["WedS"]
    child.wednesdayfinish = request.POST["WedF"]
    child.thursdaystart = request.POST["ThuS"]
    child.thursdayfinish = request.POST["ThuF"]
    child.fridaystart = request.POST["FriS"]
    child.fridayfinish = request.POST["FriF"]
    child.saturdaystart = request.POST["SatS"]
    child.saturdayfinish = request.POST["SatF"]

    child.save()
    
    context = {
        "child": child,
        "id": id
        
    }
    return render(request, 'Kids/updateChildComplete.html', context)

def newParent(request):
        
    newchild = request.POST["childID"]
    child = Child.objects.get(pk=newchild)
    print("#### on entering new parent view #####",child.id, child.firstname, child.surname, child.parent)
    context={
            "id" : child.id,
            "parents" : Parent.objects.all()
        }

    if 'cancel' in request.POST:

        return render(request, 'Kids/addChildpart4.html', context)

        
    elif 'continue' in request.POST:
    
        newParent = Parent(surname=request.POST["surname"], firstname=request.POST["firstname"], relation=request.POST["relation"], 
        mainNumber=request.POST["mainNumber"], altNumber=request.POST["altNumber"], otherNumber=request.POST["otherNumber"])
        newParent.save()
        
        child.parent = newParent

        parents = Parent.objects.all()
        for parent in parents:
            if parent.surname == "blank":
                parent.delete()
        
        
        #child.parent.surname = request.POST["surname"]
        #child.parent.firstname = request.POST["firstname"]
        #child.parent.relation = request.POST["relation"]
        #child.parent.mainNumber = request.POST["mainNumber"]
        #child.parent.altNumber = request.POST["altNumber"]
        #newParent.otherContact = request.POST["othercontact"]
        #child.parent.otherNumber = request.POST["otherNumber"]
        print("### after new parent details entered ###",child.id, child.firstname, child.surname, child.parent)
        #childID = request.POST["childID"]
        #theChild = Child.objects.get(pk =childID)

        #newParent = Parent.objects.get(pk=newparent.id)
        #parentName = request.POST["firstname"] + " " + request.POST["surname"]

        
        child.save()
        print("### after new parent saved ###",child.id, child.firstname, child.surname, child.parent)
        
       # return HttpResponseRedirect(reverse("kids"))
        #return render(request, 'Kids/kids.html')
        context2={
            "id" : child.id,
        }
        print("### after context2  ###",child.id, child.firstname, child.surname, child.parent)
       
        return render(request, 'Kids/addChildpart5.html', context2)
