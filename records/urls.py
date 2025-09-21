from django.urls import path
from . import views

app_name = 'records'
urlpatterns = [
    # Charter URLs
    path('charter/<int:pk>/', views.CharterDetailView.as_view(), name='charter_detail'),
    path('charter/create/', views.CharterCreateView.as_view(), name='charter_create'),
    path('charter/<int:pk>/edit/', views.CharterUpdateView.as_view(), name='charter_edit'),
    path('charter/<int:pk>/delete/', views.CharterDeleteView.as_view(), name='charter_delete'),

    # Dog URLs
    path('dogs/', views.DogListView.as_view(), name='dog_list'),  # Optional: list all dogs
    path('dog/<int:pk>/', views.DogDetailView.as_view(), name='dog_detail'),
    path('dog/create/', views.DogCreateView.as_view(), name='dog_create'),
    path('dog/<int:pk>/edit/', views.DogUpdateView.as_view(), name='dog_edit'),
    path('dog/<int:pk>/delete/', views.DogDeleteView.as_view(), name='dog_delete'),

    # Contact URLs
    path('contacts/', views.ContactListView.as_view(), name='contact_list'),  # Optional: list all contacts
    path('contact/<int:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('contact/create/', views.ContactCreateView.as_view(), name='contact_create'),
    path('contact/<int:pk>/edit/', views.ContactUpdateView.as_view(), name='contact_edit'),
    path('contact/<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
]