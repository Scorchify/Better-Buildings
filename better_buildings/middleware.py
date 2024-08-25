from django.shortcuts import redirect
from django.urls import resolve
from better_buildings.models import School

class getIPAddressMw:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_urls = ['no_permission']
        current_url_name = resolve(request.path_info).url_name

        if current_url_name not in excluded_urls:
            request.client_ip = self.get_client_ip_address(request)
            request.student_school = self.get_student_school(request.client_ip)

            # Check if the user is authenticated and is a supervisor
            if request.user.is_authenticated and request.user.is_supervisor():
                if not request.student_school:
                    # Set the school based on the supervisor's preset school
                    request.student_school = request.user.school

                # Ensure the user has an associated school in their profile
                if request.user.school is None or request.user.school != request.student_school:
                    return redirect('better_buildings:no_permission')

        response = self.get_response(request)
        return response

    def get_client_ip_address(self, request):
        req_headers = request.META
        x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for_value:
            ip_addr = x_forwarded_for_value.split(',')[-1].strip()
        else:
            ip_addr = req_headers.get('REMOTE_ADDR')
        return ip_addr

    def get_student_school(self, ip_addr):
        try:
            school = School.objects.get(ip_address=ip_addr)
            return school
        except School.DoesNotExist:
            return None
