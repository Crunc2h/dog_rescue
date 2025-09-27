from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from records.models import Dog, Charter, DogHealthStatus, DogVaccinationStatus, DogIntakeStatus
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
            'rescue_dogs': Dog.objects.filter(intake_status=DogIntakeStatus.RESCUE).count(),
            'training_dogs': Dog.objects.filter(intake_status=DogIntakeStatus.TRAINING).count(),
            'hotel_dogs': Dog.objects.filter(intake_status=DogIntakeStatus.HOTEL).count(),
            'owned_dogs': Dog.objects.filter(owner__isnull=False).count(),
            'unowned_dogs': Dog.objects.filter(owner__isnull=True).count(),
            'healthy_dogs': Dog.objects.filter(health_status=DogHealthStatus.HEALTHY).count(),
            'sick_dogs': Dog.objects.filter(health_status=DogHealthStatus.SICK).count(),
            'passed_away_dogs': Dog.objects.filter(health_status=DogHealthStatus.PASSED_AWAY).count(),
            'unspecified_health_dogs': Dog.objects.filter(health_status=DogHealthStatus.UNSPECIFIED).count(),
            'complete_vaccination_dogs': Dog.objects.filter(vaccination_status=DogVaccinationStatus.COMPLETE).count(),
            'incomplete_vaccination_dogs': Dog.objects.filter(vaccination_status=DogVaccinationStatus.INCOMPLETE).count(),
            'not_vaccinated_dogs': Dog.objects.filter(vaccination_status=DogVaccinationStatus.NOT_VACCINATED).count(),
            'unspecified_vaccination_dogs': Dog.objects.filter(vaccination_status=DogVaccinationStatus.UNSPECIFIED).count(),
            'charters': Charter.objects.annotate(
                dog_count=Count('housed_dogs'),
                rescue_count=Count('housed_dogs', filter=Q(housed_dogs__intake_status=DogIntakeStatus.RESCUE)),
                training_count=Count('housed_dogs', filter=Q(housed_dogs__intake_status=DogIntakeStatus.TRAINING)),
                hotel_count=Count('housed_dogs', filter=Q(housed_dogs__intake_status=DogIntakeStatus.HOTEL)),
                owned_count=Count('housed_dogs', filter=Q(housed_dogs__owner__isnull=False)),
                unowned_count=Count('housed_dogs', filter=Q(housed_dogs__owner__isnull=True)),
                healthy_count=Count('housed_dogs', filter=Q(housed_dogs__health_status=DogHealthStatus.HEALTHY)),
                sick_count=Count('housed_dogs', filter=Q(housed_dogs__health_status=DogHealthStatus.SICK)),
                passed_away_count=Count('housed_dogs', filter=Q(housed_dogs__health_status=DogHealthStatus.PASSED_AWAY)),
                unspecified_health_count=Count('housed_dogs', filter=Q(housed_dogs__health_status=DogHealthStatus.UNSPECIFIED)),
                complete_vaccination_count=Count('housed_dogs', filter=Q(housed_dogs__vaccination_status=DogVaccinationStatus.COMPLETE)),
                incomplete_vaccination_count=Count('housed_dogs', filter=Q(housed_dogs__vaccination_status=DogVaccinationStatus.INCOMPLETE)),
                not_vaccinated_count=Count('housed_dogs', filter=Q(housed_dogs__vaccination_status=DogVaccinationStatus.NOT_VACCINATED)),
                unspecified_vaccination_count=Count('housed_dogs', filter=Q(housed_dogs__vaccination_status=DogVaccinationStatus.UNSPECIFIED)),
            ).all(),
        })
        return context