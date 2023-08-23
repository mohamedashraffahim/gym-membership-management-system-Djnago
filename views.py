from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member
from .forms import *
from django.shortcuts import redirect
from collections.abc import Iterable
from datetime import datetime, timedelta


def index(request):
    template = loader.get_template('index.html')
    context = {
        'members': Member.objects.all(),
    }
    return HttpResponse(template.render(context, request))


# Edit a member in the database using form data submitted through POST method
def addDurationById(request, id):
    member = Member.objects.get(mId=id)
    member.expDate = member.regDate + timedelta(days=member.duration)
    if datetime(member.expDate.year, member.expDate.month, member.expDate.day) < datetime.now():
        member.isActive = False
    member.save()


def editMember(request, id, captain):
    member = Member.objects.get(mId=id)
    if (request.method == "POST"):
        form = addMember(request.POST, instance=member)
        if form.is_valid():
            form.save()
            addDurationById(True, id)
            return redirect('/display/'+captain)
    else:
        form = addMember(instance=member)
    return render(request, 'index.html', {'form': form})

# Delete a member from the database


def deleteMember(request, id, captain):
    member = Member.objects.get(mId=id)
    member.delete()
    return redirect('/display/'+captain)


global safar
safar = False


def displayCaptain(request, captain=0):
    total = 0
    warningList = []
    expList = []
    global safar
    members = Member.objects.all()
    captain = captain
    for member in Member.objects.all():
        if member.captain == captain and member.paymentCount == False and member.isActive == True:
            total += member.paid
        if member.captain == captain and member.isActive and int(member.expDate.strftime('%d'))-int(datetime.now().strftime('%d')) <= 3 and int(member.expDate.strftime('%m'))-int(datetime.now().strftime('%m')) == 0 and int(member.expDate.strftime('%y'))-int(datetime.now().strftime('%y')) == 0:
            warningList.append(member.mId)
        if datetime(member.expDate.year, member.expDate.month, member.expDate.day) < datetime.now():
            member.isActive = False
            member.save()
        if member.captain == captain and member.isActive == False:
            expList.append(member.mId)
    # if datetime.now().strftime("%d") == "04" and safar == False:
    #     for member in Member.objects.all():
    #         if member.captain == captain and member.paymentCount == False and member.isActive == True:
    #             member.paymentCount = True
    #             member.save()
    #             safar = True
    # if datetime.now().strftime("%d") != "04" and safar == True:
    #     safar = False
    # if searched:
    #     members = Member.objects.filter(mId__contains=searched)
    #     return render(request, 'display.html', {'searched': searched, 'members': members, 'captain': captain, 'total': total, 'warningList': warningList, 'expList': expList})
    return render(request, 'display.html', {'members': members, 'captain': captain, 'total': total, 'warningList': warningList, 'expList': expList})


# Deleting Total Count of every Captain
def deleteTotal(request, captain):
    for member in Member.objects.all():
        if member.captain == captain and member.paymentCount == False:
            member.paymentCount = True
            member.save()
    return redirect('/display/' + captain)

# renew memeber
def renew(request, id, captain):
    member = Member.objects.get(mId=id)
    if (request.method == "POST"):
        form = renewMember(request.POST, instance=member)
        if form.is_valid():
            member.isActive = True
            member.paymentCount = False
            form.save()
            member.expDate = datetime.now() + timedelta(days=member.duration)
            member.save()
            return redirect('/display/' + captain)
    else:
        form = renewMember(instance=member)
    return render(request, 'index.html', {'form': form})


# Add a new member to the database using form data submitted through POST method
def addDuration(request):
    member = Member.objects.last()
    member.expDate = member.regDate + timedelta(days=member.duration)
    if datetime(member.expDate.year, member.expDate.month, member.expDate.day) < datetime.now():
        member.isActive = False
    member.save()


def add(request):
    add = True
    if (request.method == "POST"):
        form = addMember(request.POST)
        if form.is_valid():
            form.save()
            addDuration(request=True)
            return redirect('/add')
        else:
            form = addMember()
    else:
        form = addMember()
    return render(request, 'index.html', {'form': form, 'add': add})

# Search member by Id
def searchMemberById(request, captain):
    members = Member.objects.all()
    if request.method == 'POST':
        searched = request.POST['mId']
        member = Member.objects.get(mId=searched)
        return render(request, 'display.html', {'member': member, 'members': members, 'captain':captain})
    return render(request, 'display.html', {'members': members, 'captain':captain})
