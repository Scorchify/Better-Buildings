class getIPAddressMw:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.client_ip = self.get_client_ip_address(request)
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