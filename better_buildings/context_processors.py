#context processor DO NOT TOUCH 
def add_student_school(request):
    return {
        'student_school': getattr(request, 'student_school', 'Unknown School')
    }