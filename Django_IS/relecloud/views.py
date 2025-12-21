from django.shortcuts import render
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseForbidden

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
    fields = ['name', 'description', 'image']
    
class DestinationUpdateView(generic.UpdateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description', 'image']
    
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


class DestinationReviewCreateView(LoginRequiredMixin, generic.CreateView):
    """Vista para crear reviews de destinos"""
    model = models.DestinationReview
    template_name = 'destination_review_form.html'
    fields = ['rating', 'comment']
    
    def dispatch(self, request, *args, **kwargs):
        """Verificar que el usuario haya comprado algún crucero"""
        # Los usuarios deben haber comprado al menos un crucero
        if not models.Purchase.objects.filter(user=request.user).exists():
            messages.error(request, 'You must have purchased a cruise to write reviews.')
            return HttpResponseForbidden('You must have purchased a cruise to write reviews.')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Asignar el usuario y destino al review"""
        destination = models.Destination.objects.get(pk=self.kwargs['pk'])
        
        # Verificar si el usuario ya dejó un review
        existing_review = models.DestinationReview.objects.filter(
            destination=destination,
            user=self.request.user
        ).first()
        
        if existing_review:
            # Actualizar el review existente
            existing_review.rating = form.cleaned_data['rating']
            existing_review.comment = form.cleaned_data['comment']
            existing_review.save()
            messages.success(self.request, 'Your review has been updated!')
            return super().form_valid(form)
        
        form.instance.destination = destination
        form.instance.user = self.request.user
        messages.success(self.request, 'Thank you for your review!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirigir al destino después de crear el review"""
        return reverse_lazy('destination_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        """Agregar el destino al contexto"""
        context = super().get_context_data(**kwargs)
        context['destination'] = models.Destination.objects.get(pk=self.kwargs['pk'])
        return context


class CruiseReviewCreateView(LoginRequiredMixin, generic.CreateView):
    """Vista para crear reviews de cruceros"""
    model = models.CruiseReview
    template_name = 'cruise_review_form.html'
    fields = ['rating', 'comment']
    
    def dispatch(self, request, *args, **kwargs):
        """Verificar que el usuario haya comprado algún crucero"""
        cruise = models.Cruise.objects.get(pk=self.kwargs['pk'])
        if not models.Purchase.objects.filter(user=request.user, cruise=cruise).exists():
            messages.error(request, 'You must have purchased this cruise to write a review.')
            return HttpResponseForbidden('You must have purchased this cruise to write a review.')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Asignar el usuario y crucero al review"""
        cruise = models.Cruise.objects.get(pk=self.kwargs['pk'])
        
        # Verificar si el usuario ya dejó un review
        existing_review = models.CruiseReview.objects.filter(
            cruise=cruise,
            user=self.request.user
        ).first()
        
        if existing_review:
            # Actualizar el review existente
            existing_review.rating = form.cleaned_data['rating']
            existing_review.comment = form.cleaned_data['comment']
            existing_review.save()
            messages.success(self.request, 'Your review has been updated!')
            return super().form_valid(form)
        
        form.instance.cruise = cruise
        form.instance.user = self.request.user
        messages.success(self.request, 'Thank you for your review!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirigir al crucero después de crear el review"""
        return reverse_lazy('cruise_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        """Agregar el crucero al contexto"""
        context = super().get_context_data(**kwargs)
        context['cruise'] = models.Cruise.objects.get(pk=self.kwargs['pk'])
        return context