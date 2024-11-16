from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
#///////////////////////INSTITTUTION REGISTER//////////////////
from django.shortcuts import render, redirect
from account.models import Institute
from django.contrib import messages

def institute_create(request):
    if request.method == 'POST':
        inst_name = request.POST.get('inst_name')
        code = request.POST.get('code')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        registration_number = request.POST.get('registration_number')
        established_date = request.POST.get('established_date')
        contact_person = request.POST.get('contact_person')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        number_of_students = request.POST.get('number_of_students')
        
        institute = Institute.objects.create(
            inst_name=inst_name,
            code=code,
            email=email,
            address=address,
            status="pending",
            phone=phone,
            registration_number=registration_number,
            established_date=established_date if established_date else None,
            contact_person=contact_person,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            number_of_students=number_of_students if number_of_students else None
        )
        try:
            institute.save()
            messages.success(request, "Institute registered successfully.")
            return redirect('institute_create')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    
    return render(request, 'add_institute.html')



def institute_list(request):
    institutes = Institute.objects.all()
    return render(request, 'admin/admin_view_institution.html', {'institutes': institutes})

def approve_institute(request, institute_id):
    institute = get_object_or_404(Institute, id=institute_id)
    institute.status = "approved"
    institute.is_verified = True
    institute.save()
    return redirect('institute_list')

def reject_institute(request, institute_id):
    institute = get_object_or_404(Institute, id=institute_id)
    institute.status = "rejected"
    institute.is_verified = False
    institute.save()
    return redirect('institute_list')