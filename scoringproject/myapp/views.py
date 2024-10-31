from django.shortcuts import render, get_object_or_404, redirect
import re
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from .forms import ArnisPlayersForm, ArnisPlayersLabanan, ArnisReferees, ArnisJudges, ArnisRecorders, ArnisTabulators, ArnisTimers, \
    Colleges, SchoolYears, LabananMatchForm, LabananRoundForm, LabananScoreForm, ArnisManagers, AnyoMatchForm, AnyoPlayersForm, VolleyballReferees, \
    VolleyballPlayers, VolleyballTeams, VolleyballJudges, VolleyballScorers, VolleyballMatchForm, VolleyballMatchPlayersForm, VolleyballScoreForm, VolleyballSetForm, \
    SingleTennisMatchForm, SingleTennisScoreForm, SingleTennisSetForm, DoubleTennisMatchForm, DoublelTennisSetForm, DoubleTennisScoreForm, TennisCoaches, TennisPlayersForm, \
    TennisUmpires, FormPlayers, LoginForm, SchoolYearForm, CustomUserForm
from .models import SchoolYear, ArnisLabananPlayers, ArnisFormPlayers, ArnisReferee, ArnisRecorder, ArnisTabulator, ArnisJudge, \
    ArnisTimer, College, LabananMatch, LabananRound, LabananScore, ArnisManager, VolleyballPlayer, VolleyballJudge, VolleyballReferee, \
    VolleyballScorer, VolleyballTeam, VolleyballSet, TennisCoach, TennisPlayers, TennisUmpire, SingleTennisScore, SingleTennisMatch, SingleTennisSet, DoubleTennisScore, \
    DoubleTennisMatch, DoubleTennisSet, FormMatch, VolleyballMatch, VolleyballScore, CustomUser
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from functools import wraps
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseForbidden





class CustomLogoutView(LogoutView):
    template_name = 'landing.html'  # Optionally, create a custom template for logout

    def dispatch(self, request, *args, **kwargs):
        # Customize the logout behavior if needed
        # For example, you can add a confirmation message
        messages.info(request, "You have been successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Instantiate the LoginForm with request data
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if 'next' in request.GET:
                    next_url = request.GET.get('next')
                    
                    if user.sport == 'arnis' and 'arnis' in next_url:
                        login(request, user)
                        return redirect(next_url)
                    elif user.sport == 'volleyball' and 'volleyball' in next_url:
                        login(request, user)
                        return redirect(next_url)
                    elif user.sport == 'table_tennis' and 'table_tennis' in next_url:
                        login(request, user)
                        return redirect(next_url)
                    elif user.is_admin:  # Check if the user is an admin
                        login(request, user)
                        return redirect(next_url)  # Admins can go to any page
                    else:
                        messages.error(request, "You are not an authorized user to access that page.")
                        return redirect('myapp:sports')  # Redirect to sport selection page
                else:
                    messages.error(request, "Invalid request.")
                    return redirect('myapp:sports')  # Redirect to sport selection page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()  # Instantiate an empty LoginForm for GET requests
    
    # If the request method is GET or form validation fails, render the login page with the form
    return render(request, 'login.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Instantiate the LoginForm with request data
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_admin:  # Check if the user is an admin
                    login(request, user)
                    next_url = request.GET.get('next', 'myapp:admin_dashboard')  # Get the next URL
                    return redirect(next_url)  # Redirect to the admin dashboard
                else:
                    messages.error(request, "You are not authorized to access the admin area.")
                    return redirect('myapp:admin_login')  # Redirect back to the admin login page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()  # Instantiate an empty LoginForm for GET requests
    
    return render(request, 'admin/admin_login.html', {'form': form})


@login_required(login_url='/login')
def add_form_player(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin
    
    selected_year_id = request.GET.get('previous_year')
    players_from_previous_year = []

    # If a previous school year is selected, fetch its players
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        players_from_previous_year = ArnisFormPlayers.objects.filter(yearID=previous_school_year)

    colleges = College.objects.all()  # Fetch all colleges

    if request.method == 'POST':
        # Process selected players from the previous year
        selected_player_ids = request.POST.getlist('selected_players')
        for player_id in selected_player_ids:
            player = get_object_or_404(ArnisFormPlayers, pk=player_id)
            ArnisFormPlayers.objects.create(
                player_name=player.player_name,
                collegeID=player.collegeID,
                yearID=school_year
            )

        # Process new player if entered
        new_player_name = request.POST.get('new_player_name')
        new_college_id = request.POST.get('new_college_id')

        if new_player_name and new_college_id:
            college = get_object_or_404(College, pk=new_college_id)
            ArnisFormPlayers.objects.create(
                player_name=new_player_name,
                collegeID=college,
                yearID=school_year
            )

        messages.success(request, "Players have been successfully added.")
        return redirect('myapp:arnis_sport_data')

    context = {
        'school_year': school_year,
        'all_school_years': all_school_years,
        'players_from_previous_year': players_from_previous_year,
        'colleges': colleges,
        'is_admin': is_admin,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page

    return render(request, 'add-form-player.html', context)
    
@login_required(login_url='/login')
def add_labanan_player(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin  # Check if the user is an admin

    selected_year_id = request.GET.get('previous_year')
    players_from_previous_year = []

    # If a previous school year is selected, fetch its players
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        players_from_previous_year = ArnisLabananPlayers.objects.filter(yearID=previous_school_year)

    colleges = College.objects.all()  # Fetch all colleges

    if request.method == 'POST':
        # Process selected players from the previous year
        selected_player_ids = request.POST.getlist('selected_players')
        for player_id in selected_player_ids:
            player = get_object_or_404(ArnisLabananPlayers, pk=player_id)
            ArnisLabananPlayers.objects.create(
                player_name=player.player_name,
                collegeID=player.collegeID,
                yearID=school_year
            )

        # Process new player if entered
        new_player_name = request.POST.get('new_player_name')
        new_college_id = request.POST.get('new_college_id')

        if new_player_name and new_college_id:
            college = get_object_or_404(College, pk=new_college_id)
            ArnisLabananPlayers.objects.create(
                player_name=new_player_name,
                collegeID=college,
                yearID=school_year
            )

        messages.success(request, "Players have been successfully added.")
        return redirect('myapp:arnis_sport_data')

    context = {
        'school_year': school_year,
        'all_school_years': all_school_years,
        'players_from_previous_year': players_from_previous_year,
        'colleges': colleges,
        'is_admin': is_admin,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }
     
    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    
    return render(request, 'add-arnis-player.html', context)


@login_required(login_url='/login')
def edit_form_player(request, player_id):
    player = get_object_or_404(ArnisFormPlayers, playerID=player_id)
    if request.method == 'POST':
        form = ArnisPlayersForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisPlayersForm(instance=player)

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-arnis-player.html', {'form': form})

@login_required(login_url='/login')
def edit_labanan_player(request, player_id):
    player = get_object_or_404(ArnisLabananPlayers, playerID=player_id)
    if request.method == 'POST':
        form = ArnisPlayersLabanan(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisPlayersLabanan(instance=player)

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-arnis-player.html', {'form': form})

@login_required(login_url='/login')
def add_referee(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')
    referees_from_previous_year = []

    # If a previous school year is selected, fetch its referees
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        referees_from_previous_year = ArnisReferee.objects.filter(yearID=previous_school_year)

    if request.method == 'POST':
        # Process selected referees from the previous year
        selected_referee_ids = request.POST.getlist('selected_referees')
        for referee_id in selected_referee_ids:
            referee = get_object_or_404(ArnisReferee, pk=referee_id)
            ArnisReferee.objects.create(
                referee_name=referee.referee_name,
                yearID=school_year
            )

        # Process new referee if entered
        new_referee_name = request.POST.get('new_referee_name')

        if new_referee_name:
            ArnisReferee.objects.create(
                referee_name=new_referee_name,
                yearID=school_year,
            )

        messages.success(request, "Referees have been successfully added.")
        return redirect('myapp:arnis_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'all_school_years': all_school_years,
        'is_admin' : is_admin,
        'referees_from_previous_year': referees_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    
    return render(request, 'add-referee.html', context)


def add_year(request):
    if request.method == 'POST':
        form = SchoolYearForm(request.POST)  # Create form instance with POST data
        if form.is_valid():  # Check if the form is valid
            year = form.save()  # Save the form data to create a SchoolYear object
            return redirect('myapp:admin_other_data')  # Redirect after successful save
    else:
        form = SchoolYearForm()  # Instantiate an empty form for GET requests

    return render(request, 'add-year.html', {'form': form})  # Render the form in the template

@login_required(login_url='/login')
def edit_referee(request, referee_id):
    referee = get_object_or_404(ArnisReferee, refereeID=referee_id)
    if request.method == 'POST':
        form = ArnisReferees(request.POST, instance=referee)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisReferees(instance=referee)

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-referee.html', {'form': form})\
    
@login_required(login_url='/login')
def add_judge(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year
    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')
    judges_from_previous_year = []

    # If a previous school year is selected, fetch its judges
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        judges_from_previous_year = ArnisJudge.objects.filter(yearID=previous_school_year)


    if request.method == 'POST':
        # Process selected judges from the previous year
        selected_judge_ids = request.POST.getlist('selected_judges')
        for judge_id in selected_judge_ids:
            judge = get_object_or_404(ArnisJudge, pk=judge_id)
            ArnisJudge.objects.create(
                judge_name=judge.judge_name,
                yearID=school_year
            )

        # Process new judge if entered
        new_judge_name = request.POST.get('new_judge_name')

        if new_judge_name:
            ArnisJudge.objects.create(
                judge_name=new_judge_name,
                yearID=school_year,
            )

        messages.success(request, "Judges have been successfully added.")
        return redirect('myapp:arnis_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'all_school_years': all_school_years,
        'is_admin' : is_admin,
        'judges_from_previous_year': judges_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    
    return render(request, 'add-judge.html', context)

@login_required(login_url='/login')
def edit_judge(request, judge_id):
    judge = get_object_or_404(ArnisJudge, judgeID=judge_id)
    if request.method == 'POST':
        form = ArnisJudges(request.POST, instance=judge)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisJudges(instance=judge)

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-judge.html', {'form': form})

@login_required(login_url='/login')
def add_recorder(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')
    recorders_from_previous_year = []

    # If a previous school year is selected, fetch its recorders
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        recorders_from_previous_year = ArnisRecorder.objects.filter(yearID=previous_school_year)

    if request.method == 'POST':
        # Process selected recorders from the previous year
        selected_recorder_ids = request.POST.getlist('selected_recorders')
        for recorder_id in selected_recorder_ids:
            recorder = get_object_or_404(ArnisRecorder, pk=recorder_id)
            ArnisRecorder.objects.create(
                recorder_name=recorder.recorder_name,
                yearID=school_year
            )

        # Process new recorder if entered
        new_recorder_name = request.POST.get('new_recorder_name')

        if new_recorder_name:
            ArnisRecorder.objects.create(
                recorder_name=new_recorder_name,
                yearID=school_year,
            )

        messages.success(request, "Recorders have been successfully added.")
        return redirect('myapp:arnis_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'is_admin' : is_admin,
        'all_school_years': all_school_years,
        'recorders_from_previous_year': recorders_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    
    return render(request, 'add-recorder.html', context)


@login_required(login_url='/login')
def edit_recorder(request, recorder_id):
    recorder = get_object_or_404(ArnisRecorder, recorderID=recorder_id)
    if request.method == 'POST':
        form = ArnisRecorders(request.POST, instance=recorder)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisRecorders(instance=recorder)

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-recorder.html', {'form': form})

@login_required(login_url='/login')
def add_tabulator(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')
    tabulators_from_previous_year = []

    # If a previous school year is selected, fetch its tabulators
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        tabulators_from_previous_year = ArnisTabulator.objects.filter(yearID=previous_school_year)

    if request.method == 'POST':
        # Process selected tabulators from the previous year
        selected_tabulator_ids = request.POST.getlist('selected_tabulators')
        for tabulator_id in selected_tabulator_ids:
            tabulator = get_object_or_404(ArnisTabulator, pk=tabulator_id)
            ArnisTabulator.objects.create(
                tabulator_name=tabulator.tabulator_name,
                yearID=school_year
            )

        # Process new tabulator if entered
        new_tabulator_name = request.POST.get('new_tabulator_name')

        if new_tabulator_name:
            ArnisTabulator.objects.create(
                tabulator_name=new_tabulator_name,
                yearID=school_year,
            )

        messages.success(request, "Tabulators have been successfully added.")
        return redirect('myapp:arnis_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'is_admin' : is_admin,
        'all_school_years': all_school_years,
        'tabulators_from_previous_year': tabulators_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    
    return render(request, 'add-tabulator.html', context)


@login_required(login_url='/login')
def edit_tabulator(request, tabulator_id):
    tabulator = get_object_or_404(ArnisTabulator, tabulatorID=tabulator_id)
    if request.method == 'POST':
        form = ArnisTabulators(request.POST, instance=tabulator)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisTabulators(instance=tabulator)

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-tabulator.html', {'form': form})

@login_required(login_url='/login')
def add_timer(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')
    timers_from_previous_year = []

    # If a previous school year is selected, fetch its timers
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        timers_from_previous_year = ArnisTimer.objects.filter(yearID=previous_school_year)

    if request.method == 'POST':
        # Process selected timers from the previous year
        selected_timer_ids = request.POST.getlist('selected_timers')
        for timer_id in selected_timer_ids:
            timer = get_object_or_404(ArnisTimer, pk=timer_id)
            ArnisTimer.objects.create(
                timer_name=timer.timer_name,
                yearID=school_year
            )

        # Process new timer if entered
        new_timer_name = request.POST.get('new_timer_name')

        if new_timer_name:
            ArnisTimer.objects.create(
                timer_name=new_timer_name,
                yearID=school_year,
            )

        messages.success(request, "Timers have been successfully added.")
        return redirect('myapp:arnis_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'is_admin' : is_admin,
        'all_school_years': all_school_years,
        'timers_from_previous_year': timers_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    
    return render(request, 'add-timer.html', context)


@login_required(login_url='/login')
def edit_timer(request, timer_id):
    timer = get_object_or_404(ArnisTimer, timerID=timer_id)
    if request.method == 'POST':
        form = ArnisTimers(request.POST, instance=timer)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisTimers(instance=timer)

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-timer.html', {'form': form})

@login_required(login_url='/login')
def add_manager(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')
    managers_from_previous_year = []

    # If a previous school year is selected, fetch its judges
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        managers_from_previous_year = ArnisManager.objects.filter(yearID=previous_school_year)


    if request.method == 'POST':
        # Process selected judges from the previous year
        selected_manager_ids = request.POST.getlist('selected_managers')
        for manager_id in selected_manager_ids:
            manager = get_object_or_404(ArnisManager, pk=manager_id)
            ArnisManager.objects.create(
                manager_name=manager.manager_name,
                yearID=school_year
            )

        # Process new judge if entered
        new_manager_name = request.POST.get('new_manager_name')

        if new_manager_name:
            ArnisManager.objects.create(
                manager_name=new_manager_name,
                yearID=school_year,
            )

        messages.success(request, "Judges have been successfully added.")
        return redirect('myapp:arnis_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'is_admin' : is_admin,
        'all_school_years': all_school_years,
        'managers_from_previous_year': managers_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'add-manager.html', context)

@login_required(login_url='/login')
def edit_manager(request, manager_id):
    manager = get_object_or_404(ArnisManager, managerID=manager_id)
    if request.method == 'POST':
        form = ArnisManagers(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisManagers(instance=manager)

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-manager.html', {'form': form})

@login_required(login_url='/login')
def add_college(request):
    if request.method == 'POST':
        form = Colleges(request.POST)  # Assuming the form is named CollegeForm
        if form.is_valid():
            form.save()
            return redirect('myapp:admin_other_data')
    else:
        form = Colleges()
    return render(request, 'add-college.html', {'form': form})

def admin_required(view_func):
    @login_required(login_url='/admin_login')  # Specify admin_login URL
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_admin:  # Check if the user is an admin
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You are not authorized to access the admin area.")
            return redirect('myapp:admin_login')  # Redirect non-admin users to the admin login page
    return _wrapped_view

@login_required  # Ensures only logged-in users can access the view
def admin_dashboard(request):
    context = {
        'username': request.user,  # Pass the username to the template
    }
    return render(request, 'admin/admin_dashboard.html', context)

@login_required(login_url='/login')
def edit_college(request, college_id):
    college = get_object_or_404(College, collegeID=college_id)
    if request.method == 'POST':
        form = Colleges(request.POST, instance=college)
        if form.is_valid():
            form.save()
            return redirect('myapp:admin_other_data')
    else:
        form = Colleges(instance=college)
    return render(request, 'edit-college.html', {'form': form})


def landing(request):
    return render(request, 'landing.html')

def sports(request):
    return render(request, 'sports.html')

@login_required(login_url='/login')
def arnis(request):
    context = {
        'username': request.user,
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    
    return render(request, 'arnis.html', context)


@login_required(login_url='/login')
def tennis_sport(request):
    context = {
        'username': request.user,
    }
    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'tennis_sport.html', context)

@login_required(login_url='/login')
def arnis_sport(request):
    context = {
        'username': request.user,
    }
    if request.user.sport != 'arnis' and not request.user.is_admin:   
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'arnis_sport.html', context)

@login_required(login_url='/login')
def labanan_auth(request):
     # Check if the user has the sport 'arnis' before proceeding
    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page

    # Open the session for labanan authentication
    request.session['labanan_auth_open'] = True

    school_years = SchoolYear.objects.all().order_by('-start_year')
    colleges = College.objects.all()
    selected_year_id = request.GET.get('school_year')
    
    if selected_year_id:
            selected_year_id = int(selected_year_id)
            school_year = get_object_or_404(SchoolYear, YearID=selected_year_id)
            players = ArnisLabananPlayers.objects.filter(yearID=school_year)
            judges = ArnisJudge.objects.filter(yearID=school_year)
            referees = ArnisReferee.objects.filter(yearID=school_year)
            recorders = ArnisRecorder.objects.filter(yearID=school_year)
    else:
        players = ArnisLabananPlayers.objects.all()
        judges = ArnisJudge.objects.all()
        referees = ArnisReferee.objects.all()
        recorders = ArnisRecorder.objects.all()

    context = {
        'school_years': school_years,
        'colleges': colleges,
        'players': players,
        'judges': judges,
        'referees': referees,
        'recorders': recorders,
        'selected_year_id': selected_year_id,
    }
    return render(request, 'labanan_auth.html', context)

@login_required(login_url='/login')
def tennis(request):
    context = {
        'username': request.user,
    }
    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'table_tennis.html', context)

@login_required(login_url='/login')
def dtennis_sheet(request):
    if request.method == 'POST':
        match_form = DoubleTennisMatchForm(request.POST)
        school_year_id = request.POST.get('school_year')
        school_year_instance = get_object_or_404(SchoolYear, YearID=school_year_id)
        
        if match_form.is_valid():
            match = match_form.save(commit=False)
            match.yearID = school_year_instance
            match.user = request.user
            match.save()

        set1_form = DoublelTennisSetForm(request.POST, instance=DoubleTennisSet(matchID=match), prefix='set1')
        set2_form = DoublelTennisSetForm(request.POST, instance=DoubleTennisSet(matchID=match), prefix='set2')
        set3_form = DoublelTennisSetForm(request.POST, instance=DoubleTennisSet(matchID=match), prefix='set3')
        set4_form = DoublelTennisSetForm(request.POST, instance=DoubleTennisSet(matchID=match), prefix='set4')
        set5_form = DoublelTennisSetForm(request.POST, instance=DoubleTennisSet(matchID=match), prefix='set5')
        player1_score1_form = DoubleTennisScoreForm(request.POST, prefix='player1_score1')
        player1_score2_form = DoubleTennisScoreForm(request.POST, prefix='player1_score2')
        player1_score3_form = DoubleTennisScoreForm(request.POST, prefix='player1_score3')
        player1_score4_form = DoubleTennisScoreForm(request.POST, prefix='player1_score4')
        player1_score5_form = DoubleTennisScoreForm(request.POST, prefix='player1_score5')
        player2_score1_form = DoubleTennisScoreForm(request.POST, prefix='player2_score1')
        player2_score2_form = DoubleTennisScoreForm(request.POST, prefix='player2_score2')
        player2_score3_form = DoubleTennisScoreForm(request.POST, prefix='player2_score3')
        player2_score4_form = DoubleTennisScoreForm(request.POST, prefix='player2_score4')
        player2_score5_form = DoubleTennisScoreForm(request.POST, prefix='player2_score5')

        if set1_form.is_valid() and set2_form.is_valid() and set3_form.is_valid() and set4_form.is_valid() and set5_form.is_valid() and player1_score1_form.is_valid() and player1_score2_form.is_valid() and \
            player1_score3_form.is_valid() and player1_score4_form.is_valid() and player1_score5_form.is_valid() and player2_score1_form.is_valid() and player2_score2_form.is_valid and \
            player2_score3_form.is_valid() and player2_score4_form.is_valid() and player2_score5_form.is_valid():

            winner1 = request.POST.get('winner1')
            winner2 = request.POST.get('winner2')
            winner3 = request.POST.get('winner3')
            winner4 = request.POST.get('winner4')
            winner5 = request.POST.get('winner5')

            player1_id = request.POST.get('player1_name')
            player3_id = request.POST.get('player3_name')

            player1_name = get_object_or_404(TennisPlayers, playerID=player1_id)
            player3_name = get_object_or_404(TennisPlayers, playerID=player3_id)    

            player1_score_1 = request.POST.get('player1_score1')
            player1_score_2 = request.POST.get('player1_score2')
            player1_score_3 = request.POST.get('player1_score3')
            player1_score_4 = request.POST.get('player1_score4')
            player1_score_5 = request.POST.get('player1_score5')

            player2_score_1 = request.POST.get('player2_score1')
            player2_score_2 = request.POST.get('player2_score2')
            player2_score_3 = request.POST.get('player2_score3')
            player2_score_4 = request.POST.get('player2_score4')
            player2_score_5 = request.POST.get('player2_score5')

            set1 = set1_form.save(commit=False)
            set1.matchID = match  # Pass the match instance to set1
            set1.set_no = 1
            set1.winner = winner1
            set1.save()

            set2 = set2_form.save(commit=False)
            set2.matchID = match  # Pass the match instance to set2
            set2.set_no = 2
            set2.winner = winner2
            set2.save()

            set3 = set3_form.save(commit=False)
            set3.matchID = match  # Pass the match instance to set3
            set3.set_no = 3
            set3.winner = winner3
            set3.save()
            
            set4 = set4_form.save(commit=False)
            set4.matchID = match  # Pass the match instance to set3
            set4.set_no = 4
            set4.winner = winner4
            set4.save()
            
            set5 = set5_form.save(commit=False)
            set5.matchID = match  # Pass the match instance to set3
            set5.set_no = 5
            set5.winner = winner5
            set5.save()

            player1_score1 = player1_score1_form.save(commit=False)
            player1_score1.setID = set1  # Pass the match instance to set1
            player1_score1.player = player1_name 
            player1_score1.score = player1_score_1
            player1_score1.save()

            player1_score2 = player1_score2_form.save(commit=False)
            player1_score2.setID = set2  # Pass the match instance to set1
            player1_score2.player = player1_name
            player1_score2.score = player1_score_2
            player1_score2.save()

            player1_score3 = player1_score3_form.save(commit=False)
            player1_score3.setID = set3  # Pass the match instance to set1
            player1_score3.player = player1_name
            player1_score3.score = player1_score_3
            player1_score3.save()

            player1_score4 = player1_score4_form.save(commit=False)
            player1_score4.setID = set4  # Pass the match instance to set1
            player1_score4.player = player1_name
            player1_score4.score = player1_score_4
            player1_score4.save()

            player1_score5 = player1_score5_form.save(commit=False)
            player1_score5.setID = set5  # Pass the match instance to set1
            player1_score5.player = player1_name
            player1_score5.score = player1_score_5
            player1_score5.save()

            player2_score1 = player2_score1_form.save(commit=False)
            player2_score1.setID = set1  # Pass the match instance to set1
            player2_score1.player = player3_name
            player2_score1.score = player2_score_1
            player2_score1.save()

            player2_score2 = player2_score2_form.save(commit=False)
            player2_score2.setID = set2  # Pass the match instance to set1
            player2_score2.player = player3_name
            player2_score2.score = player2_score_2
            player2_score2.save()

            player2_score3 = player2_score3_form.save(commit=False)
            player2_score3.setID = set3  # Pass the match instance to set1
            player2_score3.player = player3_name
            player2_score3.score = player2_score_3
            player2_score3.save()

            player2_score4 = player2_score4_form.save(commit=False)
            player2_score4.setID = set4  # Pass the match instance to set1
            player2_score4.player = player3_name
            player2_score4.score = player2_score_4
            player2_score4.save()

            player2_score5 = player2_score5_form.save(commit=False)
            player2_score5.setID = set5  # Pass the match instance to set1
            player2_score5.player = player3_name
            player2_score5.score = player2_score_5
            player2_score5.save()

        else:
            print("Form errors:", match_form.errors, set1_form.errors, set2_form.errors, set3_form.errors, player1_score1_form.errors, player1_score2_form.errors, player1_score3_form.errors, player1_score4_form.errors, player1_score5_form.errors, player2_score1_form.errors, player2_score2_form.errors, player2_score3_form.errors, player2_score4_form.errors, player2_score5_form.errors)  # Print out form errors for debugging purposes

        print("GET variables:", request.GET)       
        print("POST variables:", request.POST)  

        return redirect('myapp:table_tennis')  # Replace 'success_url' with the URL you want to redirect to after successful submission
    
    else:
        match_form = DoubleTennisMatchForm()
        set1_form = DoublelTennisSetForm(prefix='set1')
        set2_form = DoublelTennisSetForm(prefix='set2')
        set3_form = DoublelTennisSetForm(prefix='set3')
        set4_form = DoublelTennisSetForm(prefix='set4')
        set5_form = DoublelTennisSetForm(prefix='set5')
        player1_score1_form = DoubleTennisScoreForm(request.POST, prefix='player1_score1')
        player1_score2_form = DoubleTennisScoreForm(request.POST, prefix='player1_score2')
        player1_score3_form = DoubleTennisScoreForm(request.POST, prefix='player1_score3')
        player1_score4_form = DoubleTennisScoreForm(request.POST, prefix='player1_score4')
        player1_score5_form = DoubleTennisScoreForm(request.POST, prefix='player1_score5')
        player2_score1_form = DoubleTennisScoreForm(request.POST, prefix='player2_score1')
        player2_score2_form = DoubleTennisScoreForm(request.POST, prefix='player2_score2')
        player2_score3_form = DoubleTennisScoreForm(request.POST, prefix='player2_score3')
        player2_score4_form = DoubleTennisScoreForm(request.POST, prefix='player2_score4')
        player2_score5_form = DoubleTennisScoreForm(request.POST, prefix='player2_score5')

    context = {
        'set1_form': set1_form,
        'set2_form': set2_form,
        'set3_form': set3_form,
        'set4_form' : set4_form,
        'set5_form' : set5_form,
        'player1_score1_form' : player1_score1_form,
        'player1_score2_form' : player1_score2_form,
        'player1_score3_form' : player1_score3_form,
        'player1_score4_form' : player1_score4_form,
        'player1_score5_form' : player1_score5_form,
        'player2_score1_form' : player2_score1_form,
        'player2_score2_form' : player2_score2_form,
        'player2_score3_form' : player2_score3_form,
        'player2_score4_form' : player2_score4_form,
        'player2_score5_form' : player2_score5_form,
        'match_form': match_form,
        'username': request.user,
    }

    if not request.session.get('dtennis_auth_open'):
        return redirect('myapp:dtennis_auth')  # Redirect to the auth form if not accessed

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'dtennis_sheet.html', context)


@login_required(login_url='/login')
def stennis_auth(request):
    request.session['stennis_auth_open'] = True
    school_years = SchoolYear.objects.all().order_by('-start_year')
    colleges = College.objects.all()
    selected_year_id = request.GET.get('school_year')

    if selected_year_id:
        school_year = get_object_or_404(SchoolYear, YearID=selected_year_id)
        players = TennisPlayers.objects.filter(yearID=selected_year_id)
        coaches = TennisCoach.objects.filter(yearID=selected_year_id)
        umpires = TennisUmpire.objects.filter(yearID=selected_year_id)

    else:
        players = TennisPlayers.objects.all()
        coaches = TennisCoach.objects.all()
        umpires = TennisUmpire.objects.all()

    context = {
        'school_years': school_years,
        'players' : players,
        'colleges': colleges,
        'coaches': coaches,
        'umpires': umpires,
        'selected_year_id': selected_year_id,
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'stennis_auth.html', context)

@login_required(login_url='/login')
def dtennis_auth(request):
    request.session['dtennis_auth_open'] = True
    
    school_years = SchoolYear.objects.all().order_by('-start_year')
    colleges = College.objects.all()
    selected_year_id = request.GET.get('school_year')

    if selected_year_id:
        school_year = get_object_or_404(SchoolYear, YearID=selected_year_id)
        players = TennisPlayers.objects.filter(yearID=selected_year_id)
        coaches = TennisCoach.objects.filter(yearID=selected_year_id)
        umpires = TennisUmpire.objects.filter(yearID=selected_year_id)

    else:
        players = TennisPlayers.objects.all()
        coaches = TennisCoach.objects.all()
        umpires = TennisUmpire.objects.all()

    context = {
        'school_years': school_years,
        'players' : players,
        'colleges': colleges,
        'coaches': coaches,
        'umpires': umpires,
        'selected_year_id': selected_year_id,
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'dtennis_auth.html', context)

@login_required(login_url='/login')
def stennis_sheet(request):
    if request.method == 'POST':
        match_form = SingleTennisMatchForm(request.POST)
        school_year_id = request.POST.get('school_year')
        school_year_instance = get_object_or_404(SchoolYear, YearID=school_year_id)
        if match_form.is_valid():
            match = match_form.save(commit=False)
            match.yearID = school_year_instance
            match.user = request.user
            match.save()

        set1_form = SingleTennisSetForm(request.POST, instance=SingleTennisSet(matchID=match), prefix='set1')
        set2_form = SingleTennisSetForm(request.POST, instance=SingleTennisSet(matchID=match), prefix='set2')
        set3_form = SingleTennisSetForm(request.POST, instance=SingleTennisSet(matchID=match), prefix='set3')
        set4_form = SingleTennisSetForm(request.POST, instance=SingleTennisSet(matchID=match), prefix='set4')
        set5_form = SingleTennisSetForm(request.POST, instance=SingleTennisSet(matchID=match), prefix='set5')
        player1_score1_form = SingleTennisScoreForm(request.POST, prefix='player1_score1')
        player1_score2_form = SingleTennisScoreForm(request.POST, prefix='player1_score2')
        player1_score3_form = SingleTennisScoreForm(request.POST, prefix='player1_score3')
        player1_score4_form = SingleTennisScoreForm(request.POST, prefix='player1_score4')
        player1_score5_form = SingleTennisScoreForm(request.POST, prefix='player1_score5')
        player2_score1_form = SingleTennisScoreForm(request.POST, prefix='player2_score1')
        player2_score2_form = SingleTennisScoreForm(request.POST, prefix='player2_score2')
        player2_score3_form = SingleTennisScoreForm(request.POST, prefix='player2_score3')
        player2_score4_form = SingleTennisScoreForm(request.POST, prefix='player2_score4')
        player2_score5_form = SingleTennisScoreForm(request.POST, prefix='player2_score5')

        if set1_form.is_valid() and set2_form.is_valid() and set3_form.is_valid() and set4_form.is_valid() and set5_form.is_valid() and player1_score1_form.is_valid() and player1_score2_form.is_valid() and \
            player1_score3_form.is_valid() and player1_score4_form.is_valid() and player1_score5_form.is_valid() and player2_score1_form.is_valid() and player2_score2_form.is_valid and \
            player2_score3_form.is_valid() and player2_score4_form.is_valid() and player2_score5_form.is_valid():

            winner1 = request.POST.get('winner1')
            winner2 = request.POST.get('winner2')
            winner3 = request.POST.get('winner3')
            winner4 = request.POST.get('winner4')
            winner5 = request.POST.get('winner5')

            player1_id = request.POST.get('player1_name')
            player2_id = request.POST.get('player2_name')

            player1_name = get_object_or_404(TennisPlayers, playerID=player1_id)
            player2_name = get_object_or_404(TennisPlayers, playerID=player2_id)


            player1_score_1 = request.POST.get('player1_score1')
            player1_score_2 = request.POST.get('player1_score2')
            player1_score_3 = request.POST.get('player1_score3')
            player1_score_4 = request.POST.get('player1_score4')
            player1_score_5 = request.POST.get('player1_score5')

            player2_score_1= request.POST.get('player2_score1')
            player2_score_2 = request.POST.get('player2_score2')
            player2_score_3 = request.POST.get('player2_score3')
            player2_score_4 = request.POST.get('player2_score4')
            player2_score_5 = request.POST.get('player2_score5')

            set1 = set1_form.save(commit=False)
            set1.matchID = match  # Pass the match instance to set1
            set1.set_no = 1
            set1.winner = winner1
            set1.save()

            set2 = set2_form.save(commit=False)
            set2.matchID = match  # Pass the match instance to set2
            set2.set_no = 2
            set2.winner = winner2
            set2.save()

            set3 = set3_form.save(commit=False)
            set3.matchID = match  # Pass the match instance to set3
            set3.set_no = 3
            set3.winner = winner3
            set3.save()
            
            set4 = set4_form.save(commit=False)
            set4.matchID = match  # Pass the match instance to set3
            set4.set_no = 4
            set4.winner = winner4
            set4.save()
            
            set5 = set5_form.save(commit=False)
            set5.matchID = match  # Pass the match instance to set3
            set5.set_no = 5
            set5.winner = winner5
            set5.save()

            player1_score1 = player1_score1_form.save(commit=False)
            player1_score1.setID = set1  # Pass the match instance to set1
            player1_score1.player = player1_name
            player1_score1.score = player1_score_1
            player1_score1.save()

            player1_score2 = player1_score2_form.save(commit=False)
            player1_score2.setID = set2  # Pass the match instance to set1
            player1_score2.player = player1_name
            player1_score2.score = player1_score_2
            player1_score2.save()

            player1_score3 = player1_score3_form.save(commit=False)
            player1_score3.setID = set3  # Pass the match instance to set1
            player1_score3.player = player1_name
            player1_score3.score = player1_score_3
            player1_score3.save()

            player1_score4 = player1_score4_form.save(commit=False)
            player1_score4.setID = set4  # Pass the match instance to set1
            player1_score4.player = player1_name
            player1_score4.score = player1_score_4
            player1_score4.save()

            player1_score5 = player1_score5_form.save(commit=False)
            player1_score5.setID = set5  # Pass the match instance to set1
            player1_score5.player = player1_name
            player1_score5.score = player1_score_5
            player1_score5.save()

            player2_score1 = player2_score1_form.save(commit=False)
            player2_score1.setID = set1  # Pass the match instance to set1
            player2_score1.player = player2_name
            player2_score1.score = player2_score_1
            player2_score1.save()

            player2_score2 = player2_score2_form.save(commit=False)
            player2_score2.setID = set2  # Pass the match instance to set1
            player2_score2.player = player2_name
            player2_score2.score = player2_score_2
            player2_score2.save()

            player2_score3 = player2_score3_form.save(commit=False)
            player2_score3.setID = set3  # Pass the match instance to set1
            player2_score3.player = player2_name
            player2_score3.score = player2_score_3
            player2_score3.save()

            player2_score4 = player2_score4_form.save(commit=False)
            player2_score4.setID = set4  # Pass the match instance to set1
            player2_score4.player = player2_name
            player2_score4.score = player2_score_4
            player2_score4.save()

            player2_score5 = player2_score5_form.save(commit=False)
            player2_score5.setID = set5  # Pass the match instance to set1
            player2_score5.player = player2_name
            player2_score5.score = player2_score_5
            player2_score5.save()

        else:
            print("Form errors:", match_form.errors, set1_form.errors, set2_form.errors, set3_form.errors, player1_score1_form.errors, player1_score2_form.errors, player1_score3_form.errors, player1_score4_form.errors, player1_score5_form.errors, player2_score1_form.errors, player2_score2_form.errors, player2_score3_form.errors, player2_score4_form.errors, player2_score5_form.errors)  # Print out form errors for debugging purposes

        print("GET variables:", request.GET)       
        print("POST variables:", request.POST)  

        return redirect('myapp:table_tennis')  # Replace 'success_url' with the URL you want to redirect to after successful submission
    
    else:
        match_form = SingleTennisMatchForm()
        set1_form = SingleTennisSetForm(prefix='set1')
        set2_form = SingleTennisSetForm(prefix='set2')
        set3_form = SingleTennisSetForm(prefix='set3')
        set4_form = SingleTennisSetForm(prefix='set4')
        set5_form = SingleTennisSetForm(prefix='set5')
        player1_score1_form = SingleTennisScoreForm(request.POST, prefix='player1_score1')
        player1_score2_form = SingleTennisScoreForm(request.POST, prefix='player1_score2')
        player1_score3_form = SingleTennisScoreForm(request.POST, prefix='player1_score3')
        player1_score4_form = SingleTennisScoreForm(request.POST, prefix='player1_score4')
        player1_score5_form = SingleTennisScoreForm(request.POST, prefix='player1_score5')
        player2_score1_form = SingleTennisScoreForm(request.POST, prefix='player2_score1')
        player2_score2_form = SingleTennisScoreForm(request.POST, prefix='player2_score2')
        player2_score3_form = SingleTennisScoreForm(request.POST, prefix='player2_score3')
        player2_score4_form = SingleTennisScoreForm(request.POST, prefix='player2_score4')
        player2_score5_form = SingleTennisScoreForm(request.POST, prefix='player2_score5')

    context = {
        'set1_form': set1_form,
        'set2_form': set2_form,
        'set3_form': set3_form,
        'set4_form' : set4_form,
        'set5_form' : set5_form,
        'player1_score1_form' : player1_score1_form,
        'player1_score2_form' : player1_score2_form,
        'player1_score3_form' : player1_score3_form,
        'player1_score4_form' : player1_score4_form,
        'player1_score5_form' : player1_score5_form,
        'player2_score1_form' : player2_score1_form,
        'player2_score2_form' : player2_score2_form,
        'player2_score3_form' : player2_score3_form,
        'player2_score4_form' : player2_score4_form,
        'player2_score5_form' : player2_score5_form,
        'match_form': match_form,
        'username': request.user,
    }

    if not request.session.get('stennis_auth_open'):
        return redirect('myapp:stennis_auth')  # Redirect to the auth form if not accessed

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'stennis_sheet.html', context)

@login_required(login_url='/login')
def stennis_scoreboard(request):
    school_years = SchoolYear.objects.all().order_by('-start_year')
    selected_year_id = request.GET.get('school_year')
    
    if selected_year_id:
        players = TennisPlayers.objects.filter(yearID=selected_year_id)
    else:
        players = TennisPlayers.objects.all()
    
    context = {
        'school_years': school_years,
        'players': players,
        'selected_year_id': selected_year_id,  # Keep track of the selected school year
        'username': request.user,
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'stennis_scoreboard.html', context)

@login_required(login_url='/login')
def dtennis_scoreboard(request):
    school_years = SchoolYear.objects.all().order_by('-start_year')
    selected_year_id = request.GET.get('school_year')
    
    if selected_year_id:
        players = TennisPlayers.objects.filter(yearID=selected_year_id)
    else:
        players = TennisPlayers.objects.all()
    
    context = {
        'school_years': school_years,
        'players': players,
        'selected_year_id': selected_year_id,  # Keep track of the selected school year
        'username': request.user
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'dtennis_scoreboard.html', context)

@login_required(login_url='/login')
def arnis_school_year(request):
    school_years = SchoolYear.objects.order_by('-start_year').first()
    colleges = College.objects.all()

    context = {
        'school_years' : school_years,
        'colleges' : colleges,
        'username': request.user,
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'arnis_data.html', context)

@login_required(login_url='/login')
def arnis_details(request, year_id):
    school_year = get_object_or_404(SchoolYear, YearID=year_id)
    labanan_players = ArnisLabananPlayers.objects.filter(yearID=school_year)
    form_players = ArnisFormPlayers.objects.filter(yearID=school_year)
    referees = ArnisReferee.objects.filter(yearID=school_year)
    recorders = ArnisRecorder.objects.filter(yearID=school_year)
    tabulators = ArnisTabulator.objects.filter(yearID=school_year)
    judges = ArnisJudge.objects.filter(yearID=school_year)
    timers = ArnisTimer.objects.filter(yearID=school_year)
    managers = ArnisManager.objects.filter(yearID=school_year)


    context = {
        'school_year': school_year,
        'labanan_players': labanan_players,
        'form_players': form_players,
        'referees': referees,
        'recorders': recorders,
        'tabulators': tabulators,
        'judges': judges,
        'timers': timers,
        'managers': managers,
        'username': request.user,
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'arnis_details.html', context)

@login_required(login_url='/login')
def volleyball_school_year(request):
    school_years = SchoolYear.objects.order_by('-start_year').first()
    colleges = College.objects.all()

    context = {
        'school_years' : school_years,
        'colleges' : colleges,
        'username' : request.user,
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'volleyball_data.html', context)

@login_required(login_url='/login')
def tennis_school_year(request):
    school_years = SchoolYear.objects.order_by('-start_year').first()
    colleges = College.objects.all()

    context = {
        'school_years' : school_years,
        'colleges' : colleges,
        'username': request.user,
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page

    return render(request, 'tennis_data.html', context)

@login_required(login_url='/login')
def volleyball_details(request, year_id):
    school_year = get_object_or_404(SchoolYear, YearID=year_id)
    volleyball_team = VolleyballTeam.objects.filter(yearID=school_year)
    referees = VolleyballReferee.objects.filter(yearID=school_year)
    scorer = VolleyballScorer.objects.filter(yearID=school_year)
    judge = VolleyballJudge.objects.filter(yearID=school_year)

    # Create a dictionary to store players categorized by team
    team_players = {}

    # Populate the team_players dictionary
    for team in volleyball_team:
        players_for_team = VolleyballPlayer.objects.filter(teamID=team)
        team_players[team] = players_for_team

    context = {
        'school_year': school_year,
        'volleyball_team': volleyball_team,
        'team_players': team_players,
        'referees': referees,
        'scorer': scorer,
        'judge': judge,
         'username': request.user,

    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'volleyball_details.html', context)

@login_required(login_url='/login')
def tennis_details(request, year_id):
    school_year = get_object_or_404(SchoolYear, YearID=year_id)
    players = TennisPlayers.objects.filter(yearID=school_year)
    umpires = TennisUmpire.objects.filter(yearID=school_year)
    coaches = TennisCoach.objects.filter(yearID=school_year)

    context = {
        'school_year': school_year,
        'players': players,
        'umpires': umpires,
        'coaches': coaches,
        'username': request.user,
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'tennis_details.html', context)

@login_required(login_url='/login')
def arnis_labanan(request):
    school_years = SchoolYear.objects.all().order_by('-start_year')
    selected_year_id = request.GET.get('school_year')
    
    if selected_year_id:
        players = ArnisLabananPlayers.objects.filter(yearID=selected_year_id)
    else:
        players = ArnisLabananPlayers.objects.all()
    
    context = {
        'school_years': school_years,
        'players': players,
        'selected_year_id': selected_year_id,  # Keep track of the selected school year
        'username': request.user,
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'arnis_labanan.html', context)

@login_required(login_url='/login')
def labanan_display(request):
    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'labanan_display.html')


@login_required(login_url='/login')
def volleyball_display(request):
    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'volleyball_display.html')

@login_required(login_url='/login')
def stennis_display(request):
    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'stennis_display.html')

@login_required(login_url='/login')
def dtennis_display(request):
    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'dtennis_display.html')

@login_required(login_url='/login')
def volleyball_auth(request):
    request.session['volleyball_auth_open'] = True

    school_years = SchoolYear.objects.all().order_by('-start_year')
    colleges = College.objects.all()
    selected_year_id = request.GET.get('school_year')

    if selected_year_id:
        school_year = get_object_or_404(SchoolYear, YearID=selected_year_id)
        judges = VolleyballJudge.objects.filter(yearID=selected_year_id)
        referees = VolleyballReferee.objects.filter(yearID=selected_year_id)
        scorers = VolleyballScorer.objects.filter(yearID=selected_year_id)

    else:
        judges = VolleyballJudge.objects.all()
        referees = VolleyballReferee.objects.all()
        scorers = VolleyballScorer.objects.all()

    context = {   
        'school_years': school_years,
        'colleges': colleges,
        'judges': judges,
        'referees': referees,
        'scorers': scorers,
        'selected_year_id': selected_year_id,
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'volleyball_auth.html', context)

@login_required(login_url='/login')
def volleyball_sheet(request):
    home_team_id = request.POST.get('home_team')
    away_team_id = request.POST.get('away_team')

    if request.method == 'POST':
        match_form = VolleyballMatchForm(request.POST)
        school_year_id = request.POST.get('school_year')
        school_year_instance = get_object_or_404(SchoolYear, YearID=school_year_id)
        if match_form.is_valid():
            match = match_form.save(commit=False)
            match.yearID = school_year_instance
            match.user = request.user
            match.save()

        player_names = request.POST.getlist('player[]')
        points = request.POST.getlist('points[]')
        teams = request.POST.getlist('team[]')

        for i in range(len(player_names)):
            player_name = player_names[i]
            if not player_name:
                continue  # Skip if player name is not provided

            points_value = points[i]
            team_value = teams[i]

            player_data = {
                'player': player_name,
                'points': points_value,
                'team': team_value
            }
            
            player_form = VolleyballMatchPlayersForm(player_data)

            if player_form.is_valid():
                player = player_form.save(commit=False)
                player.matchID = match  # Ensure match is defined earlier in the view
                player.save()

        set1_form = VolleyballSetForm(request.POST, instance=VolleyballSet(matchID=match), prefix='set1')
        set2_form = VolleyballSetForm(request.POST, instance=VolleyballSet(matchID=match), prefix='set2')
        set3_form = VolleyballSetForm(request.POST, instance=VolleyballSet(matchID=match), prefix='set3')
        home1_score_form = VolleyballScoreForm(request.POST, prefix='h_score1')
        home2_score_form = VolleyballScoreForm(request.POST, prefix='h_score2')
        home3_score_form = VolleyballScoreForm(request.POST, prefix='h_score3')
        away1_score_form = VolleyballScoreForm(request.POST, prefix='a_score1')
        away2_score_form = VolleyballScoreForm(request.POST, prefix='a_score2')
        away3_score_form = VolleyballScoreForm(request.POST, prefix='a_score3')

        if set1_form.is_valid() and set2_form.is_valid() and set3_form.is_valid():

            time1 = request.POST.get('time1')
            time2 = request.POST.get('time2')
            time3 = request.POST.get('time3')

            winner1 = request.POST.get('winner1')
            winner2 = request.POST.get('winner2')
            winner3 = request.POST.get('winner3')

            home_team = get_object_or_404(VolleyballTeam, teamID=home_team_id)
            away_team = get_object_or_404(VolleyballTeam, teamID=away_team_id)

            home_score1 = request.POST.get('home_score1')
            home_score2 = request.POST.get('home_score2')
            home_score3 = request.POST.get('home_score3')
            home_timeout = request.POST.get('home_timeout')

            away_score1 = request.POST.get('away_score1')
            away_score2 = request.POST.get('away_score2')
            away_score3 = request.POST.get('away_score3')
            away_timeout = request.POST.get('away_timeout')

            set1 = set1_form.save(commit=False)
            set1.matchID = match  # Pass the match instance to set1
            set1.set_no = 1
            set1.time = time1
            set1.winner = winner1
            set1.save()

            set2 = set2_form.save(commit=False)
            set2.matchID = match  # Pass the match instance to set2
            set2.set_no = 2
            set2.time = time2
            set2.winner = winner2
            set2.save()

            set3 = set3_form.save(commit=False)
            set3.matchID = match  # Pass the match instance to set3
            set3.set_no = 3
            set3.time = time3
            set3.winner = winner3
            set3.save()

            h_score1 = home1_score_form.save(commit=False)
            h_score1.setID = set1  # Pass the match instance to set1
            h_score1.team = home_team
            h_score1.score = home_score1
            h_score1.timeout_used = home_timeout
            h_score1.save()

            h_score2 = home2_score_form.save(commit=False)
            h_score2.setID = set2 # Pass the match instance to set1
            h_score2.team = home_team
            h_score2.score = home_score2
            h_score2.timeout_used = home_timeout
            h_score2.save()

            h_score3 = home3_score_form.save(commit=False)
            h_score3.setID = set3  # Pass the match instance to set1
            h_score3.team = home_team
            h_score3.score = home_score3
            h_score3.timeout_used = home_timeout
            h_score3.save()

            a_score1 = away1_score_form.save(commit=False)
            a_score1.setID = set1  # Pass the match instance to set1
            a_score1.team = away_team
            a_score1.score = away_score1
            a_score1.timeout_used = away_timeout
            a_score1.save()

            a_score2 = away2_score_form.save(commit=False)
            a_score2.setID = set2 # Pass the match instance to set1
            a_score2.team = away_team
            a_score2.score = away_score2
            a_score2.timeout_used = away_timeout
            a_score2.save()

            a_score3 = away3_score_form.save(commit=False)
            a_score3.setID = set3  # Pass the match instance to set1
            a_score3.team = away_team
            a_score3.score = away_score3
            a_score3.timeout_used = away_timeout
            a_score3.save()

        else:
            print("Form errors:", match_form.errors, set1_form.errors, set2_form.errors, set3_form.errors, home1_score_form.errors, home2_score_form.errors, home3_score_form.errors, away1_score_form.errors, away2_score_form.errors, away3_score_form.errors, player_form.errors)  # Print out form errors for debugging purposes

        print("GET variables:", request.GET)       
        print("POST variables:", request.POST)  

        return redirect('myapp:volleyball')  # Replace 'success_url' with the URL you want to redirect to after successful submission
    
    else:
        player_form = VolleyballMatchPlayersForm()
        match_form = VolleyballMatchForm()
        set1_form = VolleyballSetForm(prefix='set1')
        set2_form = VolleyballSetForm(prefix='set2')
        set3_form = VolleyballSetForm(prefix='set3')
        home1_score_form = VolleyballScoreForm(request.POST, prefix='h_score1')
        home2_score_form = VolleyballScoreForm(request.POST, prefix='h_score2')
        home3_score_form = VolleyballScoreForm(request.POST, prefix='h_score3')
        away1_score_form = VolleyballScoreForm(request.POST, prefix='a_score1')
        away2_score_form = VolleyballScoreForm(request.POST, prefix='a_score2')
        away3_score_form = VolleyballScoreForm(request.POST, prefix='a_score3')      

    context = {
        'player_form': player_form,
        'home1_score_form': home1_score_form,
        'home2_score_form' : home2_score_form,
        'home3_score_form' : home3_score_form,
        'away1_score_form' : away1_score_form,
        'away2_score_form' : away2_score_form,
        'away3_score_form'  : away3_score_form,
        'set1_form': set1_form,
        'set2_form': set2_form,
        'set3_form': set3_form,
        'match_form': match_form,
        'username': request.user,        
    }
    
    if not request.session.get('volleyball_auth_open'):
        return redirect('myapp:volleyball_auth')  # Redirect to the auth form if not accessed

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    
    return render(request, 'volleyball_sheet.html', context)

@login_required(login_url='/login')
def labanan_sheet(request):
    if request.method == 'POST':
        match_form = LabananMatchForm(request.POST)
        round_form_1 = LabananRoundForm(request.POST, prefix='round1')
        round_form_2 = LabananRoundForm(request.POST, prefix='round2')
        round_form_3 = LabananRoundForm(request.POST, prefix='round3')
        red_score_form_1 = LabananScoreForm(request.POST, prefix='r_score1')
        red_score_form_2 = LabananScoreForm(request.POST, prefix='r_score2')
        red_score_form_3 = LabananScoreForm(request.POST, prefix='r_score3')
        blue_score_form_1 = LabananScoreForm(request.POST, prefix='b_score1')
        blue_score_form_2 = LabananScoreForm(request.POST, prefix='b_score2')
        blue_score_form_3 = LabananScoreForm(request.POST, prefix='b_score3')

        if match_form.is_valid() and round_form_1.is_valid() and round_form_2.is_valid() and round_form_3.is_valid() and \
           red_score_form_1.is_valid() and red_score_form_2.is_valid() and red_score_form_3.is_valid() and \
           blue_score_form_1.is_valid() and blue_score_form_2.is_valid() and blue_score_form_3.is_valid():
            
            school_year_id = request.POST.get('school_year')
            school_year_instance = get_object_or_404(SchoolYear, YearID=school_year_id)

            time1 = request.POST.get('time1')
            time2 = request.POST.get('time2')
            time3 = request.POST.get('time3')

            winner1 = request.POST.get('winner1')
            winner2 = request.POST.get('winner2')
            winner3 = request.POST.get('winner3')

            red_score1 = request.POST.get('red_score1') 
            red_score2 = request.POST.get('red_score2')
            red_score3 = request.POST.get('red_score3')

            blue_score1 = request.POST.get('blue_score1') 
            blue_score2 = request.POST.get('blue_score2')
            blue_score3 = request.POST.get('blue_score3')

            red_foul1 = request.POST.get('red_foul1') 
            red_foul2 = request.POST.get('red_foul2')
            red_foul3 = request.POST.get('red_foul3')

            blue_foul1 = request.POST.get('blue_foul1') 
            blue_foul2 = request.POST.get('blue_foul2')
            blue_foul3 = request.POST.get('blue_foul3')

            red_disarmed1 = request.POST.get('red_disarmed1') 
            red_disarmed2 = request.POST.get('red_disarmed2')
            red_disarmed3 = request.POST.get('red_disarmed3')

            blue_disarmed1 = request.POST.get('blue_disarmed1') 
            blue_disarmed2 = request.POST.get('blue_disarmed2')
            blue_disarmed3 = request.POST.get('blue_disarmed3')

            red_total_score1 = request.POST.get('red_total_score1') 
            red_total_score2 = request.POST.get('red_total_score2')
            red_total_score3 = request.POST.get('red_total_score3')

            blue_total_score1 = request.POST.get('blue_total_score1') 
            blue_total_score2 = request.POST.get('blue_total_score2')
            blue_total_score3 = request.POST.get('blue_total_score3')
            
            match = match_form.save(commit=False)
            match.yearID = school_year_instance
            match.user = request.user  # Save the logged-in user
            match.save()

            round1 = round_form_1.save(commit=False)
            round1.matchID = match
            round1.round_num = 1
            round1.time = time1
            round1.winner = winner1
            round1.save()

            round2 = round_form_2.save(commit=False)
            round2.matchID = match
            round2.round_num = 2
            round2.time = time2
            round2.winner = winner2
            round2.save()

            round3 = round_form_3.save(commit=False)
            round3.matchID = match
            round3.round_num = 3
            round3.time = time3
            round3.winner = winner3
            round3.save()

            r_score1 = red_score_form_1.save(commit=False)
            r_score1.roundID = round1
            r_score1.playerID = match.red_player
            r_score1.score = red_score1
            r_score1.foul = red_foul1
            r_score1.disarmed = red_disarmed1
            r_score1.total_score = red_total_score1
            r_score1.save()

            r_score2 = red_score_form_2.save(commit=False)
            r_score2.roundID = round2
            r_score2.playerID = match.red_player
            r_score2.score = red_score2
            r_score2.foul = red_foul2
            r_score2.disarmed = red_disarmed2
            r_score2.total_score = red_total_score2
            r_score2.save()

            r_score3 = red_score_form_3.save(commit=False)
            r_score3.roundID = round3
            r_score3.playerID = match.red_player
            r_score3.score = red_score3
            r_score3.foul = red_foul3
            r_score3.disarmed = red_disarmed3
            r_score3.total_score = red_total_score3
            r_score3.save()

            b_score1 = blue_score_form_1.save(commit=False)
            b_score1.roundID = round1
            b_score1.playerID = match.blue_player
            b_score1.score = blue_score1
            b_score1.foul = blue_foul1
            b_score1.disarmed = blue_disarmed1
            b_score1.total_score = blue_total_score1
            b_score1.save()

            b_score2 = blue_score_form_2.save(commit=False)
            b_score2.roundID = round2
            b_score2.playerID = match.blue_player
            b_score2.score = blue_score2
            b_score2.foul = blue_foul2
            b_score2.disarmed = blue_disarmed2
            b_score2.total_score = blue_total_score2
            b_score2.save()

            b_score3 = blue_score_form_3.save(commit=False)
            b_score3.roundID = round3
            b_score3.playerID = match.blue_player
            b_score3.score = blue_score3
            b_score3.foul = blue_foul3
            b_score3.disarmed = blue_disarmed3
            b_score3.total_score = blue_total_score3
            b_score3.save()

            return redirect('myapp:arnis')

    else:
        match_form = LabananMatchForm()
        round_form_1 = LabananRoundForm(prefix='round1')
        round_form_2 = LabananRoundForm(prefix='round2')
        round_form_3 = LabananRoundForm(prefix='round3')
        red_score_form_1 = LabananScoreForm(prefix='r_score1')
        red_score_form_2 = LabananScoreForm(prefix='r_score2')
        red_score_form_3 = LabananScoreForm(prefix='r_score_3')
        blue_score_form_1 = LabananScoreForm(prefix='b_score1')
        blue_score_form_2 = LabananScoreForm(prefix='b_score2')
        blue_score_form_3 = LabananScoreForm(prefix='b_score3')

    context = {
        'match_form': match_form,
        'round_form_1': round_form_1,
        'round_form_2': round_form_2,
        'round_form_3': round_form_3,
        'red_score_form_1': red_score_form_1,
        'red_score_form_2': red_score_form_2,
        'red_score_form_3': red_score_form_3,
        'blue_score_form_1': blue_score_form_1,
        'blue_score_form_2': blue_score_form_2,
        'blue_score_form_3': blue_score_form_3,
        'username': request.user,
    }

    if not request.session.get('labanan_auth_open'):
        return redirect('myapp:labanan_auth')  # Redirect to the auth form if not accessed

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    
    return render(request, 'labanan_sheet.html', context)

@login_required(login_url='/login')
def arnis_anyo(request):
    school_years = SchoolYear.objects.all().order_by('-start_year')
    selected_year_id = request.GET.get('school_year')
    
    if selected_year_id:
        players = ArnisFormPlayers.objects.filter(yearID=selected_year_id)
    else:
        players = ArnisFormPlayers.objects.all()

    context = {
        'school_years': school_years,
        'players': players,
        'selected_year_id': selected_year_id,  # Keep track of the selected school year
        'username': request.user,
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'arnis_anyo.html', context)

@login_required(login_url='/login')
def players_list(request):
    school_year_id = request.GET.get('school_year')
    if school_year_id:
        players = list(ArnisFormPlayers.objects.filter(yearID=school_year_id).values('playerID', 'player_name'))
    else:
        players = list(ArnisFormPlayers.objects.all().values('playerID', 'player_name'))
    return JsonResponse({'players': players})

@login_required(login_url='/login')
def anyo_display(request):
    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'anyo_display.html')

@login_required(login_url='/login')
def anyo_auth(request):    
    request.session['anyo_auth_open'] = True

    school_years = SchoolYear.objects.all().order_by('-start_year')
    selected_year_id = request.GET.get('school_year')
    school_year = None  # Define school_year here to ensure its availability throughout

    if selected_year_id:
        school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        tabulators = ArnisTabulator.objects.filter(yearID=school_year)
        timers = ArnisTimer.objects.filter(yearID=school_year)
        managers = ArnisManager.objects.filter(yearID=school_year)
    else:
        tabulators = ArnisTabulator.objects.all()
        timers = ArnisTimer.objects.all()
        managers = ArnisManager.objects.all()

    context = {
        'school_years': school_years,
        'tabulators': tabulators,
        'timers': timers,
        'managers': managers,
        'selected_year_id': selected_year_id,
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page

    return render(request, 'anyo_auth.html', context)

@login_required(login_url='/login')
def anyo_sheet(request):
    if request.method == 'POST':
        # Retrieve YearID directly from the POST request
        year_id = request.POST.get('school_year')

        # Ensure that the school year instance exists
        school_year_instance = get_object_or_404(SchoolYear, YearID=year_id)

        anyo_form = AnyoMatchForm(request.POST)

        if anyo_form.is_valid():
            with transaction.atomic():
                # Save the main match form without committing yet
                form_match = anyo_form.save(commit=False)
                form_match.yearID = school_year_instance  # Link to the school year
                form_match.user = request.user  # Link to the school year
                form_match.save()  # Now save the form instance

                # Save all player-related data
                for i in range(20):
                    player_id = request.POST.get(f'playerID_{i}')
                    
                    if not player_id:
                        continue  # Skip if player ID is not provided

                    try:
                        player_instance = ArnisFormPlayers.objects.get(pk=player_id)
                    except ArnisFormPlayers.DoesNotExist:
                        continue  # Skip if the player does not exist

                    # Gather the player's data
                    player_data = {
                        'judgeScores1': request.POST.get(f'judgeScores1_{i}', 0),
                        'judgeScores2': request.POST.get(f'judgeScores2_{i}', 0),
                        'judgeScores3': request.POST.get(f'judgeScores3_{i}', 0),
                        'judgeScores4': request.POST.get(f'judgeScores4_{i}', 0),
                        'judgeScores5': request.POST.get(f'judgeScores5_{i}', 0),
                        'time': request.POST.get(f'time_{i}', 0),
                        'lost_control': request.POST.get(f'lost_control_{i}', 0),
                        'outside': request.POST.get(f'outside_{i}', 0),
                        'other': request.POST.get(f'other_{i}', 0),
                        'time_consumed': request.POST.get(f'time_consumed_{i}', ''),
                        'rank': request.POST.get(f'rank_{i}', 0),
                        'total_score': request.POST.get(f'total_score_{i}', 0),
                    }

                    player_form = AnyoPlayersForm(player_data)
                    if player_form.is_valid():
                        player = player_form.save(commit=False)
                        player.formID = form_match  
                        player.playerID = player_instance  
                        player.save() 
                    else:
                        print(player_form.errors)  # Debugging purposes

                return redirect('myapp:arnis')  # Redirect on successful submission

    # For GET request or if the form is not valid
    context = {
        'anyo_form': AnyoMatchForm(),  # Provide an empty form on GET requests
        'username': request.user,
    }

    if not request.session.get('anyo_auth_open'):
        return redirect('myapp:anyo_auth')  # Redirect to the auth form if not accessed

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page

    return render(request, 'anyo_sheet.html', context)

@login_required(login_url='/login')
def arnis_bracket(request):
    school_years = SchoolYear.objects.all().order_by('-start_year')
    selected_year_id = request.GET.get('school_year')
    
    if selected_year_id:
        players = ArnisLabananPlayers.objects.filter(yearID=selected_year_id)
    else:
        players = ArnisLabananPlayers.objects.all()
    
    context = {
        'school_years': school_years,
        'players': players,
        'selected_year_id': selected_year_id,  # Keep track of the selected school year
        'username': request.user,
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'arnis_bracket.html', context)

@login_required(login_url='/login')
def bracket_list(request):
    school_year_id = request.GET.get('school_year')
    if school_year_id:
        players = list(ArnisLabananPlayers.objects.filter(yearID=school_year_id).values('playerID', 'player_name'))
    else:
        players = list(ArnisLabananPlayers.objects.all().values('playerID', 'player_name'))
    return JsonResponse({'players': players})

def bracket_list1(request):
    school_year_id = request.GET.get('school_year')
    if school_year_id:
        players = list(ArnisFormPlayers.objects.filter(yearID=school_year_id).values('playerID', 'player_name'))
    else:
        players = list(ArnisFormPlayers.objects.all().values('playerID', 'player_name'))
    return JsonResponse({'players': players})

@login_required(login_url='/login')
def volleyball(request):
    context = {
        'username': request.user,
    }
    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'volleyball.html', context)

def timer(request):
    return render(request, 'timer.html')

@login_required(login_url='/login')
def volleyball_bracket(request):
    school_years = SchoolYear.objects.all().order_by('-start_year')
    selected_year_id = request.GET.get('school_year')
    
    if selected_year_id:
        players = VolleyballTeam.objects.filter(yearID=selected_year_id)
    else:
        players = VolleyballTeam.objects.all()
    
    context = {
        'school_years': school_years,
        'players': players,
        'selected_year_id': selected_year_id,  # Keep track of the selected school year
        'username': request.user,
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'volleyball_bracket.html', context)

def bracket_list2(request):
    school_year_id = request.GET.get('school_year')
    if school_year_id:
        players = list(VolleyballTeam.objects.filter(yearID=school_year_id).values('teamID', 'team_name'))
    else:
        players = list(VolleyballTeam.objects.all().values('teamID', 'team_name'))
    return JsonResponse({'players': players})

@login_required(login_url='/login')
def tennis_bracket(request):
    school_years = SchoolYear.objects.all().order_by('-start_year')
    selected_year_id = request.GET.get('school_year')
    
    if selected_year_id:
        players = TennisPlayers.objects.filter(yearID=selected_year_id)
    else:
        players = TennisPlayers.objects.all()
    
    context = {
        'school_years': school_years,
        'players': players,
        'selected_year_id': selected_year_id,  # Keep track of the selected school year
        'username': request.user,
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'tennis_bracket.html', context)

def bracket_list3(request):
    school_year_id = request.GET.get('school_year')
    if school_year_id:
        players = list(TennisPlayers.objects.filter(yearID=school_year_id).values('playerID', 'player_name'))
    else:
        players = list(TennisPlayers.objects.all().values('playerID', 'player_name'))
    return JsonResponse({'players': players})

@login_required(login_url='/login')
def volleyball_scoreboard(request):
    school_years = SchoolYear.objects.all()
    selected_year_id = request.GET.get('school_year')    
    selected_team_id1 = request.GET.get('team-selection1')
    selected_team_id2 = request.GET.get('team-selection2')

    home_teams = []
    away_teams = []
    home_team = []
    away_team = []

    if selected_year_id:
        selected_year = get_object_or_404(SchoolYear, YearID=selected_year_id)
        home_teams = VolleyballTeam.objects.filter(yearID=selected_year)
        away_teams = VolleyballTeam.objects.filter(yearID=selected_year)
    
    if selected_team_id1:
        home_team = get_object_or_404(VolleyballTeam, teamID=selected_team_id1)
        players1 = VolleyballPlayer.objects.filter(teamID=home_team)
    
    if selected_team_id2:
        away_team = get_object_or_404(VolleyballTeam, teamID=selected_team_id2)
        players2 = VolleyballPlayer.objects.filter(teamID=away_team)

    context = {
        'school_years': school_years,
        'selected_year_id': selected_year_id,
        'selected_team_id1': selected_team_id1,
        'selected_team_id2': selected_team_id2,
        'home_team': home_team,
        'away_team': away_team,
        'home_teams': home_teams,
        'away_teams': away_teams,
        'players1': players1 if home_team else [],  # Return empty list if home_team is None
        'players2': players2 if away_team else [],  # Return empty list if away_team is None
        'username': request.user,
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'volleyball_scoreboard.html', context)

@login_required(login_url='/login')
def add_team(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')  # Capture the year ID from GET
    teams_from_previous_year = []

    # If a previous school year is selected, fetch its teams
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        teams_from_previous_year = VolleyballTeam.objects.filter(yearID=previous_school_year)
    
    colleges = College.objects.all()  # Fetch all colleges to display in the dropdown

    if request.method == 'POST':
        selected_team_ids = request.POST.getlist('selected_teams')  # Use 'selected_teams' to match the HTML
        for team_id in selected_team_ids:
            team = get_object_or_404(VolleyballTeam, pk=team_id)
            VolleyballTeam.objects.create(
                team_name=team.team_name,
                collegeID=team.collegeID,                   
                yearID=school_year
            )
            

        # Process new team if entered
        new_team_name = request.POST.get('new_team_name')
        new_college_id = request.POST.get('new_college_id')  # Get the selected college ID

        if new_team_name and new_college_id:
            college = get_object_or_404(College, pk=new_college_id)  # Fetch the selected college
            VolleyballTeam.objects.create(
                team_name=new_team_name,
                collegeID=college,  # Associate the college with the new team
                yearID=school_year
            )

        messages.success(request, "New volleyball team has been successfully added.")
        return redirect('myapp:volleyball_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'is_admin' : is_admin,
        'all_school_years': all_school_years,
        'teams_from_previous_year': teams_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
        'colleges': colleges,  # Pass all colleges to the template
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    
    return render(request, 'add-team.html', context)

@login_required(login_url='/login')
def edit_team(request, team_id):
    team = get_object_or_404(VolleyballTeam, teamID=team_id)
    if request.method == 'POST':
        form = VolleyballTeams(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballTeams(instance=team)

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-team.html', {'form': form})

@login_required(login_url='/login')
def view_players(request, team_id):
    team = VolleyballTeam.objects.get(teamID=team_id)
    players = VolleyballPlayer.objects.filter(teamID=team_id)

    context = {
        'team': team,
        'players': players,
        'username': request.user,
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'volleyball_players.html', context)

@login_required(login_url='/login')
def add_volleyball_player(request, team_id):
    team = get_object_or_404(VolleyballTeam, pk=team_id)
    if request.method == 'POST':
        form = VolleyballPlayers(request.POST)
        if form.is_valid():
            volleyball_player = form.save(commit=False) 
            volleyball_player.teamID = team 
            volleyball_player.save() 
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballPlayers()

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'add-volley-player.html', {'form': form})

@login_required(login_url='/login')
def edit_volleyball_player(request, player_id):
    player = get_object_or_404(VolleyballPlayer, playerID=player_id)
    if request.method == 'POST':
        form = VolleyballPlayers(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballPlayers(instance=player)
    
    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-volley-player.html', {'form': form})

@login_required(login_url='/login')
def add_volleyball_judge(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin  # Check if the user is an admin

    selected_year_id = request.GET.get('previous_year')
    judges_from_previous_year = []

    # If a previous school year is selected, fetch its judges
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        judges_from_previous_year = VolleyballJudge.objects.filter(yearID=previous_school_year)


    if request.method == 'POST':
        # Process selected judges from the previous year
        selected_judge_ids = request.POST.getlist('selected_judges')
        for judge_id in selected_judge_ids:
            judge = get_object_or_404(VolleyballJudge, pk=judge_id)
            VolleyballJudge.objects.create(
                judge_name=judge.judge_name,
                yearID=school_year
            )

        # Process new judge if entered
        new_judge_name = request.POST.get('new_judge_name')

        if new_judge_name:
            VolleyballJudge.objects.create(
                judge_name=new_judge_name,
                yearID=school_year,
            )

        messages.success(request, "Judges have been successfully added.")
        return redirect('myapp:volleyball_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'all_school_years': all_school_years,
        'judges_from_previous_year': judges_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
        'is_admin': is_admin,
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'add-volley-judge.html', context)

@login_required(login_url='/login')
def edit_volleyball_judge(request, judge_id):
    judge = get_object_or_404(VolleyballJudge, judgeID=judge_id)
    if request.method == 'POST':
        form = VolleyballJudge(request.POST, instance=judge)
        if form.is_valid():
            form.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballJudge(instance=judge)

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-volley-judge.html', {'form': form})

@login_required(login_url='/login')
def add_volleyball_referee(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')
    referees_from_previous_year = []

    # If a previous school year is selected, fetch its referees
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        referees_from_previous_year = VolleyballReferee.objects.filter(yearID=previous_school_year)

    if request.method == 'POST':
        # Process selected referees from the previous year
        selected_referee_ids = request.POST.getlist('selected_referees')
        for referee_id in selected_referee_ids:
            referee = get_object_or_404(VolleyballReferee, pk=referee_id)
            VolleyballReferee.objects.create(
                referee_name=referee.referee_name,
                yearID=school_year
            )

        # Process new referee if entered
        new_referee_name = request.POST.get('new_referee_name')

        if new_referee_name:
            VolleyballReferee.objects.create(
                referee_name=new_referee_name,
                yearID=school_year,
            )

        messages.success(request, "Referees have been successfully added.")
        return redirect('myapp:volleyball_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'all_school_years': all_school_years,
        'is_admin' : is_admin,
        'referees_from_previous_year': referees_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'add-volley-referee.html', context)

@login_required(login_url='/login')
def edit_volleyball_referee(request, referee_id):
    referee = get_object_or_404(VolleyballReferee, refereeID=referee_id)
    if request.method == 'POST':
        form = VolleyballReferees(request.POST, instance=referee)
        if form.is_valid():
            form.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballReferees(instance=referee)

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-volley-referee.html', {'form': form})

@login_required(login_url='/login')
def add_volleyball_scorer(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')
    scorers_from_previous_year = []

    # If a previous school year is selected, fetch its referees
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        scorers_from_previous_year = VolleyballScorer.objects.filter(yearID=previous_school_year)

    if request.method == 'POST':
        # Process selected referees from the previous year
        selected_scorer_ids = request.POST.getlist('selected_scorers')
        for scorer_id in selected_scorer_ids:
            scorer = get_object_or_404(VolleyballScorer, pk=scorer_id)
            VolleyballScorer.objects.create(
                scorer_name=scorer.scorer_name,
                yearID=school_year
            )

        # Process new referee if entered
        new_scorer_name = request.POST.get('new_scorer_name')

        if new_scorer_name:
            VolleyballScorer.objects.create(
                scorer_name=new_scorer_name,
                yearID=school_year,
            )

        messages.success(request, "Scorers have been successfully added.")
        return redirect('myapp:volleyball_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'all_school_years': all_school_years,
        'is_admin' : is_admin,
        'scorers_from_previous_year': scorers_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'add-volley-scorer.html', context)

@login_required(login_url='/login')
def edit_volleyball_scorer(request, scorer_id):
    scorer = get_object_or_404(VolleyballScorer, scorerID=scorer_id)
    if request.method == 'POST':
        form = VolleyballScorers(request.POST, instance=scorer)
        if form.is_valid():
            form.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballScorers(instance=scorer)

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-volley-scorer.html', {'form': form})

@login_required(login_url='/login')
def add_tennis_player(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')  # Changed to GET to capture the year ID
    players_from_previous_year = []

    # If a previous school year is selected, fetch its players
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        players_from_previous_year = TennisPlayers.objects.filter(yearID=previous_school_year)

    colleges = College.objects.all()  # Fetch all colleges

    if request.method == 'POST':
        # Process selected players from the previous year
        selected_player_ids = request.POST.getlist('selected_players')
        for player_id in selected_player_ids:
            player = get_object_or_404(TennisPlayers, pk=player_id)
            TennisPlayers.objects.create(
                player_name=player.player_name,
                collegeID=player.collegeID,
                yearID=school_year
            )

        # Process new player if entered
        new_player_name = request.POST.get('new_player_name')
        new_college_id = request.POST.get('new_college_id')

        if new_player_name and new_college_id:
            college = get_object_or_404(College, pk=new_college_id)
            TennisPlayers.objects.create(
                player_name=new_player_name,
                collegeID=college,  # Add college_id to player creation
                yearID=school_year
            )

        messages.success(request, "Player has been successfully added.")
        return redirect('myapp:tennis_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'is_admin' : is_admin,
        'all_school_years': all_school_years,
        'players_from_previous_year': players_from_previous_year,
        'colleges': colleges,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'add-tennis-player.html', context)


@login_required(login_url='/login')
def edit_tennis_player(request, player_id):
    player = get_object_or_404(TennisPlayers, playerID=player_id)
    if request.method == 'POST':
        form = TennisPlayersForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('myapp:tennis_sport_data')
    else:
        form = TennisPlayersForm(instance=player)

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-tennis-player.html', {'form': form})

@login_required(login_url='/login')
def add_tennis_umpire(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')  # Use GET to fetch selected year
    umpires_from_previous_year = []

    # If a previous school year is selected, fetch its coaches
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        umpires_from_previous_year = TennisUmpire.objects.filter(yearID=previous_school_year)

    if request.method == 'POST':
        # Process selected coaches from the previous year
        selected_umpire_ids = request.POST.getlist('selected_umpires')
        for umpire_id in selected_umpire_ids:
            umpire = get_object_or_404(TennisUmpire, pk=umpire_id)
            TennisUmpire.objects.create(
                umpire_name=umpire.umpire_name,
                yearID=school_year
            )

        # Process new coach if entered
        new_umpire_name = request.POST.get('new_umpire_name')

        if new_umpire_name:
            TennisUmpire.objects.create(
                umpire_name=new_umpire_name,
                yearID=school_year,
            )

        messages.success(request, "Umpire have been successfully added.")
        return redirect('myapp:tennis_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'is_admin' : is_admin,
        'all_school_years': all_school_years,
        'umpires_from_previous_year': umpires_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }
    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'add-tennis-umpire.html', context)

@login_required(login_url='/login')
def edit_tennis_umpire(request, umpire_id):
    umpire = get_object_or_404(TennisUmpire, umpireID=umpire_id)
    if request.method == 'POST':
        form = TennisUmpires(request.POST, instance=umpire)
        if form.is_valid():
            form.save()
            return redirect('myapp:tennis_sport_data')
    else:
        form = TennisUmpires(instance=umpire)

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-tennis-umpire.html', {'form': form})

@login_required(login_url='/login')
def add_tennis_coach(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    all_school_years = SchoolYear.objects.exclude(pk=year_id)  # Exclude current school year

    is_admin = request.user.is_admin

    selected_year_id = request.GET.get('previous_year')  # Use GET to fetch selected year
    coaches_from_previous_year = []

    # If a previous school year is selected, fetch its coaches
    if selected_year_id:
        previous_school_year = get_object_or_404(SchoolYear, pk=selected_year_id)
        coaches_from_previous_year = TennisCoach.objects.filter(yearID=previous_school_year)

    if request.method == 'POST':
        # Process selected coaches from the previous year
        selected_coach_ids = request.POST.getlist('selected_coaches')
        for coach_id in selected_coach_ids:
            coach = get_object_or_404(TennisCoach, pk=coach_id)
            TennisCoach.objects.create(
                coach_name=coach.coach_name,
                yearID=school_year
            )

        # Process new coach if entered
        new_coach_name = request.POST.get('new_coach_name')

        if new_coach_name:
            TennisCoach.objects.create(
                coach_name=new_coach_name,
                yearID=school_year,
            )

        messages.success(request, "Coaches have been successfully added.")
        return redirect('myapp:tennis_sport_data')  # Redirect to the appropriate page

    context = {
        'school_year': school_year,
        'is_admin' : is_admin,
        'all_school_years': all_school_years,
        'coaches_from_previous_year': coaches_from_previous_year,
        'selected_year_id': selected_year_id,  # Pass the selected year ID to the template
    }
    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page

    return render(request, 'add-tennis-coach.html', context)


@login_required(login_url='/login')
def edit_tennis_coach(request, coach_id):
    coach = get_object_or_404(TennisCoach, coachID=coach_id)
    if request.method == 'POST':
        form = TennisCoaches(request.POST, instance=coach)
        if form.is_valid():
            form.save()
            return redirect('myapp:tennis_sport_data')
    else:
        form = TennisCoaches(instance=coach)

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'edit-tennis-coach.html', {'form': form})

@login_required(login_url='/login')
def arnis_history(request):
    matches = LabananMatch.objects.all()
    forms = FormMatch.objects.all()
    winners = FormPlayers.objects.filter(rank=1)


    context ={
    'matches': matches,
    'forms': forms,
    'winners': winners,  # Pass rank 1 players to the template
    'username': request.user,
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'arnis_history.html', context)

@login_required(login_url='/login')
def labanan_match_view(request, match_id):
    match = get_object_or_404(LabananMatch, matchID=match_id)
    
    # Get round 1 for the match
    round_1 = get_object_or_404(LabananRound, round_num=1, matchID=match)
    round_2 = get_object_or_404(LabananRound, round_num=2, matchID=match)
    round_3 = get_object_or_404(LabananRound, round_num=3, matchID=match)

    # Get all scores in round 1
    score1 = LabananScore.objects.filter(roundID=round_1)
    score2 = LabananScore.objects.filter(roundID=round_2)
    score3 = LabananScore.objects.filter(roundID=round_3)

    first_player1 = score1.first()  # This gets the first player's score
    second_player1 = score1[1] if score1.count() > 1 else None  # This gets the second player's score, if available

    first_player2 = score2.first()  # This gets the first player's score
    second_player2 = score2[1] if score2.count() > 1 else None  # This gets the second player's score, if available

    first_player3 = score3.first()  # This gets the first player's score
    second_player3 = score3[1] if score3.count() > 1 else None  # This gets the second player's score, if available

    context = {
        'match': match,
        'round1': round_1,
        'round2': round_2,
        'round3': round_3,
        'first_player1': first_player1,
        'second_player1': second_player1,
        'first_player2': first_player2,
        'second_player2': second_player2,
        'first_player3': first_player3,
        'second_player3': second_player3,
        'username': request.user,
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'labanan_match_view.html', context)

@login_required(login_url='/login')
def anyo_match_view(request, form_id):
    form = get_object_or_404(FormMatch, formID=form_id)
    
    players = FormPlayers.objects.filter(formID=form)

    context = {
        'form': form,
        'players': players,
        'username': request.user,
    }

    if request.user.sport != 'arnis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'anyo_match_view.html', context)

@login_required(login_url='/login')
def tennis_history(request):
    singles = SingleTennisMatch.objects.all()
    doubles = DoubleTennisMatch.objects.all()
    
    context ={
    'singles': singles,
    'doubles': doubles,
    'username': request.user,
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'tennis_history.html', context)

@login_required(login_url='/login')
def single_match_view(request, match_id):
    game = get_object_or_404(SingleTennisMatch, matchID=match_id)
    
    # Get round 1 for the match
    set_1 = get_object_or_404(SingleTennisSet, set_no=1, matchID=game)
    set_2 = get_object_or_404(SingleTennisSet, set_no=2, matchID=game)
    set_3 = get_object_or_404(SingleTennisSet, set_no=3, matchID=game)
    set_4 = get_object_or_404(SingleTennisSet, set_no=4, matchID=game)
    set_5 = get_object_or_404(SingleTennisSet, set_no=5, matchID=game)


    # Get all scores in round 1
    score1 = SingleTennisScore.objects.filter(setID=set_1)
    score2 = SingleTennisScore.objects.filter(setID=set_2)
    score3 = SingleTennisScore.objects.filter(setID=set_3)
    score4 = SingleTennisScore.objects.filter(setID=set_4)
    score5 = SingleTennisScore.objects.filter(setID=set_5)


    first_player1 = score1.first()  # This gets the first player's score
    second_player1 = score1[1] if score1.count() > 1 else None  # This gets the second player's score, if available

    first_player2 = score2.first()  # This gets the first player's score
    second_player2 = score2[1] if score2.count() > 1 else None  # This gets the second player's score, if available

    first_player3 = score3.first()  # This gets the first player's score
    second_player3 = score3[1] if score3.count() > 1 else None  # This gets the second player's score, if available

    first_player4 = score4.first()  # This gets the first player's score
    second_player4 = score4[1] if score4.count() > 1 else None  # This gets the second player's score, if available

    first_player5 = score5.first()  # This gets the first player's score
    second_player5 = score5[1] if score5.count() > 1 else None  # This gets the second player's score, if available
   
    context = {
        'game': game,
        'set1': set_1,
        'set2': set_2,
        'set3': set_3,
        'set4': set_4,
        'set5': set_5,
        'first_player1': first_player1,
        'second_player1': second_player1,
        'first_player2': first_player2,
        'second_player2': second_player2,
        'first_player3': first_player3,
        'second_player3': second_player3,
        'first_player4': first_player4,
        'second_player4': second_player4,
        'first_player5': first_player5,
        'second_player5': second_player5,
        'username': request.user,
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'stennis_match_view.html', context)

@login_required(login_url='/login')
def double_match_view(request, match_id):
    game = get_object_or_404(DoubleTennisMatch, matchID=match_id)
    
    # Get round 1 for the match
    set_1 = get_object_or_404(DoubleTennisSet, set_no=1, matchID=game)
    set_2 = get_object_or_404(DoubleTennisSet, set_no=2, matchID=game)
    set_3 = get_object_or_404(DoubleTennisSet, set_no=3, matchID=game)
    set_4 = get_object_or_404(DoubleTennisSet, set_no=4, matchID=game)
    set_5 = get_object_or_404(DoubleTennisSet, set_no=5, matchID=game)


    # Get all scores in round 1
    score1 = DoubleTennisScore.objects.filter(setID=set_1)
    score2 = DoubleTennisScore.objects.filter(setID=set_2)
    score3 = DoubleTennisScore.objects.filter(setID=set_3)
    score4 = DoubleTennisScore.objects.filter(setID=set_4)
    score5 = DoubleTennisScore.objects.filter(setID=set_5)


    first_player1 = score1.first()  # This gets the first player's score
    second_player1 = score1[1] if score1.count() > 1 else None  # This gets the second player's score, if available

    first_player2 = score2.first()  # This gets the first player's score
    second_player2 = score2[1] if score2.count() > 1 else None  # This gets the second player's score, if available

    first_player3 = score3.first()  # This gets the first player's score
    second_player3 = score3[1] if score3.count() > 1 else None  # This gets the second player's score, if available

    first_player4 = score4.first()  # This gets the first player's score
    second_player4 = score4[1] if score4.count() > 1 else None  # This gets the second player's score, if available

    first_player5 = score5.first()  # This gets the first player's score
    second_player5 = score5[1] if score5.count() > 1 else None  # This gets the second player's score, if available
   
    context = {
        'game': game,
        'set1': set_1,
        'set2': set_2,
        'set3': set_3,
        'set4': set_4,
        'set5': set_5,
        'first_player1': first_player1,
        'second_player1': second_player1,
        'first_player2': first_player2,
        'second_player2': second_player2,
        'first_player3': first_player3,
        'second_player3': second_player3,
        'first_player4': first_player4,
        'second_player4': second_player4,
        'first_player5': first_player5,
        'second_player5': second_player5,
        'username': request.user,
    }

    if request.user.sport != 'table_tennis' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'dtennis_match_view.html', context)

@login_required(login_url='/login')
def volleyball_history(request):
    volley = VolleyballMatch.objects.all()
    
    context ={
    'volley': volley,
    'username': request.user,
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'volleyball_history.html', context)

@login_required(login_url='/login')
def volleyball_match_view(request, match_id):
    match = get_object_or_404(VolleyballMatch, matchID=match_id)
    
    # Get round 1 for the match
    set_1 = get_object_or_404(VolleyballSet, set_no=1, matchID=match)
    set_2 = get_object_or_404(VolleyballSet, set_no=2, matchID=match)
    set_3 = get_object_or_404(VolleyballSet, set_no=3, matchID=match)
   

    # Get all scores in round 1
    score1 = VolleyballScore.objects.filter(setID=set_1)
    score2 = VolleyballScore.objects.filter(setID=set_2)
    score3 = VolleyballScore.objects.filter(setID=set_3)

    first_player1 = score1.first()  # This gets the first player's score
    second_player1 = score1[1] if score1.count() > 1 else None  # This gets the second player's score, if available

    first_player2 = score2.first()  # This gets the first player's score
    second_player2 = score2[1] if score2.count() > 1 else None  # This gets the second player's score, if available

    first_player3 = score3.first()  # This gets the first player's score
    second_player3 = score3[1] if score3.count() > 1 else None  # This gets the second player's score, if available
   
    context = {
        'match': match,
        'set1': set_1,
        'set2': set_2,
        'set3': set_3,
        'first_player1': first_player1,
        'second_player1': second_player1,
        'first_player2': first_player2,
        'second_player2': second_player2,
        'first_player3': first_player3,
        'second_player3': second_player3,
        'username': request.user,
    }

    if request.user.sport != 'volleyball' and not request.user.is_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('myapp:sports')  # Redirect to sport selection page
    return render(request, 'volleyball_match_view.html', context)

@admin_required   
def admin_school_year(request):
    # Fetch all school years
    school_years = SchoolYear.objects.all()

    # Count total school years, users, and colleges
    total_school_years = school_years.count()
    total_users = CustomUser.objects.count()  # Assuming you have a User model
    total_colleges = College.objects.count()  # Assuming you have a College model

    # Prepare context
    context = {
        'school_years': school_years,
        'total_school_years': total_school_years,
        'total_users': total_users,
        'total_colleges': total_colleges,
        'username': request.user,
    }

    return render(request, 'admin/admin_data.html', context)

def admin_analytics_view(request, year_id):
    # Fetch the selected school year
    school_year = get_object_or_404(SchoolYear, YearID=year_id)
    
    # Count the players and teams based on the selected school year
    total_labanan_players = ArnisLabananPlayers.objects.filter(yearID=school_year).count()
    total_form_teams = ArnisFormPlayers.objects.filter(yearID=school_year).count()
    total_volleyball_teams = VolleyballTeam.objects.filter(yearID=school_year).count()
    total_tennis_players = TennisPlayers.objects.filter(yearID=school_year).count()

    # Count judges, referees, and other roles
    total_arnis_judges = ArnisJudge.objects.filter(yearID=school_year).count()
    total_arnis_recorders = ArnisRecorder.objects.filter(yearID=school_year).count()
    total_arnis_referees = ArnisReferee.objects.filter(yearID=school_year).count()
    total_arnis_tabulators = ArnisTabulator.objects.filter(yearID=school_year).count()
    total_arnis_timers = ArnisTimer.objects.filter(yearID=school_year).count()
    
    total_volleyball_judges = VolleyballJudge.objects.filter(yearID=school_year).count()
    total_volleyball_referees = VolleyballReferee.objects.filter(yearID=school_year).count()
    total_volleyball_scorers = VolleyballScorer.objects.filter(yearID=school_year).count()
    
    total_tennis_coaches = TennisCoach.objects.filter(yearID=school_year).count()
    total_tennis_umpires = TennisUmpire.objects.filter(yearID=school_year).count()

    # Count matches
    total_double_tennis_matches = DoubleTennisMatch.objects.filter(yearID=school_year).count()
    total_single_tennis_matches = SingleTennisMatch.objects.filter(yearID=school_year).count()
    total_labanan_matches = LabananMatch.objects.filter(yearID=school_year).count()
    total_form_matches = FormMatch.objects.filter(yearID=school_year).count()
    total_volleyball_matches = VolleyballMatch.objects.filter(yearID=school_year).count()

    # Calculate total players for percentage calculations
    total_players = total_labanan_players + total_form_teams + total_volleyball_teams + total_tennis_players

    # Calculate percentages (avoid division by zero)
    total_labanan_players_percentage = (total_labanan_players / total_players * 100) if total_players > 0 else 0
    total_form_players_percentage = (total_form_teams / total_players * 100) if total_players > 0 else 0
    total_tennis_players_percentage = (total_tennis_players / total_players * 100) if total_players > 0 else 0
    total_volleyball_teams_percentage = (total_volleyball_teams / total_players * 100) if total_players > 0 else 0

    # Prepare the context for rendering
    context = {
        'school_year': school_year,
        'total_labanan_players': total_labanan_players,
        'total_form_teams': total_form_teams,
        'total_tennis_players': total_tennis_players,
        'total_volleyball_teams': total_volleyball_teams,
        'total_labanan_players_percentage': total_labanan_players_percentage,
        'total_form_players_percentage': total_form_players_percentage,
        'total_tennis_players_percentage': total_tennis_players_percentage,
        'total_volleyball_teams_percentage': total_volleyball_teams_percentage,
        
        # Add counts for roles
        'total_arnis_judges': total_arnis_judges,
        'total_arnis_recorders': total_arnis_recorders,
        'total_arnis_referees': total_arnis_referees,
        'total_arnis_tabulators': total_arnis_tabulators,
        'total_arnis_timers': total_arnis_timers,
        'total_volleyball_judges': total_volleyball_judges,
        'total_volleyball_referees': total_volleyball_referees,
        'total_volleyball_scorers': total_volleyball_scorers,
        'total_tennis_coaches': total_tennis_coaches,
        'total_tennis_umpires': total_tennis_umpires,

        # Add counts for matches
        'total_double_tennis_matches': total_double_tennis_matches,
        'total_single_tennis_matches': total_single_tennis_matches,
        'total_labanan_matches': total_labanan_matches,
        'total_form_matches': total_form_matches,
        'total_volleyball_matches': total_volleyball_matches,
        'username': request.user,
    }

    return render(request, 'admin/admin_analytics.html', context)

@admin_required
def admin_user_management_view(request):
    users = CustomUser.objects.all()  # Fetch all users

    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('userID')

        if action == 'delete' and user_id:
            user = get_object_or_404(CustomUser, userID=user_id)
            user.delete()
            messages.success(request, f'User {user.username} deleted successfully.')

    context = {
        'users': users,
        'username': request.user,
    }
    return render(request, 'admin/admin_users.html', context)

@admin_required
def admin_add_user_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'User {user.username} added successfully.')
            return redirect('myapp:admin_users')

    else:
        form = CustomUserForm()

    context = {
        'form': form
        }
    return render(request, 'admin/admin_user_add.html', context)

@admin_required
def admin_edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, userID=user_id)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'User {user.username} updated successfully.')
            return redirect('myapp:admin_users')

    else:
        form = CustomUserForm(instance=user)

    context = {'form': form, 'user': user}
    return render(request, 'admin/admin_user_edit.html', context)

def admin_delete_user_view(request, user_id):
    user = get_object_or_404(CustomUser, userID=user_id)
    user.delete()
    messages.success(request, f'User {user.username} deleted successfully.')
    return redirect('myapp:admin_users')

@admin_required
def admin_view_user_view(request, user_id):
    user = get_object_or_404(CustomUser, userID=user_id)
    context = {'user': user}
    return render(request, 'admin/admin_user_view.html', context)

@admin_required
def admin_other_data(request):
    school_years = SchoolYear.objects.all().order_by('-start_year')
    colleges = College.objects.all()

    context = {
        'school_years': school_years,
        'colleges': colleges,
        'username': request.user,
    }
    return render(request, 'admin/admin_other_data.html', context)

def delete_school_year(request, year_id):
    school_year = get_object_or_404(SchoolYear, YearID=year_id)
    school_year.delete()
    messages.success(request, "School Year deleted successfully!")
    return redirect('myapp:admin_other_data')

def delete_college(request, college_id):
    college = get_object_or_404(College, collegeID=college_id)
    college.delete()
    messages.success(request, "College deleted successfully!")
    return redirect('myapp:admin_other_data')

def delete_arnis_form_player(request, player_id):
    form_player = get_object_or_404(ArnisFormPlayers, playerID=player_id)
    form_player.delete()
    messages.success(request, "Player successfully deleted.")
    return redirect('myapp:arnis_sport_data')

def delete_arnis_labanan_player(request, player_id):
    labanan_player = get_object_or_404(ArnisLabananPlayers, playerID=player_id)
    labanan_player.delete()
    messages.success(request, "Player successfully deleted.")
    return redirect('myapp:arnis_sport_data')

def delete_manager(request, manager_id):
    manager = get_object_or_404(ArnisManager, managerID=manager_id)
    manager.delete()
    messages.success(request, "Manager successfully deleted.")
    return redirect('myapp:arnis_sport_data')

def delete_referee(request, referee_id):
    referee = get_object_or_404(ArnisReferee, refereeID=referee_id)
    referee.delete()
    messages.success(request, "Referee successfully deleted.")
    return redirect('myapp:arnis_sport_data')

def delete_judge(request, judge_id):
    judge = get_object_or_404(ArnisJudge, judgeID=judge_id)
    judge.delete()
    messages.success(request, "Judge successfully deleted.")
    return redirect('myapp:arnis_sport_data')

def delete_recorder(request, recorder_id):
    recorder = get_object_or_404(ArnisRecorder, recorderID=recorder_id)
    recorder.delete()
    messages.success(request, "Recorder successfully deleted.")
    return redirect('myapp:arnis_sport_data')

def delete_tabulator(request, tabulator_id):
    tabulator = get_object_or_404(ArnisTabulator, tabulatorID=tabulator_id)
    tabulator.delete()
    messages.success(request, "Tabulator successfully deleted.")
    return redirect('myapp:arnis_sport_data')

def delete_timer(request, timer_id):
    timer = get_object_or_404(ArnisLabananPlayers, timerID=timer_id)
    timer.delete()
    messages.success(request, "Timer successfully deleted.")
    return redirect('myapp:arnis_sport_data')

def delete_tennis_player(request, player_id):
    tennis_player = get_object_or_404(TennisPlayers, playerID=player_id)
    tennis_player.delete()
    messages.success(request, "Player successfully deleted.")
    return redirect('myapp:tennis_sport_data')

def delete_coach(request, coach_id):
    coach = get_object_or_404(TennisCoach, coachID=coach_id)
    coach.delete()
    messages.success(request, "Coach successfully deleted.")
    return redirect('myapp:tennis_sport_data')

def delete_umpire(request, umpire_id):
    umpire = get_object_or_404(TennisUmpire, umpireID=umpire_id)
    umpire.delete()
    messages.success(request, "Umpire successfully deleted.")
    return redirect('myapp:tennis_sport_data')

def delete_team(request, team_id):
    team = get_object_or_404(VolleyballTeam, teamID=team_id)
    team.delete()
    messages.success(request, "Team successfully deleted.")
    return redirect('myapp:volleyball_sport_data')

def delete_volley_judge(request, judge_id):
    judge = get_object_or_404(VolleyballJudge, judgeID=judge_id)
    judge.delete()
    messages.success(request, "Judge successfully deleted.")
    return redirect('myapp:volleyball_sport_data')

def delete_volley_referee(request, referee_id):
    referee = get_object_or_404(VolleyballReferee, refereeID=referee_id)
    referee.delete()
    messages.success(request, "Referee successfully deleted.")
    return redirect('myapp:volleyball_sport_data')

def delete_volley_scorer(request, scorer_id):
    scorer = get_object_or_404(VolleyballScorer, scorerID=scorer_id)
    scorer.delete()
    messages.success(request, "Scorer successfully deleted.")
    return redirect('myapp:volleyball_sport_data')

def delete_volley_player(request, player_id):
    volleyball_player = get_object_or_404(VolleyballPlayer, playerID=player_id)
    volleyball_player.delete()
    messages.success(request, "Player successfully deleted.")
    return redirect('myapp:volleyball_sport_data')
    