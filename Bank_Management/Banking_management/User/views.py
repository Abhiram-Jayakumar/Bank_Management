from datetime import timezone
from django.shortcuts import redirect, render
from django.contrib import messages
from decimal import Decimal
from Admin.models import Admintable
from .models import Complaint, Transaction, User
# Create your views here.


def index(request):
    return render(request,'User/index.html')

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def user_home(request):
    return render(request,'User/user_home.html')

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pan = request.POST.get('pan')
        adhaar = request.POST.get('adhaar')
        account_type = request.POST.get('account_type')
        password = request.POST.get('password')

        if not all([username, full_name, phone_number, email, address, pan, adhaar, account_type, password]):
            messages.error(request, 'Please fill out all required fields.')
            return render(request, 'User/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'User/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'User/register.html')

        user = User(
            username=username,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            address=address,
            password=password,
            Pan=pan,
            Adhaar=adhaar,
            account_type=account_type,
        )
        user.save()  

        messages.success(request, 'Your account has been created successfully!')
        return redirect('User:login') 
    
    return render(request, 'User/register.html')


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        Ulogin=User.objects.filter(email=email,password=password,vstatus=True).count()
        Alogin=Admintable.objects.filter(email=email,password=password).count()


        if Ulogin > 0:
            uadmin=User.objects.get(email=email,password=password,vstatus=1)
            request.session['Uid']=uadmin.id
            return redirect('User:user_home')
        elif Alogin > 0:
            Aadmin=Admintable.objects.get(email=email,password=password)
            request.session['Aid']=Aadmin.id
            return redirect('Admin:admin_home')
        
        else:
            error="Invalid Credentials!!"
            return render(request,"User/Login.html",{'ERR':error})
    else:
        return render(request, "User/Login.html")
    
    


#////////////////////////////////////////////////////////////////////////

def user_profile(request):
    if 'Uid' in request.session:
        user_id = request.session['Uid']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('User:login')

        return render(request, 'User/profile.html', {'user': user})
    else:
        messages.error(request, "You must be logged in to view your profile.")
        return redirect('User:login')
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    

def deposit(request):
    if 'Uid' not in request.session:
        messages.error(request, "You need to be logged in to make a deposit.")
        return redirect('User:login')

    if request.method == 'POST':
        amount = request.POST.get('amount')
        
        if not amount or Decimal(amount) <= 0:
            messages.error(request, "Please enter a valid amount.")
            return render(request, 'User/deposit.html')

        user = User.objects.get(id=request.session['Uid'])
        
        deposit_amount = Decimal(amount)
        
        user.balance += deposit_amount 
        user.save()

        transaction = Transaction(
            user=user,
            transaction_type='credit',
            amount=deposit_amount,
            balance_amount=user.balance,
            credit_amount=deposit_amount,
        )
        transaction.save()

        messages.success(request, "Deposit successful!")
        return redirect('User:user_profile') 
    return render(request, 'User/deposit.html')

#////////////////////////////////////////////////////////////////////////////

def transfer(request):
    if 'Uid' not in request.session:
        messages.error(request, "You need to be logged in to transfer money.")
        return redirect('User:login')

    user = User.objects.get(id=request.session['Uid'])

    if request.method == 'POST':
        recipient_account_number = request.POST.get('recipient_account_number')
        transfer_amount = request.POST.get('amount')

        if not transfer_amount or Decimal(transfer_amount) <= 0:
            messages.error(request, "Please enter a valid amount.")
            return render(request, 'User/transfer.html', {'user': user})  
        try:
            recipient = User.objects.get(account_number=recipient_account_number)
        except User.DoesNotExist:
            messages.error(request, "Recipient account number is invalid.")
            return render(request, 'User/transfer.html', {'user': user}) 

        if recipient.vstatus == 0:
            messages.error(request, "Recipient's account is not approved.")
            return render(request, 'User/transfer.html', {'user': user})  

        transfer_amount = Decimal(transfer_amount)

        if user.balance < transfer_amount:
            messages.error(request, "Insufficient balance for this transaction.")
            return render(request, 'User/transfer.html', {'user': user})  

        user.balance -= transfer_amount
        recipient.balance += transfer_amount

        user.save()
        recipient.save()

        Transaction.objects.create(
            user=user,
            transaction_type='debit',
            amount=transfer_amount,
            balance_amount=user.balance,
            debit_amount=transfer_amount,
        )

        Transaction.objects.create(
            user=recipient,
            transaction_type='credit',
            amount=transfer_amount,
            balance_amount=recipient.balance,
            credit_amount=transfer_amount,
        )

        messages.success(request, "Transfer successful!")
        return redirect('User:user_profile')  

    return render(request, 'User/transfer.html', {'user': user})  


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

from django.http import JsonResponse

def get_user_details(request):
    if request.method == 'GET':
        account_number = request.GET.get('account_number')
        try:
            user = User.objects.get(account_number=account_number)
            if user.vstatus == 1: 
                return JsonResponse({
                    'success': True,
                    'full_name': user.full_name,
                    'email': user.email
                })
            else:
                return JsonResponse({'success': False, 'message': "User account not approved."})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': "User does not exist."})

    return JsonResponse({'success': False, 'message': "Invalid request."})


#//////////////////////////////////////////////////////////////////////////////////////////////////////////

def transaction_details(request):
    if 'Uid' not in request.session:
        messages.error(request, "You need to be logged in to view transaction details.")
        return redirect('User:login')

    user = User.objects.get(id=request.session['Uid'])
    
    transactions = Transaction.objects.filter(user=user).order_by('-timestamp') 

    return render(request, 'User/transaction_details.html', {'user': user, 'transactions': transactions})


#////////////////////////////////////////////////////////////////////////////////////////////////////////////


def register_complaint(request):
    if 'Uid' not in request.session:
        messages.error(request, "You need to be logged in to register a complaint.")
        return redirect('User:login')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        complaint = Complaint.objects.create(
            user=User.objects.get(id=request.session['Uid']),
            title=title,
            description=description
        )
        messages.success(request, "Complaint registered successfully!")
        return redirect('User:complaint_list')  

    return render(request, 'User/register_complaint.html') 

def complaint_list(request):
    if 'Uid' not in request.session:
        messages.error(request, "You need to be logged in to view your complaints.")
        return redirect('User:login')

    user = User.objects.get(id=request.session['Uid'])
    complaints = Complaint.objects.filter(user=user).order_by('-created_at') 

    return render(request, 'User/complaint_list.html', {'complaints': complaints})


#/////////////////////////////////////////////////////////////////////////////////////////////////////

def update_password(request):
    if 'Uid' not in request.session:
        messages.error(request, "You need to be logged in to update your password.")
        return redirect('User:login')

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = User.objects.get(id=request.session['Uid'])

        if user.password != current_password:
            messages.error(request, "Current password is incorrect.")
            return render(request, 'User/update_password.html')

        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return render(request, 'User/update_password.html')

        user.password = new_password
        user.save()

        messages.success(request, "Password updated successfully!")
        return redirect('User:user_profile')

    return render(request, 'User/update_password.html')