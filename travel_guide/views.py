from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout
import datetime
from django.db import IntegrityError
from django.contrib import messages
import folium
from django.core.exceptions import ValidationError

# Create your views here.
def notification():
    status = Status.objects.get(status='pending')
    new = Service_Man.objects.filter(status=status)
    count=0
    for i in new:
        count+=1
    d = {'count':count,'new':new}
    return d
def Home(request):
    user=""
    error=""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
    ser1 = Service_Man.objects.all()
    ser = Service_Category.objects.all()
    for i in ser:
        count=0
        for j in ser1:
            if i.category==j.service_name:
                count+=1
        i.total = count
        i.save()
    d = {'error': error, 'ser': ser}
    return render(request,'home.html',d)

def contact(request):
    error = False
    if request.method == "POST":
        n = request.POST['name']
        e = request.POST['email']
        m = request.POST['message']
        status = Status.objects.get(status="unread")
        # Analyze the sentiment of the message
        blob = TextBlob(m)
        sentiment_score = blob.sentiment.polarity
        # Create a new Contact object with the sentiment score
        Contact.objects.create(status=status, name=n, email=e, message1=m, sentiment_score=sentiment_score)
        error = True
    d = {'error': error}
    return render(request, 'contact.html', d)


def Admin_Home(request):
    dic = notification()
    cus = Customer.objects.all()
    ser = Service_Man.objects.all()
    cat = Service_Category.objects.all()
    count1=0
    count2=0
    count3=0
    for i in cus:
        count1+=1
    for i in ser:
        count2+=1
    for i in cat:
        count3+=1
    d = {'new':dic['new'],'count':dic['count'],'customer':count1,'service_man':count2,'service':count3}
    return render(request,'admin_home.html',d)

def about(request):
    return render(request,'about.html')

def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            try:
                sign = Customer.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "pat1"
            else:
                stat = Status.objects.get(status="Accept")
                pure=False
                try:
                    pure = Service_Man.objects.get(status=stat,user=user)
                except:
                    pass
                if pure:
                    login(request, user)
                    error = "pat2"
                else:
                    login(request, user)
                    error="notmember"

        else:
            error="not"
    d = {'error': error}
    return render(request, 'login.html', d)

def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            error="pat"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'admin_login.html', d)

def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['address']
        type = request.POST['type']
        im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        if type=="customer":
            Customer.objects.create(user=user,contact=con,address=add,image=im)
        else:
            stat = Status.objects.get(status='pending')
            Service_Man.objects.create(doj=dat,image=im,user=user,contact=con,address=add,status=stat)
        error = "create"
    d = {'error':error}
    return render(request,'signup.html',d)

def User_home(request):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        pass
    d = {'error':error}
    return render(request,'user_home.html',d)

def Service_home(request):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    terro=""
    if None == sign.service_name:
        terro = "message"
    else:
        if sign.status.status == "pending":
            terro="message1"
    d = {'error':error,'terro':terro}
    return render(request,'service_home.html',d)

def Service_Order(request):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    terro=""
    if None == sign.service_name:
        terro = "message"
    else:
        if sign.status.status == "pending":
            terro="message1"
    order = Order.objects.filter(service=sign)
    d = {'error':error,'terro':terro,'order':order}
    return render(request,'service_order.html',d)

def Admin_Order(request):
    dic = notification()
    order = Order.objects.all()
    d = {'order':order,'new': dic['new'], 'count': dic['count']}
    return render(request,'admin_order.html',d)

def Customer_Order(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    order = Order.objects.filter(customer=sign)
    d = {'error': error, 'order': order}
    return render(request, 'customer_order.html', d)


# def Customer_Booking(request,pid):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     user= User.objects.get(id=request.user.id)
#     error=""
#     try:
#         sign = Customer.objects.get(user=user)
#         error = "pat"
#     except:
#         sign = Service_Man.objects.get(user=user)
#         pass
#     terror=False
#     ser1 = Service_Man.objects.get(id=pid)
#     if request.method == "POST":
#         n = request.POST['name']
#         c = request.POST['contact']
#         add = request.POST['add']
#         dat = request.POST['date']
#         da = request.POST['day']
#         # ho = request.POST['hour']
#         st = Status.objects.get(status="pending")
#         Order.objects.create(status=st,service=ser1,customer=sign,book_date=dat,book_days=da)
#         terror=True
#     d = {'error':error,'ser':sign,'terror':terror}
#     return render(request,'booking.html',d)



# def Customer_Booking(request,pid):
#     if not request.user.is_authenticated:
#         return redirect('login')
    # user = request.user
    # error = ""
    # try:
    #     sign = Customer.objects.get(user=user)
    #     error = "pat"
    # except:
    #     sign = Service_Man.objects.get(user=user)
    #     pass
    # terror = False
    # ser1 = Service_Man.objects.get(id=pid)
    # if request.method == "POST":
    #     n = request.POST['name']
    #     c = request.POST['contact']
    #     add = request.POST['add']
    #     dat = request.POST['date']
    #     da = request.POST['day']
    #     # ho = request.POST['hour']
    #     st = Status.objects.get(status="pending")
        
        # Check if the service is already booked on the selected date
    #     existing_orders = Order.objects.filter(service=ser1, book_date=dat)

    #     if existing_orders.exists():
    #         raise ValidationError("The selected date is not available")
        
    #     Order.objects.create(status=st, service=ser1, customer=sign, book_date=dat, book_days=da)
    #     terror = True
    # d = {'error': error, 'ser': sign, 'terror': terror}
    # return render(request, 'booking.html', d)
    # existing_orders = Order.objects.filter(service=ser1, book_date=dat)

    # if existing_orders.exists():
    #     message = "The selected date is not available. Please choose a different date."
    # else:
    #     Order.objects.create(status=st, service=ser1, customer=sign, book_date=dat, book_days=da)
    #     terror = True
    #     message = "Your booking has been confirmed!"

    # d = {'error': error, 'ser': sign, 'terror': terror, 'message': message}
    # return render(request, 'booking.html', d)

def Customer_Booking(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    terror = False
    ser1 = Service_Man.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['name']
        c = request.POST['contact']
        add = request.POST['add']
        dat = request.POST['date']
        da = request.POST['day']
        # ho = request.POST['hour']
        st = Status.objects.get(status="pending")
        
        # Check if the service is already booked on the selected date
        existing_orders = Order.objects.filter(service=ser1, book_date=dat)

        if existing_orders.exists():
            raise ValidationError("The selected date is not available")
        
        Order.objects.create(status=st, service=ser1, customer=sign, book_date=dat, book_days=da)
        terror = True
    d = {'error': error, 'ser': sign, 'terror': terror}
    return render(request, 'booking.html', d) 


def Booking_detail(request,pid):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    order = Order.objects.get(id=pid)
    d = {'error':error,'order':order}
    return render(request,'booking_detail.html',d) 

def All_Service(request):
    user = ""
    error = ""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
    ser1 = Service_Man.objects.all()
    ser = Service_Category.objects.all()
    for i in ser:
        count=0
        for j in ser1:
            if i.category==j.service_name:
                count+=1
        i.total = count
        i.save()
    d = {'error': error,'ser':ser}
    return render(request,'services.html',d)

def Explore_Service(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    user = ""
    error = ""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
    ser = Service_Category.objects.get(id=pid)
    sta = Status.objects.get(status="Accept")
    order = Service_Man.objects.filter(service_name=ser.category,status=sta)
    d = {'error': error,'ser':ser,'order':order}
    return render(request,'explore_services.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

def Edit_Profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image=i
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        sign.address = ad
        sign.contact=con
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        sign.save()
        terror = True
    d = {'terror':terror,'error':error,'pro':sign,'ser':ser}
    return render(request, 'edit_profile.html',d)

def Edit_Service_Profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    car = ID_Card.objects.all()
    city = City.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image=i
            sign.save()
        except:
            pass
        try:
            i1 = request.FILES['image1']
            sign.id_card=i1
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        se = request.POST['service']
        card = request.POST['card']
        cit = request.POST['city']
        ex = request.POST['exp']
        dob = request.POST['dob']
        if dob:
            sign.dob=dob
            sign.save()
        ci=City.objects.get(city=cit)
        sign.address = ad
        sign.contact=con
        sign.city=ci
        user.first_name = f
        user.last_name = l
        user.email = e
        sign.id_type = card
        sign.experience = ex
        sign.service_name = se
        user.save()
        sign.save()
        terror = True
    d = {'city':city,'terror':terror,'error':error,'pro':sign,'car':car,'ser':ser}
    return render(request, 'edit_service_profile.html',d)

def Edit_Admin_Profile(request):
    dic = notification()
    error = False
    user = User.objects.get(id=request.user.id)
    pro = Customer.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            pro.image=i
            pro.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        pro.address = ad
        pro.contact=con
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        pro.save()
        error = True
    d = {'error':error,'pro':pro,'new': dic['new'], 'count': dic['count']}
    return render(request, 'edit_admin_profile.html',d)

def profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    d = {'pro':sign,'error':error}
    return render(request,'profile.html',d)

def service_profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    d = {'pro':sign,'error':error}
    return render(request,'service_profile.html',d)

def admin_profile(request):
    dic = notification()
    user = User.objects.get(id=request.user.id)
    pro = Customer.objects.get(user=user)
    d = {'pro':pro,'new': dic['new'], 'count': dic['count']}
    return render(request,'admin_profile.html',d)

def Change_Password(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        pass
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'error':error,'terror':terror}
    return render(request,'change_password.html',d)

def Admin_Change_Password(request):
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'terror':terror}
    return render(request,'admin_change_password.html',d)

def New_Service_man(request):
    dic = notification()
    status = Status.objects.get(status="pending")
    ser = Service_Man.objects.filter(status=status)
    d = {'ser':ser,'new': dic['new'], 'count': dic['count']}
    return render(request,'new_service_man.html',d)

def All_Service_man(request):
    dic = notification()
    ser = Service_Man.objects.all()
    d = {'ser':ser,'new': dic['new'], 'count': dic['count']}
    return render(request,'all_service_man.html',d)

def All_Customer(request):
    dic = notification()
    ser = Customer.objects.all()
    d = {'ser':ser,'new': dic['new'], 'count': dic['count']}
    return render(request,'all_customer.html',d)

def Add_Service(request):
    dic = notification()
    error=False
    if request.method == "POST":
        n = request.POST['cat']
        i = request.FILES['image']
        de = request.POST['desc']
        Service_Category.objects.create(category=n,image=i,desc=de)
        error=True
    d = {'error':error,'new': dic['new'], 'count': dic['count']}
    return render(request,'add_service.html',d)

def Add_City(request):
    dic = notification()

    if request.method == "POST":
        city_name = request.POST['cat']
        try:
            City.objects.create(city=city_name)
            messages.success(request, f'The city "{city_name}" was added successfully.')
        except IntegrityError:
            messages.error(request, f'The city "{city_name}" already exists.')

        return redirect('add_city')

    context = {
        'new': dic['new'],
        'count': dic['count'],
    }

    return render(request, 'add_city.html', context)

def Edit_Service(request,pid):
    dic = notification()
    error=False
    ser = Service_Category.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['cat']
        try:
            i = request.FILES['image']
            ser.image = i
            ser.save()
        except:
            pass
        de = request.POST['desc']
        ser.category = n
        ser.desc = de
        ser.save()
        error=True
    d = {'error':error,'ser':ser,'new': dic['new'], 'count': dic['count']}
    return render(request,'edit_service.html',d)

def View_Service(request):
    dic = notification()
    ser = Service_Category.objects.all()
    d = {'ser':ser,'new': dic['new'], 'count': dic['count']}
    return render(request,'view_service.html',d)

def View_City(request):
    dic = notification()
    ser = City.objects.all()
    d = {'ser':ser,'new': dic['new'], 'count': dic['count']}
    return render(request,'view_city.html',d)

def accept_confirmation(request,pid):
    ser = Order.objects.get(id=pid)
    sta = Status.objects.get(status='Accept')
    ser.status = sta
    ser.save()
    return redirect('service_order')

def confirm_message(request,pid):
    ser = Contact.objects.get(id=pid)
    sta = Status.objects.get(status='read')
    ser.status = sta
    ser.save()
    return redirect('new_message')

def delete_service(request,pid):
    ser = Service_Category.objects.get(id=pid)
    ser.delete()
    return redirect('view_service')

def delete_city(request,pid):
    ser = City.objects.get(id=pid)
    ser.delete()
    return redirect('view_city')

def delete_admin_order(request,pid):
    ser = Order.objects.get(id=pid)
    ser.delete()
    return redirect('admin_order')

def delete_Booking(request,pid):
    ser = Order.objects.get(id=pid)
    ser.delete()
    return redirect('customer_order')

def delete_service_man(request,pid):
    ser = Service_Man.objects.get(id=pid)
    ser.delete()
    return redirect('all_service_man')

def delete_customer(request,pid):
    ser = Customer.objects.get(id=pid)
    ser.delete()
    return redirect('all_customer')

def Change_status(request,pid):
    dic = notification()
    error = False
    pro1 = Service_Man.objects.get(id=pid)
    if request.method == "POST":
        stat = request.POST['stat']
        sta = Status.objects.get(status=stat)
        pro1.status=sta
        pro1.save()
        error=True
    d = {'pro':pro1,'error':error,'new': dic['new'], 'count': dic['count']}
    return render(request,'status.html',d)

def Order_status(request,pid):
    dic = notification()
    error = False
    pro1 = Order.objects.get(id=pid)
    if request.method == "POST":
        stat = request.POST['stat']
        sta = Status.objects.get(status=stat)
        pro1.status=sta
        pro1.save()
        error=True
    d = {'pro':pro1,'error':error,'new': dic['new'], 'count': dic['count']}
    return render(request,'order_status.html',d)

def Order_detail(request,pid):
    dic = notification()
    pro1 = Order.objects.get(id=pid)
    d = {'pro':pro1,'new': dic['new'], 'count': dic['count']}
    return render(request,'order_detail.html',d)

def service_man_detail(request,pid):
    dic = notification()
    pro1 = Service_Man.objects.get(id=pid)
    d = {'pro':pro1,'new': dic['new'], 'count': dic['count']}
    return render(request,'service_man_detail.html',d)

def search_cities(request):
    error=""
    try:
        user = User.objects.get(id=request.user.id)
        error = ""
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
    dic = notification()
    terror=False
    pro=""
    car = City.objects.all()
    count1=0
    car1 = Service_Category.objects.all()
    c=""
    c1=""
    if request.method=="POST":
        c=request.POST['city']
        c1 = request.POST['cat']
        ser = City.objects.get(city=c)
        ser1 = Service_Category.objects.get(category=c1)
        pro = Service_Man.objects.filter(service_name=ser1,city=ser)
        for i in pro:
            count1+=1
        terror = True
    d = {'c':c,'c1':c1,'count1':count1,'car1':car1,'car':car,'order':pro,'new': dic['new'], 'count': dic['count'],'error':error,'terror':terror}
    return render(request,'search_cities.html',d)

def search_services(request):
    dic = notification()
    error=False
    pro=""
    car = Service_Category.objects.all()
    c=""
    if request.method=="POST":
        c=request.POST['cat']
        ser = Service_Category.objects.get(category=c)
        pro = Service_Man.objects.filter(service_name=ser)
        error=True
    d = {'service':c,'car':car,'order':pro,'new': dic['new'], 'count': dic['count'],'error':error}
    return render(request,'search_services.html',d)

def new_message(request):
    dic = notification()
    sta = Status.objects.get(status='unread')
    pro1 = Contact.objects.filter(status=sta)
    d = {'ser':pro1,'new': dic['new'], 'count': dic['count']}
    return render(request,'new_message.html',d)

def read_message(request):
    dic = notification()
    sta = Status.objects.get(status='read')
    pro1 = Contact.objects.filter(status=sta)
    d = {'ser':pro1,'new': dic['new'], 'count': dic['count']}
    return render(request,'read_message.html',d)

def Search_Report(request):
    dic = notification()
    status = Status.objects.get(status="pending")
    reg1 = Order.objects.filter(status=status)
    total = 0
    for i in reg1:
        total += 1
    data = Order.objects.all( )
    error = ""
    terror = ""
    reg=""
    if request.method == "POST":
        terror="found"
        i = request.POST['date1']
        n = request.POST['date2']
        i1 = datetime.datetime.fromisoformat(i).month
        i2 = datetime.datetime.fromisoformat(i).year
        i3 = datetime.datetime.fromisoformat(i).day
        n1 = datetime.datetime.fromisoformat(n).month
        n2 = datetime.datetime.fromisoformat(n).year
        n3 = datetime.datetime.fromisoformat(n).day
        for j in data:
            d1 =j.book_date.month
            d2 =j.book_date.year
            d3 = j.book_date.day
            day3 = (d2 * 365) + (d1 * 30) + d3
            day1 = (i2 * 365) + (i1 * 30) + i3
            day2 = (n2 * 365) + (n1 * 30) + n3
            if day3 > day1 and day3 < day2:
                j.report_status = 'active'
                j.save()
            else:
                j.report_status = 'inactive'
                j.save()
        reg = Order.objects.filter(report_status="active")
        if not reg:
            error="notfound"
    d = {'new': dic['new'], 'count': dic['count'],'order':reg,'error':error,'terror':terror,'reg1': reg1, 'total': total}
    return render(request,'search_report.html',d)

def sentiment_analysis(request):
    contacts = Contact.objects.all()

    # Count the number of positive feedback
    positive_count = contacts.filter(sentiment_score__gt=0.5).count()

    # Count the number of negative feedback
    negative_count = contacts.filter(sentiment_score__lt=-0.5).count()

    # Count the number of neutral feedback
    neutral_count = contacts.filter(sentiment_score__lte=0.5, sentiment_score__gte=-0.5).count()

    context = {'positive_count': positive_count, 'negative_count': negative_count, 'neutral_count': neutral_count}
    return render(request, 'sentiment_analysis.html', context)

def map_view(request):
    # create a map centered on the first registered service man
    first_service_man = Service_Man.objects.first()
    map = folium.Map(location=[first_service_man.latitude, first_service_man.longitude], zoom_start=8)

    # add a marker for each registered service man with their image
    for service_man in Service_Man.objects.all():
        tooltip = f"{service_man.service_name} in {service_man.city.city}"
        popup_html = f"<div><img src='{service_man.image.url}' width='100px'><br>{service_man.service_name} in {service_man.city.city}</div>"
        folium.Marker(location=[service_man.latitude, service_man.longitude], tooltip=tooltip, popup=popup_html).add_to(map)

    return render(request, 'map.html', {'map': map._repr_html_()})


def feedback(request, pid):
    order = Order.objects.get(id=pid)
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        service_man = order.service
        customer = order.customer
        feedback = Feedback.objects.create(service_man=service_man, customer=customer, feedback_text=feedback_text)
        rating = Rating.objects.create(service_man=service_man, customer=customer, rating=rating)
        return redirect('Booking_detail', pid=pid)
    else:
        d = {'order': order}
        return render(request, 'feedback.html', d)
    