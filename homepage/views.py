from django.shortcuts import render, get_object_or_404
from .models import Service, Intervention, Doctor_TMP


# Generate the homepage
def home(request):
    services = Service.objects.all()
    context = {'services': services}

    return render(request, 'homepage/home.html', context)


# Generate service pages
def service(request, Service_slug=None):
    services = None
    interventions = None
    doctors = None

    if Service_slug != None:
        services = get_object_or_404(Service, slug=Service_slug)
        print('services', services)
        interventions = Intervention.objects.filter(service=services)
        print('interventions', interventions)
        doctors = Doctor_TMP.objects.filter(service=services)
        print('doctors', doctors)
        context = {
            'services': services,
            'interventions': interventions,
            'doctors': doctors,
            'service_image': services.image,  # Add this line to include the image in the context
        }
    return render(request, 'homepage/service.html', context)