from django.shortcuts import render
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    all_destinations = models.Destination.objects.all()  # pylint: disable=no-member
    return render(request, 'destinations.html', { 'destinations': all_destinations})

class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'
    
class DestinationCreateView(generic.CreateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description']
    
class DestinationUpdateView(generic.UpdateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description']
    
class DestinationDeleteView(generic.DeleteView):
    model = models.Destination
    template_name = 'destination_confirm_delete.html'
    success_url = reverse_lazy('destinations')

class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'

class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        cruise = form.cleaned_data['cruise']
        notes = form.cleaned_data['notes']
        
        subject = f'New Info Request for {cruise.name}'
        message = f'''Hello {name},

Thank you for your interest in {cruise.name}!

Your request details:
- Cruise: {cruise.name}
- Email: {email}
- Notes: {notes}

We will contact you soon with more information.

Best regards,
ReleCloud Team
'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return response