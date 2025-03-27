from .forms import InquiryForm

def inquiry_form_context(request):
    return {'form': InquiryForm()}
