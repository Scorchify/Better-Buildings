from .models import Area, Report, Announcement

def areas(request):
    student_school = getattr(request, 'student_school', None)
    if student_school:
        return {
            'areas': Area.objects.filter(school=student_school)
        }
    return {
        'areas': Area.objects.none()
    }

def supervisor_status(request):
    return {
        'supervisor': request.user.is_authenticated and request.user.is_superuser
    }

def add_student_school(request):
    return {
        'student_school': getattr(request, 'student_school', 'Unknown School')
    }

def reports(request):
    student_school = getattr(request, 'student_school', None)
    if student_school:
        return {
            'reports': Report.objects.filter(school=student_school)
        }
    return {
        'reports': Report.objects.none()
    }

def announcements(request):
    student_school = getattr(request, 'student_school', None)
    if student_school:
        return {
            'announcements': Announcement.objects.filter(school=student_school)
        }
    return {
        'announcements': Announcement.objects.none()
    }