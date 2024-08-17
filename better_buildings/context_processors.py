#context processor DO NOT TOUCH 
from .models import Area

def areas(request):
    return {
        'areas': Area.objects.all()
    }

def supervisor_status(request):
    return {
        'supervisor': request.user.is_authenticated and request.user.is_superuser
    }

def add_student_school(request):
    return {
        'student_school': getattr(request, 'student_school', 'Unknown School')
    }
