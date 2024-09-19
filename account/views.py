from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.views.decorators.csrf import csrf_protect
from .models import User 
from adherent.models import Adherent
from cotisation.models import Cotisation
from django.utils import timezone
from django.db.models import Sum, F, FloatField
from django.contrib.auth.decorators import login_required
from decimal import Decimal





def home_view(request):
    return render(request, 'home.html')



@csrf_protect
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser or user.is_staff:
                    login(request, user)
                    return redirect('dashboard_admin')
                elif user.is_tresorier:
                    login(request, user)
                    return redirect('dashboard_treso')
                elif user.is_president:
                    login(request, user)
                    return redirect('dashboard_presi')
                elif user.is_secretaire:
                    login(request, user)
                    return redirect('dashboard_secret')
                else:
                    msg = 'Vous n\'avez pas les permissions nécessaires.'
            else:
                msg = 'Nom d\'utilisateur ou mot de passe incorrect.'
        else:
            msg = 'Formulaire invalide. Veuillez vérifier les informations fournies.'
    return render(request, 'login.html', {'form': form, 'msg': msg})

@login_required
@csrf_protect
def register_view(request):
    msg = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
           user = form.save()
           msg = 'Utilisateur créé avec succès !'
           return redirect('listuser_view')
        else:
            msg = 'Erreur de création de l\'utilisateur'
    else:
        form = RegisterForm()
    return render(request, 'administrateurs/create_user.html', {'form': form, 'msg': msg})

def dashboard_admin(request):
    active_count = Adherent.objects.filter(StatutAdh='Actif').count()
    inactive_count = Adherent.objects.filter(StatutAdh='Inactif').count()
    suspended_count = Adherent.objects.filter(StatutAdh='Suspendu').count()
    female_count = Adherent.objects.filter(SexeAdh='F').count()
    total_count = Adherent.objects.count()

     # Récupérer l'année en cours
    current_year = timezone.now().year

    # Calculer la somme des cotisations des adhérents actifs pour l'année en cours
    total_cotisations_actifs = Cotisation.objects.filter(Adherent__StatutAdh='Actif').aggregate(total=Sum('MontantCotise'))['total'] or 0

    # Calculer la somme des cotisations des adhérents inactifs pour l'année en cours
    total_cotisations_inactifs = Cotisation.objects.filter(Adherent__StatutAdh='Inactif', AnneeConcernee=current_year).aggregate(total=Sum('MontantCotise'))['total'] or 0

     # Agréger les cotisations par mois et calculer la somme pour chaque mois
    cotisations_par_mois = Cotisation.objects.values('MoisCotisation').annotate(
        total_montant=Sum('MontantCotise')
    ).order_by('MoisCotisation')

     # Récupérer toutes les cotisations et grouper par mois et année
    cotisations_by_month = Cotisation.objects.values('MoisCotisation', 'AnneeConcernee') \
        .annotate(total_montant=Sum('MontantCotise')) \
        .order_by('-AnneeConcernee', '-MoisCotisation')[:5]

    # Calculer le montant total cotisé pour l'année en cours ou une autre période souhaitée
    montant_total = cotisations_by_month.aggregate(total=Sum('total_montant', output_field=FloatField()))['total'] or 0

    # Ajouter un champ pour calculer le pourcentage de chaque mois
    for cotisation in cotisations_by_month:
        montant_total = Decimal(montant_total)
        cotisation['pourcentage'] = (cotisation['total_montant'] / montant_total) * 100 if montant_total > 0 else 0

    context = {
        'current_year': current_year,
        'active_count': active_count,
        'inactive_count': inactive_count,
        'suspended_count': suspended_count,
        'female_count': female_count,
        'total_count': total_count,
        'total_cotisations_actifs': total_cotisations_actifs,
        'total_cotisations_inactifs': total_cotisations_inactifs,
        'cotisations_stats': cotisations_by_month,
        'montant_total': montant_total,
        'cotisations_par_mois': cotisations_par_mois
    }
    return render(request, 'administrateurs/dashboard_admin.html', context)








@login_required
def listuser_view(request):
    users = User.objects.all()  # Récupère tous les utilisateurs
    return render(request, 'administrateurs/list_user.html', {'users': users})

@login_required
def dashboard_presi(request):
    return render(request, 'presidents/dashboard_presi.html')


@login_required
def dashboard_treso(request):
    return render(request, 'tresoriers/dashboard_treso.html')

@login_required
def dashboard_secret(request):
    return render(request, 'secretaires/dashboard_secret.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')  # Redirige l'utilisateur vers la page de connexion après déconnexion


@login_required
def cotisation_stats(request):
    # Récupérer toutes les cotisations et grouper par mois et année
    cotisations_by_month = Cotisation.objects.values('MoisCotisation', 'AnneeConcernee') \
        .annotate(total_montant=Sum('MontantCotise')) \
        .order_by('AnneeConcernee', 'MoisCotisation')

    # Calculer le montant total cotisé pour l'année en cours ou une autre période souhaitée
    montant_total = cotisations_by_month.aggregate(total=Sum('total_montant', output_field=FloatField()))['total'] or 0

    # Ajouter un champ pour calculer le pourcentage de chaque mois
    for cotisation in cotisations_by_month:
        cotisation['pourcentage'] = (cotisation['total_montant'] / montant_total) * 100 if montant_total > 0 else 0

    return render(request, 'administrateurs/cotisations/list_cotisations.html', {
        'cotisations_stats': cotisations_by_month,
        'montant_total': montant_total,
    })


