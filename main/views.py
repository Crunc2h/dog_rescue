from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from records.models import Dog, Charter, AdoptionStatus, DogHealthStatus, DogVaccinationStatus
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
            'adopted_dogs': Dog.objects.filter(adoption_status=AdoptionStatus.ADOPTED).count(),
            'fit_dogs': Dog.objects.filter(adoption_status=AdoptionStatus.FIT).count(),
            'unfit_dogs': Dog.objects.filter(adoption_status=AdoptionStatus.UNFIT).count(),
            'trial_dogs': Dog.objects.filter(adoption_status=AdoptionStatus.TRIAL).count(),
            'unspecified_dogs': Dog.objects.filter(adoption_status=AdoptionStatus.UNSPECIFIED).count(),
            'healthy_dogs': Dog.objects.filter(health_status=DogHealthStatus.HEALTHY).count(),
            'sick_dogs': Dog.objects.filter(health_status=DogHealthStatus.SICK).count(),
            'passed_away_dogs': Dog.objects.filter(health_status=DogHealthStatus.PASSED_AWAY).count(),
            'unspecified_health_dogs': Dog.objects.filter(health_status=DogHealthStatus.UNSPECIFIED).count(),
            'complete_vaccination_dogs': Dog.objects.filter(vaccination_status=DogVaccinationStatus.COMPLETE).count(),
            'incomplete_vaccination_dogs': Dog.objects.filter(vaccination_status=DogVaccinationStatus.INCOMPLETE).count(),
            'not_vaccinated_dogs': Dog.objects.filter(vaccination_status=DogVaccinationStatus.NOT_VACCINATED).count(),
            'unspecified_vaccination_dogs': Dog.objects.filter(vaccination_status=DogVaccinationStatus.UNSPECIFIED).count(),
            'charters': Charter.objects.annotate(
                dog_count=Count('dogs'),
                adopted_count=Count('dogs', filter=Q(dogs__adoption_status=AdoptionStatus.ADOPTED)),
                fit_count=Count('dogs', filter=Q(dogs__adoption_status=AdoptionStatus.FIT)),
                unfit_count=Count('dogs', filter=Q(dogs__adoption_status=AdoptionStatus.UNFIT)),
                trial_count=Count('dogs', filter=Q(dogs__adoption_status=AdoptionStatus.TRIAL)),
                unspecified_count=Count('dogs', filter=Q(dogs__adoption_status=AdoptionStatus.UNSPECIFIED)),
                healthy_count=Count('dogs', filter=Q(dogs__health_status=DogHealthStatus.HEALTHY)),
                sick_count=Count('dogs', filter=Q(dogs__health_status=DogHealthStatus.SICK)),
                passed_away_count=Count('dogs', filter=Q(dogs__health_status=DogHealthStatus.PASSED_AWAY)),
                unspecified_health_count=Count('dogs', filter=Q(dogs__health_status=DogHealthStatus.UNSPECIFIED)),
                complete_vaccination_count=Count('dogs', filter=Q(dogs__vaccination_status=DogVaccinationStatus.COMPLETE)),
                incomplete_vaccination_count=Count('dogs', filter=Q(dogs__vaccination_status=DogVaccinationStatus.INCOMPLETE)),
                not_vaccinated_count=Count('dogs', filter=Q(dogs__vaccination_status=DogVaccinationStatus.NOT_VACCINATED)),
                unspecified_vaccination_count=Count('dogs', filter=Q(dogs__vaccination_status=DogVaccinationStatus.UNSPECIFIED)),
            ).all(),
        })
        return context