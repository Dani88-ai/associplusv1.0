from .models import Adherent
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import AdherentForm
from .models import Adherent
import datetime
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def adherent_view(request):
    # Récupérer les paramètres de recherche depuis l'URL
    code = request.GET.get('code', '')
    name = request.GET.get('name', '')
    address = request.GET.get('address', '')

    # Filtrer les adhérents en fonction des paramètres de recherche
    adherents = Adherent.objects.all()
    if code:
        adherents = adherents.filter(CodeAdh__icontains=code)
    if name:
        adherents = adherents.filter(NomAdh__icontains=name) | adherents.filter(PrenomAdh__icontains=name)
    if address:
        adherents = adherents.filter(AdresseAdh__icontains=address)
    
    return render(request, 'administrateurs/adherents/list_adherents.html', {'adherents': adherents})
""" def adherent_view(request):
    adherents = Adherent.objects.all()
    return render(request, 'administrateurs/adherents/list_adherents.html', {'adherents': adherents}) """


def generate_code_adh():
    # Obtenez l'année en cours
    current_year = datetime.datetime.now().year

    # Format de l'année
    year_str = str(current_year)

    # Obtenez le dernier code utilisé pour l'année en cours
    last_adherent = Adherent.objects.filter(CodeAdh__startswith=f'ADH{year_str}').order_by('-CodeAdh').first()
    
    if last_adherent:
        # Extraire le dernier numéro à trois chiffres et incrémenter
        last_number = int(last_adherent.CodeAdh[-3:])
        new_number = last_number + 1
    else:
        # Si aucun adhérent n'existe encore pour cette année, commencez par 001
        new_number = 1

    # Formatez le numéro avec trois chiffres
    new_number_str = f'{new_number:03}'

    return f'ADH{year_str}{new_number_str}'


@login_required
def adherent_add(request):
    if request.method == 'POST':
        # Obtenez la valeur générée pour CodeAdh
        code_adh = generate_code_adh()
        form = AdherentForm(request.POST, request.FILES, code_adh=code_adh)
        if form.is_valid():
            form.save()
            messages.success(request, 'Adhérent ajouté avec succès.')
            return redirect('adherent_view')  # Assurez-vous que cette URL est définie dans vos URLs
    else:
        # Obtenez la valeur générée pour CodeAdh
        code_adh = generate_code_adh()
        form = AdherentForm(code_adh=code_adh)
    return render(request, 'administrateurs/adherents/add_adherents.html', {'form': form})



# Vue pour modifier un adhérent existant
@login_required
def adherent_edit(request, adherent_id):
    # Récupérer l'adhérent en fonction de l'ID ou renvoyer une erreur 404 si non trouvé
    adherent = get_object_or_404(Adherent, id=adherent_id)
    
    if request.method == 'POST':
        # Préremplir le formulaire avec les données POST et les fichiers (si présents)
        form = AdherentForm(request.POST, request.FILES, instance=adherent)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Adhérent modifié avec succès.')
            return redirect('adherent_view')  # Rediriger vers la liste des adhérents après la modification
    else:
        # Préremplir le formulaire avec les données de l'adhérent existant
        form = AdherentForm(instance=adherent)
    
    return render(request, 'administrateurs/adherents/edit_adherents.html', {'form': form})


# Vue pour supprimer un adhérent existant
@login_required
def adherent_delete(request, adherent_id):
    # Récupérer l'adhérent en fonction de l'ID ou renvoyer une erreur 404 si non trouvé
    adherent = get_object_or_404(Adherent, id=adherent_id)
    
    if request.method == 'POST':
        # Supprimer l'adhérent
        adherent.delete()
        messages.success(request, 'Adhérent supprimé avec succès.')
        return redirect('adherent_view')  # Rediriger vers la liste des adhérents après la suppression
    
    return render(request, 'administrateurs/adherents/delete_adherents.html', {'adherent': adherent})