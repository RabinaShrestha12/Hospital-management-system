from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Doctors, Appointment


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




def appointment_list(request):
    try:
        appointments = Appointment.objects.all().order_by('-created_at')
    except Exception as e:
        messages.error(request, f"Error fetching appointments: {e}")
        appointments = []
    return render(request, 'appointment/appointment_list.html', {'appointments': appointments})


@login_required
def create_appointment(request):
    errors = {}
    doctors = Doctors.objects.all()

    if request.method == 'POST':
        fullname = request.POST.get('fullname', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        category = request.POST.get('category', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()
        description = request.POST.get('description', '').strip()
        doctor_id = request.POST.get('doctor_id', '').strip()

        # ✅ Validation
        if not fullname:
            errors['fullname'] = "Fullname is required"
        if not phone_number:
            errors['phone_number'] = "Phone number is required"
        if not category:
            errors['category'] = "Category is required"
        if not date:
            errors['date'] = "Date is required"
        if not time:
            errors['time'] = "Time is required"
        if not description:
            errors['description'] = "Description is required"
        if not doctor_id:
            errors['doctor_id'] = "Doctor is required"

        if errors:
            return render(request, 'appointment/create_appointment.html', {
                'errors': errors,
                'data': request.POST,
                'doctors': doctors
            })

        try:
            doctor = get_object_or_404(Doctors, id=doctor_id)
            Appointment.objects.create(
                fullname=fullname,
                phone_number=phone_number,
                category=category,
                date=date,
                time=time,
                description=description,
                doctors=doctor
            )
            messages.success(request, "Appointment booked successfully")
            return redirect('appointment_list')
        except Exception as e:
            messages.error(request, f"Error while creating appointment: {e}")

    return render(request, 'appointment/create_appointment.html', {'doctors': doctors})


@login_required
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    doctors = Doctors.objects.all()

    if request.method == 'POST':
        try:
            appointment.fullname = request.POST.get('fullname', appointment.fullname).strip()
            appointment.phone_number = request.POST.get('phone_number', appointment.phone_number).strip()
            appointment.category = request.POST.get('category', appointment.category).strip()
            appointment.date = request.POST.get('date', appointment.date)
            appointment.time = request.POST.get('time', appointment.time)
            appointment.description = request.POST.get('description', appointment.description).strip()
            doctor_id = request.POST.get('doctor_id')

            if doctor_id:
                appointment.doctors = get_object_or_404(Doctors, id=doctor_id)

            appointment.save()
            messages.success(request, "Appointment updated successfully")
            return redirect('appointment_list')
        except Exception as e:
            messages.error(request, f"Error updating appointment: {e}")

    return render(request, 'appointment/edit_appointment.html', {'appointment': appointment, 'doctors': doctors})


@login_required
def delete_appointment(request, id):
    try:
        appointment = get_object_or_404(Appointment, id=id)
        appointment.delete()
        messages.success(request, "Appointment deleted successfully")
    except Exception as e:
        messages.error(request, f"Error deleting appointment: {e}")
    return redirect('appointment_list')
