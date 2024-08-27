from django.shortcuts import redirect
from django.urls import resolve
from better_buildings.models import School
from geopy.distance import geodesic

class getGeolocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_urls = ['no_permission']
        current_url_name = resolve(request.path_info).url_name

        if current_url_name not in excluded_urls:
            student_school = self.get_student_school(request)

            if student_school is None:
                return redirect('no_permission')

            # Check if the user is authenticated
            if request.user.is_authenticated:
                if request.user.is_supervisor():
                    # Set the school based on the supervisor's preset school
                    request.student_school = request.user.school
                else:
                    # If the user is not a supervisor, set the school by geolocation
                    request.student_school = student_school
                    # Automatically set the user's school if it's not set or doesn't match
                    if request.user.school is None or request.user.school != student_school:
                        request.user.school = student_school
                        request.user.save()

        response = self.get_response(request)
        return response

    def get_student_school(self, request):
        # Check if latitude and longitude are provided
        user_latitude = request.GET.get('latitude')
        user_longitude = request.GET.get('longitude')

        if user_latitude and user_longitude:
            try:
                user_location = (float(user_latitude), float(user_longitude))
            except ValueError:
                return None  # Handle invalid coordinates

            # Fetch schools and calculate distance
            schools = School.objects.all()
            for school in schools:
                school_location = (school.latitude, school.longitude)
                distance = geodesic(user_location, school_location).miles
                if distance <= 1.5:
                    return school
        return None