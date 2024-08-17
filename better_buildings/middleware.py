from django.shortcuts import redirect
from django.urls import resolve

class getIPAddressMw:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URL names to exclude from IP check
        excluded_urls = ['no_permission']

        current_url_name = resolve(request.path_info).url_name
        # Prevents infinite redirect
        if current_url_name not in excluded_urls:
            request.client_ip = self.get_client_ip_address(request)
            if not self.is_allowed_ip(request.client_ip):
                return redirect('no_permission')

            # Set the student_school based on IP address
            request.student_school = self.get_student_school(request.client_ip)

        response = self.get_response(request)
        return response

    # Grabs IP address
    def get_client_ip_address(self, request):
        req_headers = request.META
        x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for_value:
            ip_addr = x_forwarded_for_value.split(',')[-1].strip()
        else:
            ip_addr = req_headers.get('REMOTE_ADDR')
        return ip_addr

    # Checks if IP address is allowed
    def is_allowed_ip(self, ip_addr):
        allowed_ips = ['127.0.0.1', '::1']  # allowed IPS TODO find MCPS ips 
        return ip_addr in allowed_ips

    # Maps IP address to student_school
    def get_student_school(self, ip_addr):
        ip_school_map = {
            '127.0.0.1': 'Wheaton High',  # Example mapping
            '::1': 'Wheaton High',
            #TODO Upload to server and put other school ips here to do testing 
        }
        return ip_school_map.get(ip_addr, 'Unknown School')
