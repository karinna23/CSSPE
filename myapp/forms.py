from django import forms
from .models import ArnisFormPlayers, College, ArnisLabananPlayers, ArnisReferee, ArnisJudge, ArnisRecorder, ArnisTabulator, ArnisTimer, SchoolYear, LabananMatch, LabananRound, LabananScore, ArnisManager, FormMatch, FormPlayers , \
VolleyballPlayer, VolleyballJudge, VolleyballReferee, VolleyballScorer, VolleyballTeam, VolleyballMatch, VolleyballMatchPlayers,VolleyballScore, VolleyballSet, TennisCoach, TennisPlayers, TennisUmpire, SingleTennisSet, SingleTennisMatch, \
SingleTennisScore, DoubleTennisScore, DoubleTennisMatch, DoubleTennisSet

class ArnisPlayersForm(forms.ModelForm):
    class Meta:
        model = ArnisFormPlayers
        fields = ['player_name', 'collegeID']
        labels = {
            'player_name': 'Player Name',
            'collegeID': 'College',
        }

class ArnisPlayersLabanan(forms.ModelForm):
    class Meta:
        model = ArnisLabananPlayers
        fields = ['player_name', 'collegeID']
        labels = {
            'player_name': 'Player Name',
            'collegeID': 'College',
        }

class ArnisReferees(forms.ModelForm):
    class Meta:
        model = ArnisReferee
        fields = ['referee_name']
        labels = {
            'referee_name': 'Referee Name',
        }

class ArnisJudges(forms.ModelForm):
    class Meta:
        model = ArnisJudge
        fields = ['judge_name']
        labels = {
            'judge_name': 'Judge Name',
        }

class ArnisRecorders(forms.ModelForm):
    class Meta:
        model = ArnisRecorder
        fields = ['recorder_name']
        labels = {
            'recorder_name': 'Recorder Name',
        }

class ArnisTabulators(forms.ModelForm):
    class Meta:
        model = ArnisTabulator
        fields = ['tabulator_name']
        labels = {
            'tabulator_name': 'Tabulator Name',
        }

class ArnisTimers(forms.ModelForm):
    class Meta:
        model = ArnisTimer
        fields = ['timer_name']
        labels = {
            'timer_name': 'Timer Name',
        }

class ArnisManagers(forms.ModelForm):
    class Meta:
        model = ArnisManager
        fields = ['manager_name']
        labels = {
            'manager_name': 'Manager Name',
        }

class Colleges(forms.ModelForm):
    class Meta:
        model = College
        fields = ['college_abb', 'college_name']
        labels = {
            'college_abb': 'College Abbreviation',
            'college_name' : 'College Name',
        }

class SchoolYears(forms.ModelForm):
    class Meta:
        model = SchoolYear
        fields = ['start_year', 'end_year']
        labels = {
            'start_year': 'School Year Start',
            'end_year' : 'School Year End',
        }
    
class LabananMatchForm(forms.ModelForm):
    class Meta:
        model = LabananMatch
        fields = ['match_no', 'yearID', 'event', 'venue', 'date', 'division', 'weight_category', 'area', 'blue_team', 'red_team', 'blue_player', 'red_player', 'judge1', 'judge2', 'judge3', 'referee', 'recorder', 'final_winner']

class LabananRoundForm(forms.ModelForm):
    class Meta:
        model = LabananRound
        fields = ['round_num', 'time', 'winner']

class LabananScoreForm(forms.ModelForm):
    class Meta:
        model = LabananScore
        fields = ['foul', 'disarmed', 'total_score', 'score']

class AnyoMatchForm(forms.ModelForm):
    class Meta:
        model = FormMatch
        fields = ['form_no', 'yearID', 'form_type', 'venue', 'date', 'division', 'category', 'preference', 'tabulator', 'timer', 'manager']

class AnyoPlayersForm(forms.ModelForm):
    class Meta:
        model = FormPlayers
        fields = ['judgeScores1', 'judgeScores2', 'judgeScores3', 'judgeScores4', 'judgeScores5', 'time', 'lost_control', 'outside', 'other', 'time_consumed', 'rank', 'total_score']

class VolleyballTeams(forms.ModelForm):
    class Meta:
        model = VolleyballTeam
        fields = ['team_name', 'collegeID']
        labels = {
            'team_name': 'Team Name',
            'collegeID' : 'College',
        }

class VolleyballPlayers(forms.ModelForm):
    class Meta:
        model = VolleyballPlayer
        fields = ['player_name', 'player_role']
        labels = {
            'player_name': 'Player Name',
            'player_role': 'Player Role',
        }

class VolleyballReferees(forms.ModelForm):
    class Meta:
        model = VolleyballReferee
        fields = ['referee_name']
        labels = {
            'referee_name': 'Referee Name',
        }

class VolleyballJudges(forms.ModelForm):
    class Meta:
        model = VolleyballJudge
        fields = ['judge_name']
        labels = {
            'judge_name': 'Judge Name',
        }

class VolleyballScorers(forms.ModelForm):
    class Meta:
        model = VolleyballScorer
        fields = ['scorer_name']
        labels = {
            'scorer_name': 'Scorer Name',
        }

class VolleyballMatchForm(forms.ModelForm):
    class Meta:
        model = VolleyballMatch
        fields = ['yearID', 'event', 'place', 'category', 'match_no', 'date', 'start', 'finish', 'home_team', 'away_team', 'winning_team', 'losing_team', 'referee1', 'referee2', 'line_judge1', 'line_judge2', 'scorer']

class VolleyballSetForm(forms.ModelForm):
    class Meta:
        model = VolleyballSet
        fields = ['matchID', 'set_no', 'time', 'winner']

class VolleyballScoreForm(forms.ModelForm):
    class Meta:
        model = VolleyballScore
        fields = ['setID', 'team', 'timeout_used', 'score']

class VolleyballMatchPlayersForm(forms.ModelForm):
    class Meta:
        model = VolleyballMatchPlayers
        fields = ['player', 'matchID', 'team', 'points']

class SingleTennisMatchForm(forms.ModelForm):
    class Meta:
        model = SingleTennisMatch
        fields = ['yearID', 'group', 'table', 'category', 'match_no', 'date', 'time', 'stage', 'player1_name', 'player2_name', 'winning_team', 'losing_team', 'coach1', 'coach2', 'umpire']

class SingleTennisSetForm(forms.ModelForm):
    class Meta:
        model = SingleTennisSet
        fields = ['matchID', 'set_no', 'winner']

class SingleTennisScoreForm(forms.ModelForm):
    class Meta:
        model = SingleTennisScore
        fields = ['setID', 'player', 'timeout_used', 'score']

class DoubleTennisMatchForm(forms.ModelForm):
    class Meta:
        model = DoubleTennisMatch
        fields = ['yearID', 'group', 'table', 'category', 'match_no', 'date', 'time', 'stage', 'player1_name', 'player2_name', 'player3_name', 'player4_name', 'winning_team', 'losing_team', 'coach1', 'coach2', 'umpire']

class DoublelTennisSetForm(forms.ModelForm):
    class Meta:
        model = DoubleTennisSet
        fields = ['matchID', 'set_no', 'winner']

class DoubleTennisScoreForm(forms.ModelForm):
    class Meta:
        model = DoubleTennisScore
        fields = ['setID', 'player', 'timeout_used', 'score']

class TennisPlayersForm(forms.ModelForm):
    class Meta:
        model = TennisPlayers
        fields = ['collegeID', 'player_name']
        labels = {
            'player_name': 'Player Name',
            'collegeID': 'Team Name',
        }

class TennisUmpires(forms.ModelForm):
    class Meta:
        model = TennisUmpire
        fields = ['umpire_name']
        labels = {
            'umpire_name': 'Umpire Name',
        }

class TennisCoaches(forms.ModelForm):
    class Meta:
        model = TennisCoach
        fields = ['coach_name']
        labels = {
            'coach_name': 'Coach Name',
        }
