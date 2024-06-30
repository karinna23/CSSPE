from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from .forms import *

# Models
from account.models import Account, CustomUser
from .models import *

from django.contrib.auth.decorators import login_required
from django.contrib import auth

def landing(request):      
    return render(request, 'landing.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            auth.login(request, user)

            if request.user.is_superuser == False:
                return redirect('/sports')

            else:
                return redirect('/admin_mode/referees')

        
        else:
            error_messages = 'Invalid email or password'

        return render(request, 'coach_login.html', {'error_messages': error_messages})
    
    return render(request, 'referee_login.html')

@login_required
def sports(request):
    user = request.user

    return render(request, 'sports.html', {'user': user})

def add_form_player(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = ArnisPlayersForm(request.POST)
        if form.is_valid():
            arnis_form_player = form.save(commit=False) 
            arnis_form_player.yearID = school_year 
            arnis_form_player.save() 
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisPlayersForm()
    return render(request, 'add-arnis-player.html', {'form': form})

def add_labanan_player(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = ArnisPlayersLabanan(request.POST)
        if form.is_valid():
            arnis_labanan_player = form.save(commit=False) 
            arnis_labanan_player.yearID = school_year 
            arnis_labanan_player.save() 
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisPlayersLabanan()
    return render(request, 'add-arnis-player.html', {'form': form})

def edit_form_player(request, player_id):
    player = get_object_or_404(ArnisFormPlayers, playerID=player_id)
    if request.method == 'POST':
        form = ArnisPlayersForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisPlayersForm(instance=player)
    return render(request, 'edit-arnis-player.html', {'form': form})

def edit_labanan_player(request, player_id):
    player = get_object_or_404(ArnisLabananPlayers, playerID=player_id)
    if request.method == 'POST':
        form = ArnisPlayersLabanan(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisPlayersLabanan(instance=player)
    return render(request, 'edit-arnis-player.html', {'form': form})

def add_referee(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = ArnisReferees(request.POST)
        if form.is_valid():
            arnis_referee = form.save(commit=False) 
            arnis_referee.yearID = school_year 
            arnis_referee.save() 
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisReferees()
    return render(request, 'add-referee.html', {'form': form})

def edit_referee(request, referee_id):
    referee = get_object_or_404(ArnisReferee, refereeID=referee_id)
    if request.method == 'POST':
        form = ArnisReferees(request.POST, instance=referee)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisReferees(instance=referee)
    return render(request, 'edit-referee.html', {'form': form})\
    
def add_judge(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = ArnisJudges(request.POST)
        if form.is_valid():
            arnis_judge = form.save(commit=False) 
            arnis_judge.yearID = school_year 
            arnis_judge.save() 
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisJudges()
    return render(request, 'add-judge.html', {'form': form})

def edit_judge(request, judge_id):
    judge = get_object_or_404(ArnisJudge, judgeID=judge_id)
    if request.method == 'POST':
        form = ArnisJudges(request.POST, instance=judge)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisJudges(instance=judge)
    return render(request, 'edit-judge.html', {'form': form})

def add_recorder(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = ArnisRecorders(request.POST)
        if form.is_valid():
            arnis_recorder = form.save(commit=False) 
            arnis_recorder.yearID = school_year 
            arnis_recorder.save() 
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisRecorders()
    return render(request, 'add-recorder.html', {'form': form})

def edit_recorder(request, recorder_id):
    recorder = get_object_or_404(ArnisRecorder, recorderID=recorder_id)
    if request.method == 'POST':
        form = ArnisRecorders(request.POST, instance=recorder)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisRecorders(instance=recorder)
    return render(request, 'edit-recorder.html', {'form': form})

def add_tabulator(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = ArnisTabulators(request.POST)
        if form.is_valid():
            arnis_tabulator = form.save(commit=False) 
            arnis_tabulator.yearID = school_year 
            arnis_tabulator.save() 
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisTabulators()
    return render(request, 'add-tabulator.html', {'form': form})

def edit_tabulator(request, tabulator_id):
    tabulator = get_object_or_404(ArnisTabulator, tabulatorID=tabulator_id)
    if request.method == 'POST':
        form = ArnisTabulators(request.POST, instance=tabulator)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisTabulators(instance=tabulator)
    return render(request, 'edit-tabulator.html', {'form': form})

def add_timer(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = ArnisTimers(request.POST)
        if form.is_valid():
            arnis_timer = form.save(commit=False) 
            arnis_timer.yearID = school_year 
            arnis_timer.save() 
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisTimers()
    return render(request, 'add-timer.html', {'form': form})

def edit_timer(request, timer_id):
    timer = get_object_or_404(ArnisTimer, timerID=timer_id)
    if request.method == 'POST':
        form = ArnisTimers(request.POST, instance=timer)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisTimers(instance=timer)
    return render(request, 'edit-timer.html', {'form': form})

def add_manager(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = ArnisManagers(request.POST)
        if form.is_valid():
            arnis_manager = form.save(commit=False) 
            arnis_manager.yearID = school_year 
            arnis_manager.save() 
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisManagers()
    return render(request, 'add-manager.html', {'form': form})

def edit_manager(request, manager_id):
    manager = get_object_or_404(ArnisManager, managerID=manager_id)
    if request.method == 'POST':
        form = ArnisManagers(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = ArnisManagers(instance=manager)
    return render(request, 'edit-manager.html', {'form': form})

def add_college(request):
    if request.method == 'POST':
        form = Colleges(request.POST)  # Assuming the form is named CollegeForm
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = Colleges()
    return render(request, 'add-college.html', {'form': form})


def edit_college(request, college_id):
    college = get_object_or_404(College, collegeID=college_id)
    if request.method == 'POST':
        form = Colleges(request.POST, instance=college)
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = Colleges(instance=college)
    return render(request, 'edit-college.html', {'form': form})

def add_school_year(request):
    if request.method == 'POST':
        form = SchoolYear(request.POST)  # Assuming the form is named CollegeForm
        if form.is_valid():
            form.save()
            return redirect('myapp:arnis_sport_data')
    else:
        form = SchoolYears()
    return render(request, 'add-year.html', {'form': form})

def arnis(request):
    return render(request, 'arnis.html')

def tennis(request):
    return render(request, 'table_tennis.html')

def dtennis_sheet(request):
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

    if request.method == 'POST':
        match_form = DoubleTennisMatchForm(request.POST)
        if match_form.is_valid():
            match = match_form.save(commit=False)
            match.yearID = school_year
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

            player1_name = request.POST.get('player1_name')
            player2_name = request.POST.get('player2_name')

            player1_score_1 = request.POST.get('player1_score1')
            player1_score_2 = request.POST.get('player1_score2')
            player1_score_3 = request.POST.get('player1_score3')
            player1_score_4 = request.POST.get('player1_score4')
            player1_score_5 = request.POST.get('player1_score5')
            player1_timeout = request.POST.get('player1_timeout')

            player2_score_1= request.POST.get('player2_score1')
            player2_score_2 = request.POST.get('player2_score2')
            player2_score_3 = request.POST.get('player2_score3')
            player2_score_4 = request.POST.get('player2_score4')
            player2_score_5 = request.POST.get('player2_score5')
            player2_timeout = request.POST.get('player2_timeout')

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
            player1_score1.timeout_used = player1_timeout
            player1_score1.save()

            player1_score2 = player1_score2_form.save(commit=False)
            player1_score2.setID = set2  # Pass the match instance to set1
            player1_score2.player = player1_name
            player1_score2.score = player1_score_2
            player1_score2.timeout_used = player1_timeout
            player1_score2.save()

            player1_score3 = player1_score3_form.save(commit=False)
            player1_score3.setID = set3  # Pass the match instance to set1
            player1_score3.player = player1_name
            player1_score3.score = player1_score_3
            player1_score3.timeout_used = player1_timeout
            player1_score3.save()

            player1_score4 = player1_score4_form.save(commit=False)
            player1_score4.setID = set4  # Pass the match instance to set1
            player1_score4.player = player1_name
            player1_score4.score = player1_score_4
            player1_score4.timeout_used = player1_timeout
            player1_score4.save()

            player1_score5 = player1_score5_form.save(commit=False)
            player1_score5.setID = set5  # Pass the match instance to set1
            player1_score5.player = player1_name
            player1_score5.score = player1_score_5
            player1_score5.timeout_used = player1_timeout
            player1_score5.save()

            player2_score1 = player2_score1_form.save(commit=False)
            player2_score1.setID = set1  # Pass the match instance to set1
            player2_score1.player = player2_name
            player2_score1.score = player2_score_1
            player2_score1.timeout_used = player2_timeout
            player2_score1.save()

            player2_score2 = player2_score2_form.save(commit=False)
            player2_score2.setID = set2  # Pass the match instance to set1
            player2_score2.player = player2_name
            player2_score2.score = player2_score_2
            player2_score2.timeout_used = player2_timeout
            player2_score2.save()

            player2_score3 = player2_score3_form.save(commit=False)
            player2_score3.setID = set3  # Pass the match instance to set1
            player2_score3.player = player2_name
            player2_score3.score = player2_score_3
            player2_score3.timeout_used = player2_timeout
            player2_score3.save()

            player2_score4 = player2_score4_form.save(commit=False)
            player2_score4.setID = set4  # Pass the match instance to set1
            player2_score4.player = player2_name
            player2_score4.score = player2_score_4
            player2_score4.timeout_used = player2_timeout
            player2_score4.save()

            player2_score5 = player2_score5_form.save(commit=False)
            player2_score5.setID = set5  # Pass the match instance to set1
            player2_score5.player = player2_name
            player2_score5.score = player2_score_5
            player2_score5.timeout_used = player2_timeout
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
        'school_years': school_years,
        'players' : players,
        'colleges': colleges,
        'coaches': coaches,
        'umpires': umpires,
        'selected_year_id': selected_year_id,
    }
    return render(request, 'dtennis_sheet.html', context)

def stennis_sheet(request):
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

    if request.method == 'POST':
        match_form = SingleTennisMatchForm(request.POST)
        if match_form.is_valid():
            match = match_form.save(commit=False)
            match.yearID = school_year
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

            player1_name = request.POST.get('player1_name')
            player2_name = request.POST.get('player2_name')

            player1_score_1 = request.POST.get('player1_score1')
            player1_score_2 = request.POST.get('player1_score2')
            player1_score_3 = request.POST.get('player1_score3')
            player1_score_4 = request.POST.get('player1_score4')
            player1_score_5 = request.POST.get('player1_score5')
            player1_timeout = request.POST.get('player1_timeout')

            player2_score_1= request.POST.get('player2_score1')
            player2_score_2 = request.POST.get('player2_score2')
            player2_score_3 = request.POST.get('player2_score3')
            player2_score_4 = request.POST.get('player2_score4')
            player2_score_5 = request.POST.get('player2_score5')
            player2_timeout = request.POST.get('player2_timeout')

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
            player1_score1.timeout_used = player1_timeout
            player1_score1.save()

            player1_score2 = player1_score2_form.save(commit=False)
            player1_score2.setID = set2  # Pass the match instance to set1
            player1_score2.player = player1_name
            player1_score2.score = player1_score_2
            player1_score2.timeout_used = player1_timeout
            player1_score2.save()

            player1_score3 = player1_score3_form.save(commit=False)
            player1_score3.setID = set3  # Pass the match instance to set1
            player1_score3.player = player1_name
            player1_score3.score = player1_score_3
            player1_score3.timeout_used = player1_timeout
            player1_score3.save()

            player1_score4 = player1_score4_form.save(commit=False)
            player1_score4.setID = set4  # Pass the match instance to set1
            player1_score4.player = player1_name
            player1_score4.score = player1_score_4
            player1_score4.timeout_used = player1_timeout
            player1_score4.save()

            player1_score5 = player1_score5_form.save(commit=False)
            player1_score5.setID = set5  # Pass the match instance to set1
            player1_score5.player = player1_name
            player1_score5.score = player1_score_5
            player1_score5.timeout_used = player1_timeout
            player1_score5.save()

            player2_score1 = player2_score1_form.save(commit=False)
            player2_score1.setID = set1  # Pass the match instance to set1
            player2_score1.player = player2_name
            player2_score1.score = player2_score_1
            player2_score1.timeout_used = player2_timeout
            player2_score1.save()

            player2_score2 = player2_score2_form.save(commit=False)
            player2_score2.setID = set2  # Pass the match instance to set1
            player2_score2.player = player2_name
            player2_score2.score = player2_score_2
            player2_score2.timeout_used = player2_timeout
            player2_score2.save()

            player2_score3 = player2_score3_form.save(commit=False)
            player2_score3.setID = set3  # Pass the match instance to set1
            player2_score3.player = player2_name
            player2_score3.score = player2_score_3
            player2_score3.timeout_used = player2_timeout
            player2_score3.save()

            player2_score4 = player2_score4_form.save(commit=False)
            player2_score4.setID = set4  # Pass the match instance to set1
            player2_score4.player = player2_name
            player2_score4.score = player2_score_4
            player2_score4.timeout_used = player2_timeout
            player2_score4.save()

            player2_score5 = player2_score5_form.save(commit=False)
            player2_score5.setID = set5  # Pass the match instance to set1
            player2_score5.player = player2_name
            player2_score5.score = player2_score_5
            player2_score5.timeout_used = player2_timeout
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
        'school_years': school_years,
        'players' : players,
        'colleges': colleges,
        'coaches': coaches,
        'umpires': umpires,
        'selected_year_id': selected_year_id,
    }
    return render(request, 'stennis_sheet.html', context)

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
    }

    return render(request, 'stennis_scoreboard.html', context)

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
    }
    return render(request, 'dtennis_scoreboard.html', context)

def arnis_school_year(request):
    school_years = SchoolYear.objects.all()
    colleges = College.objects.all()

    context = {
        'school_years' : school_years,
        'colleges' : colleges,
    }

    return render(request, 'arnis_data.html', context)

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
    }
    return render(request, 'arnis_details.html', context)

def volleyball_school_year(request):
    school_years = SchoolYear.objects.all()
    colleges = College.objects.all()

    context = {
        'school_years' : school_years,
        'colleges' : colleges,
    }

    return render(request, 'volleyball_data.html', context)

def tennis_school_year(request):
    school_years = SchoolYear.objects.all()
    colleges = College.objects.all()

    context = {
        'school_years' : school_years,
        'colleges' : colleges,
    }

    return render(request, 'tennis_data.html', context)

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
    }
    return render(request, 'volleyball_details.html', context)

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
    }
    return render(request, 'tennis_details.html', context)


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
    }
    return render(request, 'arnis_labanan.html', context)

def labanan_display(request):
    return render(request, 'labanan_display.html')


def volleyball_display(request):
    return render(request, 'volleyball_display.html')

def stennis_display(request):
    return render(request, 'stennis_display.html')

def dtennis_display(request):
    return render(request, 'dtennis_display.html')

def volleyball_sheet(request):
    school_years = SchoolYear.objects.all().order_by('-start_year')
    colleges = College.objects.all()
    selected_year_id = request.GET.get('school_year')

    if selected_year_id:
        school_year = get_object_or_404(SchoolYear, YearID=selected_year_id)
        teams = VolleyballTeam.objects.filter(yearID=selected_year_id)
        judges = VolleyballJudge.objects.filter(yearID=selected_year_id)
        referees = VolleyballReferee.objects.filter(yearID=selected_year_id)
        scorers = VolleyballScorer.objects.filter(yearID=selected_year_id)

    else:
        teams = VolleyballTeam.objects.all()
        judges = VolleyballJudge.objects.all()
        referees = VolleyballReferee.objects.all()
        scorers = VolleyballScorer.objects.all()

    if request.method == 'POST':
        match_form = VolleyballMatchForm(request.POST)
        if match_form.is_valid():
            match = match_form.save(commit=False)
            match.yearID = school_year
            match.save()

        for i in range(50):
            player_name = request.POST.get(f'player_{i}')
            if not player_name:
                continue  # Skip if player name is not provided

            points = request.POST.get(f'points_{i}')
            team = request.POST.get(f'team_{i}')
                
            player_data = {
                'player': player_name,
                'points': points,
                'team': team
            }
                
            player_form = VolleyballMatchPlayersForm(player_data)

            if player_form.is_valid():
                player = player_form.save(commit=False)
                player.matchID = match
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

            home_team = request.POST.get('home_team')
            away_team = request.POST.get('away_team')

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
        'teams': teams,
        'match_form': match_form,
        'school_years': school_years,
        'colleges': colleges,
        'judges': judges,
        'referees': referees,
        'scorers': scorers,
        'selected_year_id': selected_year_id,
    }
    
    return render(request, 'volleyball_sheet.html', context)


def labanan_sheet(request):
    school_years = SchoolYear.objects.all().order_by('-start_year')
    colleges = College.objects.all()
    selected_year_id = request.GET.get('school_year')

    if selected_year_id:
        school_year = get_object_or_404(SchoolYear, YearID=selected_year_id)
        players = ArnisLabananPlayers.objects.filter(yearID=selected_year_id)
        judges = ArnisJudge.objects.filter(yearID=selected_year_id)
        referees = ArnisReferee.objects.filter(yearID=selected_year_id)
        recorders = ArnisRecorder.objects.filter(yearID=selected_year_id)

    else:
        players = ArnisLabananPlayers.objects.all()
        judges = ArnisJudge.objects.all()
        referees = ArnisReferee.objects.all()
        recorders = ArnisRecorder.objects.all()

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

            match = match_form.save(commit=False)
            match.yearID = school_year
            match.save()

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
        'school_years': school_years,
        'players': players,
        'colleges': colleges,
        'judges': judges,
        'referees': referees,
        'recorders': recorders,
        'selected_year_id': selected_year_id,
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
    }

    
    return render(request, 'labanan_sheet.html', context)

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
    }
    return render(request, 'arnis_anyo.html', context)

def players_list(request):
    school_year_id = request.GET.get('school_year')
    if school_year_id:
        players = list(ArnisFormPlayers.objects.filter(yearID=school_year_id).values('playerID', 'player_name'))
    else:
        players = list(ArnisFormPlayers.objects.all().values('playerID', 'player_name'))
    return JsonResponse({'players': players})

def anyo_display(request):
    return render(request, 'anyo_display.html')

def anyo_sheet(request):
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

    if request.method == 'POST':
        anyo_form = AnyoMatchForm(request.POST)
        if anyo_form.is_valid():
            with transaction.atomic():
                form_match = anyo_form.save(commit=False)
                if school_year:
                    form_match.yearID = school_year
                form_match.save()
                
                for i in range(20):
                    playerID_str = request.POST.get(f'playerID_{i}')
                    
                    try:
                        player_instance = ArnisFormPlayers.objects.get(pk=playerID_str)
                    except ArnisFormPlayers.DoesNotExist:
                        continue  # Skip if player does not exist

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

                    # Convert player_data to FormPlayers instance
                    player_form = AnyoPlayersForm(player_data)
                    if player_form.is_valid():
                        player = player_form.save(commit=False)
                        player.formID = form_match
                        player.playerID = player_instance
                        player.save()                    
                    else:
                        print(player_form.errors)  # Consider more robust error handling

                return redirect('myapp:arnis')  # Ensure this named URL is defined in your urls.py

    # Moved context definition here to ensure tabulators, timers, and managers are defined
    context = {
        'school_years': school_years,
        'tabulators': tabulators,
        'timers': timers,
        'managers': managers,
        'selected_year_id': selected_year_id,
    }
    return render(request, 'anyo_sheet.html', context)

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
    }
    return render(request, 'arnis_bracket.html', context)


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

def volleyball(request):
    return render(request, 'volleyball.html')

def timer(request):
    return render(request, 'timer.html')

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
    }
    return render(request, 'volleyball_bracket.html', context)


def bracket_list2(request):
    school_year_id = request.GET.get('school_year')
    if school_year_id:
        players = list(VolleyballTeam.objects.filter(yearID=school_year_id).values('teamID', 'team_name'))
    else:
        players = list(VolleyballTeam.objects.all().values('teamID', 'team_name'))
    return JsonResponse({'players': players})

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
    }
    return render(request, 'tennis_bracket.html', context)


def bracket_list3(request):
    school_year_id = request.GET.get('school_year')
    if school_year_id:
        players = list(TennisPlayers.objects.filter(yearID=school_year_id).values('playerID', 'player_name'))
    else:
        players = list(TennisPlayers.objects.all().values('playerID', 'player_name'))
    return JsonResponse({'players': players})

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
    }
    return render(request, 'volleyball_scoreboard.html', context)

def add_team(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = VolleyballTeams(request.POST)
        if form.is_valid():
            volleyball_team = form.save(commit=False) 
            volleyball_team.yearID = school_year 
            volleyball_team.save() 
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballTeams()
    return render(request, 'add-team.html', {'form': form})

def edit_team(request, team_id):
    team = get_object_or_404(VolleyballTeam, teamID=team_id)
    if request.method == 'POST':
        form = VolleyballTeams(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballTeams(instance=team)
    return render(request, 'edit-team.html', {'form': form})

def view_players(request, team_id):
    team = VolleyballTeam.objects.get(teamID=team_id)
    players = VolleyballPlayer.objects.filter(teamID=team_id)

    context = {
        'team': team,
        'players': players,
    }
    return render(request, 'volleyball_players.html', context)

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
    return render(request, 'add-volley-player.html', {'form': form})

def edit_volleyball_player(request, player_id):
    player = get_object_or_404(VolleyballPlayer, playerID=player_id)
    if request.method == 'POST':
        form = VolleyballPlayers(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballPlayers(instance=player)
    return render(request, 'edit-volley-player.html', {'form': form})

def add_volleyball_judge(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = VolleyballJudges(request.POST)
        if form.is_valid():
            volleyball_judge = form.save(commit=False) 
            volleyball_judge.yearID = school_year 
            volleyball_judge.save() 
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballJudges()
    return render(request, 'add-volley-judge.html', {'form': form})

def edit_volleyball_judge(request, judge_id):
    judge = get_object_or_404(VolleyballJudge, judgeID=judge_id)
    if request.method == 'POST':
        form = VolleyballJudge(request.POST, instance=judge)
        if form.is_valid():
            form.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballJudge(instance=judge)
    return render(request, 'edit-volley-judge.html', {'form': form})

def add_volleyball_referee(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = VolleyballReferees(request.POST)
        if form.is_valid():
            volleyball_referee = form.save(commit=False)
            volleyball_referee.yearID = school_year
            volleyball_referee.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballReferees()
    return render(request, 'add-volley-referee.html', {'form': form})


def edit_volleyball_referee(request, referee_id):
    referee = get_object_or_404(VolleyballReferee, refereeID=referee_id)
    if request.method == 'POST':
        form = VolleyballReferees(request.POST, instance=referee)
        if form.is_valid():
            form.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballReferees(instance=referee)
    return render(request, 'edit-volley-referee.html', {'form': form})

def add_volleyball_scorer(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = VolleyballScorers(request.POST)
        if form.is_valid():
            volleyball_scorer = form.save(commit=False)
            volleyball_scorer.yearID = school_year
            volleyball_scorer.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballScorers()
    return render(request, 'add-volley-scorer.html', {'form': form})


def edit_volleyball_scorer(request, scorer_id):
    scorer = get_object_or_404(VolleyballScorer, scorerID=scorer_id)
    if request.method == 'POST':
        form = VolleyballScorers(request.POST, instance=scorer)
        if form.is_valid():
            form.save()
            return redirect('myapp:volleyball_sport_data')
    else:
        form = VolleyballScorers(instance=scorer)
    return render(request, 'edit-volley-scorer.html', {'form': form})

def add_tennis_player(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = TennisPlayersForm(request.POST)
        if form.is_valid():
            tennis_player = form.save(commit=False)
            tennis_player.yearID = school_year
            tennis_player.save()
            return redirect('myapp:tennis_sport_data')
    else:
        form = TennisPlayersForm()
    return render(request, 'add-tennis-player.html', {'form': form})


def edit_tennis_player(request, player_id):
    player = get_object_or_404(TennisPlayers, playerID=player_id)
    if request.method == 'POST':
        form = TennisPlayersForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('myapp:tennis_sport_data')
    else:
        form = TennisPlayersForm(instance=player)
    return render(request, 'edit-tennis-player.html', {'form': form})


def add_tennis_umpire(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = TennisUmpires(request.POST)
        if form.is_valid():
            tennis_umpire = form.save(commit=False)
            tennis_umpire.yearID = school_year
            tennis_umpire.save()
            return redirect('myapp:tennis_sport_data')
    else:
        form = TennisUmpires()
    return render(request, 'add-tennis-umpire.html', {'form': form})


def edit_tennis_umpire(request, umpire_id):
    umpire = get_object_or_404(TennisUmpire, umpireID=umpire_id)
    if request.method == 'POST':
        form = TennisUmpires(request.POST, instance=umpire)
        if form.is_valid():
            form.save()
            return redirect('myapp:tennis_sport_data')
    else:
        form = TennisUmpires(instance=umpire)
    return render(request, 'edit-tennis-umpire.html', {'form': form})


def add_tennis_coach(request, year_id):
    school_year = get_object_or_404(SchoolYear, pk=year_id)
    if request.method == 'POST':
        form = TennisCoaches(request.POST)
        if form.is_valid():
            tennis_coach = form.save(commit=False)
            tennis_coach.yearID = school_year
            tennis_coach.save()
            return redirect('myapp:tennis_sport_data')
    else:
        form = TennisCoaches()
    return render(request, 'add-tennis-coach.html', {'form': form})


def edit_tennis_coach(request, coach_id):
    coach = get_object_or_404(TennisCoach, coachID=coach_id)
    if request.method == 'POST':
        form = TennisCoaches(request.POST, instance=coach)
        if form.is_valid():
            form.save()
            return redirect('myapp:tennis_sport_data')
    else:
        form = TennisCoaches(instance=coach)
    return render(request, 'edit-tennis-coach.html', {'form': form})