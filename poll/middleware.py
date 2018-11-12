import hashlib


class AnonymousUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated():
            x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
            remote_addr = request.META.get('REMOTE_ADDR', None)
            if x_forward_for:
                ip_address = x_forward_for.split(', ')[0]
            else:
                ip_address = remote_addr

            hashed_ip = hashlib.md5(ip_address.encode('utf-8'))
            request.POST = request.POST.copy()
            request.POST['hashed_ip'] = hashed_ip.hexdigest()

        response = self.get_response(request)
        return response
