from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from records.models import Dog, Charter
from django.db.models import Count, Q
# Create your views here.
# =============================================================================
# DASHBOARD & MAIN VIEWS (Function-based - complex logic)
# =============================================================================

class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard - using TemplateView for custom context"""
    template_name = 'main/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Global statistics
        context.update({
            'total_dogs': Dog.objects.count(),
            'adopted_dogs': Dog.objects.filter(adoption_status='ADOPTED').count(),
            'available_dogs': Dog.objects.filter(eligible_for_adoption=True, adoption_status='I').count(),
            'healthy_dogs': Dog.objects.filter(health_status='HEALTHY').count(),
            'charters': Charter.objects.annotate(
                dog_count=Count('dogs'),
                adopted_count=Count('dogs', filter=Q(dogs__adoption_status='ADOPTED'))
            ).all(),
        })
        return context