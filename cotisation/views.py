from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Cotisation
from adherent.models import Adherent
from .forms import CotisationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q , Sum, F, FloatField





# Create your views here.

@login_required
def cotisation_view(request):
    # Récupérer les paramètres de recherche depuis la requête GET
    search_id = request.GET.get('search_id', '')
    search_name = request.GET.get('search_name', '')
    search_phone = request.GET.get('search_phone', '')

    # Construire la requête de filtrage
    query = Q()
    if search_id:
        query &= Q(Adherent__CodeAdh__icontains=search_id)
    if search_name:
        query &= Q(Adherent__NomAdh__icontains=search_name) | Q(Adherent__PrenomAdh__icontains=search_name)
    if search_phone:
        query &= Q(MoisCotisation__icontains=search_phone) |Q (AnneeConcernee__icontains=search_phone)

    # Filtrer les cotisations selon la requête
    cotisations = Cotisation.objects.filter(query).select_related('Adherent').all()

    return render(request, 'administrateurs/cotisations/list_cotisations.html', {'cotisations': cotisations})

""" def cotisation_view(request):
	cotisations = Cotisation.objects.select_related('Adherent').all()
	return render(request, 'administrateurs/cotisations/list_cotisations.html', {'cotisations': cotisations}) """




@login_required
def cotisation_add(request):
    adherents = Adherent.objects.filter(StatutAdh__in=['Actif', 'Inactif'] )  # Filtrer les adhérents actifs et inactif
    if request.method == 'POST':
        form = CotisationForm(request.POST)
        if form.is_valid():
            cotisation = form.save(commit=False)
            cotisation.save()  # Cela va déclencher la méthode save et mettre à jour le montant restant
            messages.success(request, 'Cotisation ajoutée avec succès!')
            return redirect('cotisation_view')
    else:
        form = CotisationForm()
        form.fields['Adherent'].queryset = adherents

    return render(request, 'administrateurs/cotisations/add_cotisations.html', {'form': form})



# Vue pour modifier une cotisation
@login_required
def cotisation_edit(request, cotisation_id):
    cotisation = get_object_or_404(Cotisation, id=cotisation_id)
    adherents = Adherent.objects.filter(StatutAdh__in=['Actif'])  # Filtrer les adhérents actifs

    if request.method == 'POST':
        form = CotisationForm(request.POST, instance=cotisation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cotisation modifiée avec succès!')
            return redirect('cotisation_view')
    else:
        form = CotisationForm(instance=cotisation)
        form.fields['Adherent'].queryset = adherents  # Restreindre les choix des adhérents actifs

    return render(request, 'administrateurs/cotisations/edit_cotisations.html', {'form': form})



# Vue pour supprimer un adhérent existant
@login_required
def cotisation_delete(request, cotisation_id):
    # Récupérer le cotisation en fonction de l'ID ou renvoyer une erreur 404 si non trouvé
    cotisation = get_object_or_404(Cotisation, id=cotisation_id)  # Utilisez 'cotisation' au singulier
    
    if request.method == 'POST':
        # Supprimer la cotisation
        cotisation.delete()  # Ici, on supprime 'cotisation' (au singulier)
        messages.success(request, 'Cotisation supprimée avec succès.')
        return redirect('cotisation_view')  # Rediriger vers la liste des cotisations après la suppression
    
    return render(request, 'administrateurs/cotisations/delete_cotisations.html', {'cotisation': cotisation})


""" 
@login_required
def cotisation_details(request, cotisation_id):
    cotisation = get_object_or_404(Cotisation, id=cotisation_id)
    # Récupérer l'adhérent associé
    adherent = cotisation.Adherent
    mois_cotisation = cotisation.MoisCotisation
    return render(request, 'administrateurs/cotisations/details_cotisations.html', {'cotisation': cotisation, 'adherent':adherent, 'mois_cotisation':mois_cotisation})
 """


from django.db.models import Sum

@login_required
def cotisation_details(request, cotisation_id):
    cotisation = get_object_or_404(Cotisation, id=cotisation_id)
    adherent = cotisation.Adherent
    cotisations = Cotisation.objects.filter(Adherent=adherent)

    # Calculer la somme totale des montants cotisés
    somme_total_cotise = cotisations.aggregate(total=Sum('MontantCotise'))['total'] or 0

    return render(request, 'administrateurs/cotisations/details_cotisations.html', {
        'cotisation': cotisation,
        'adherent': adherent,
        'cotisations': cotisations,
        'somme_total_cotise': somme_total_cotise
    })



@login_required
def cotisation_stats(request):
    # Récupérer toutes les cotisations
    cotisations = Cotisation.objects.all()

    # Calculer le montant total cotisé
    montant_total = cotisations.aggregate(total=Sum('MontantCotise'))['total'] or 0

    # Calculer le pourcentage de chaque mois
    cotisations_stats = cotisations.annotate(
        pourcentage=(F('MontantCotise') / montant_total) * 100
    )

    return render(request, 'administrateurs/cotisations/stats.html', {
        'cotisations_stats': cotisations_stats,
        'montant_total': montant_total,
        'cotisations': cotisations,
    })

