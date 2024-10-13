# Create your views here.
from datetime import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from User.models import Complaint, User
from django.contrib import messages
from django.utils import timezone


def admin_home(request):
    return render(request,'Admin/Admin_home.html')

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def view_registered_User(request):
    registered_User= User.objects.filter(vstatus=0)
    return render(request, 'Admin/view_registered_User.html', {'registered_User': registered_User})

def handle_user_registration(request, user_id, action):
    user = get_object_or_404(User, pk=user_id)

    if action == 'accept':
        user.vstatus = 1  
    elif action == 'reject':
        user.vstatus = -1 
    else:
        return redirect('Admin:view_registered_User')

    user.save()
    return redirect('Admin:view_registered_User')


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def complaint_list_admin(request):
    complaints = Complaint.objects.all()  
    return render(request, 'Admin/complaint_list_admin.html', {'complaints': complaints})


def respond_to_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        response = request.POST.get('response')
        if response:
            complaint.response = response
            complaint.status = 'resolved'  
            complaint.responded_at = timezone.now()  
            complaint.save()  
            messages.success(request, "Response submitted successfully.")
            return redirect('Admin:complaint_list_admin') 
    return render(request, 'Admin/respond_complaint.html', {'complaint': complaint})



