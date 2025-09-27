from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView,
    ListView
)
from .models import Dog, Contact, Charter, DogHealthStatus
from .forms import DogForm, ContactForm, CharterForm
# Create your views here.
# =============================================================================
# CHARTER VIEWS
# =============================================================================

class CharterDetailView(LoginRequiredMixin, DetailView):
    """Charter detail with dogs and contacts"""
    model = Charter
    template_name = 'records/charter_detail.html'
    context_object_name = 'charter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        charter = self.object

        # Get related objects
        dogs = charter.housed_dogs.select_related('owner').all()

        # Charter statistics
        context.update({
            'dogs': dogs,
            'charter_stats': {
                'total_dogs': dogs.count(),
                'owned_dogs': dogs.filter(owner__isnull=False).count(),
                'unowned_dogs': dogs.filter(owner__isnull=True).count(),
                'healthy_dogs': dogs.filter(health_status=DogHealthStatus.HEALTHY).count(),
                'sick_dogs': dogs.filter(health_status=DogHealthStatus.SICK).count(),
                'passed_away_dogs': dogs.filter(health_status=DogHealthStatus.PASSED_AWAY).count(),
                'unspecified_health_dogs': dogs.filter(health_status=DogHealthStatus.UNSPECIFIED).count(),
            }
        })
        return context


class CharterCreateView(LoginRequiredMixin, CreateView):
    model = Charter
    form_class = CharterForm
    template_name = 'records/charter_form.html'

    def get_success_url(self):
        return reverse_lazy('records:charter_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        charter_name = form.cleaned_data['name']
        messages.success(self.request, f'Charter "{charter_name}" created successfully!')
        return super().form_valid(form)


class CharterUpdateView(LoginRequiredMixin, UpdateView):
    model = Charter
    form_class = CharterForm
    template_name = 'records/charter_form.html'

    def get_success_url(self):
        return reverse_lazy('records:charter_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Charter "{form.instance.entity_info.name}" updated!')
        return super().form_valid(form)


class CharterDeleteView(LoginRequiredMixin, DeleteView):
    model = Charter
    template_name = 'records/confirm_delete.html'
    success_url = reverse_lazy('main:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_type': 'Charter',
            'cancel_url': 'records:charter_detail',
        })
        return context

    def delete(self, request, *args, **kwargs):
        charter = self.get_object()
        
        # Check if charter has associated dogs or adoptees
        dogs_count = charter.dogs.count()
        adoptees_count = charter.adoptee_set.count()
        
        if dogs_count > 0 or adoptees_count > 0:
            error_msg = f"Charter cannot be deleted because there are {dogs_count} dog{'s' if dogs_count != 1 else ''} and {adoptees_count} adoptee{'s' if adoptees_count != 1 else ''} associated with it."
            messages.error(request, error_msg)
            return redirect('records:charter_detail', pk=charter.pk)
        
        messages.success(request, f'Charter "{charter.entity_info.name}" has been deleted.')
        return super().delete(request, *args, **kwargs)

# =============================================================================
# CONTACT VIEWS
# =============================================================================

class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'records/contact_detail.html'
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add adopted dogs by this contact
        context['adopted_dogs'] = self.object.adopted_dogs.all()
        return context


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'records/contact_form.html'

    def get_success_url(self):
        return reverse_lazy('records:contact_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Contact "{form.instance.entity_info.name}" has been added!')
        return super().form_valid(form)

    def get_initial(self):
        """Pre-populate charter if coming from charter page"""
        initial = super().get_initial()
        charter_id = self.request.GET.get('charter')
        if charter_id:
            initial['charter'] = charter_id
        return initial


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'records/contact_form.html'

    def get_success_url(self):
        return reverse_lazy('records:contact_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Contact "{form.instance.entity_info.name}" has been updated!')
        return super().form_valid(form)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'records/confirm_delete.html'

    def get_success_url(self):
        # Contact doesn't have charter field anymore, return to dashboard
        return reverse_lazy('main:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_type': 'Contact',
            'cancel_url': 'records:contact_detail',
        })
        return context

    def delete(self, request, *args, **kwargs):
        contact = self.get_object()
        
        # Check if contact has associated dogs
        dogs_count = contact.adopted_dogs.count()
        
        if dogs_count > 0:
            error_msg = f"Contact cannot be deleted because there are {dogs_count} dog{'s' if dogs_count != 1 else ''} associated with it."
            messages.error(request, error_msg)
            return redirect('records:contact_detail', pk=contact.pk)
        
        messages.success(request, f'Contact "{contact.entity_info.name}" has been deleted.')
        return super().delete(request, *args, **kwargs)
# =============================================================================
# DOG VIEWS
# =============================================================================

class DogListView(LoginRequiredMixin, ListView):
    """List all dogs - useful for search/filtering later"""
    model = Dog
    template_name = 'records/dog_list.html'
    context_object_name = 'dogs'
    paginate_by = 20  # Pagination for large lists

    def get_queryset(self):
        queryset = Dog.objects.select_related('charter', 'owner').all()
        charter_id = self.request.GET.get('charter')
        if charter_id:
            queryset = queryset.filter(charter_id=charter_id)
        
        # Filter by adoption status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(adoption_status=status)
        
        return queryset.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        charter_id = self.request.GET.get('charter')
        if charter_id:
            try:
                charter = Charter.objects.get(id=charter_id)
                context['charter'] = charter
                context['page_title'] = f'Dogs in {charter.name}'
            except Charter.DoesNotExist:
                pass
        else:
            context['page_title'] = 'All Dogs'
        return context


class DogDetailView(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = 'records/dog_detail.html'
    context_object_name = 'dog'

    def get_queryset(self):
        # Optimize query with related objects
        return Dog.objects.select_related('charter', 'owner')


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'records/dog_form.html'

    def get_success_url(self):
        return reverse_lazy('records:dog_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Dog "{form.instance.name}" has been added successfully!')
        return super().form_valid(form)

    def get_initial(self):
        """Pre-populate form with charter if coming from charter page"""
        initial = super().get_initial()
        charter_id = self.request.GET.get('charter')
        if charter_id:
            initial['charter'] = charter_id
        return initial


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'records/dog_form.html'

    def get_success_url(self):
        return reverse_lazy('records:dog_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Dog "{form.instance.name}" has been updated!')
        return super().form_valid(form)


class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    template_name = 'records/confirm_delete.html'

    def get_success_url(self):
        # Return to charter page if dog belongs to a charter
        if self.object.charter:
            return reverse_lazy('records:charter_detail',
                                kwargs={'pk': self.object.charter.pk})
        return reverse_lazy('main:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_type': 'Dog',
            'cancel_url': 'records:dog_detail',
        })
        return context

    def delete(self, request, *args, **kwargs):
        dog = self.get_object()
        messages.success(request, f'Dog "{dog.name}" has been deleted.')
        return super().delete(request, *args, **kwargs)


# =============================================================================
# CONTACT VIEWS
# =============================================================================

class ContactListView(LoginRequiredMixin, ListView):
    """List all contacts - useful for search/filtering later"""
    model = Contact
    template_name = 'records/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 20  # Pagination for large lists

    def get_queryset(self):
        queryset = Contact.objects.select_related('entity_info').all()
        # Note: Contact doesn't have charter field anymore
        return queryset.order_by('-entity_info__created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'All Contacts'
        return context




