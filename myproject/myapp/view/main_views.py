from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Doctors


def abouthosp(request):
    return render(request, 'abouthosp.html')

def department(request):
    return render(request, 'department.html')

def index(request):
    doctors = Doctors.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'doctors': doctors})

@login_required
def createdoctors(request):
    errors = {}
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        category = request.POST.get('category')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not fullname:
            errors['fullname'] = "Fullname is required"
        if not category:
            errors['category'] = "Category is required"
        if not description:
            errors['description'] = "Description is required"
        if not image:
            errors['image'] = "Image is required"

        if errors:
            return render(request, 'doctors/createdoctors.html', {'errors': errors, 'data': request.POST})

        Doctors.objects.create(
            fullname=fullname,
            category=category,
            description=description,
            image=image
        )
        messages.success(request, "Doctor added successfully")
        return redirect('index')

    return render(request, 'doctors/createdoctors.html')


def singledoctors(request, id):
    doctor = get_object_or_404(Doctors, id=id)
    return render(request, 'doctors/singledoctors.html', {"doctor": doctor})


@login_required
def editdoctors(request, id):
    doctor = get_object_or_404(Doctors, id=id)

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        category = request.POST.get('category')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        doctor.fullname = fullname
        doctor.category = category
        doctor.description = description
        if image:
            doctor.image = image
        doctor.save()

        messages.success(request, "Doctor updated successfully")
        return redirect('singledoctor', id=doctor.id)

    return render(request, 'doctors/editdoctors.html', {"doctor": doctor})


@login_required
def deletedoctors(request, id):
    doctor = get_object_or_404(Doctors, id=id)
    doctor.delete()
    messages.success(request, "Doctor deleted successfully")
    return redirect('index')
