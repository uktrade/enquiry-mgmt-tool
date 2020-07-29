def add_cache_control_header_middleware(get_response):
    def middleware(request):

        response = get_response(request)
        response["Cache-Control"] = "max-age=0, no-cache, no-store, must-revalidate, private"
        return response

    return middleware
