# gipl_app/middleware.py

class SubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the host (e.g., 'stationary.gitanshuimpex.com' or 'localhost:8000')
        host = request.get_host().lower()
        
        # Strip the port number if you are testing locally
        if ':' in host:
            host = host.split(':')[0]

        # Define your primary production domain
        base_domain = 'gitanshuimpex.com'
        
        # Default assumption: The user is NOT on a subdomain
        request.subdomain = None
        
        # Check if the URL ends with your domain, but isn't JUST the base domain or www
        if host.endswith(base_domain) and host != base_domain and host != f"www.{base_domain}":
            # Strip off the base domain to isolate the subdomain string
            subdomain = host.replace(f".{base_domain}", "")
            
            # Double check it's not just 'www'
            if subdomain != 'www':
                request.subdomain = subdomain

        # Pass the request (now carrying the subdomain info) to your views
        response = self.get_response(request)
        return response