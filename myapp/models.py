from django.db import models
from decimal import Decimal


class SchoolYear(models.Model):
    YearID = models.AutoField(primary_key=True)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    def __str__(self):
        return f"{self.YearID}: {self.start_year}-{self.end_year}"
    
class College(models.Model):
    collegeID = models.AutoField(primary_key=True)
    college_abb = models.CharField(max_length=100)
    college_name = models.CharField(max_length=150)

    def __str__(self):
        return self.college_abb 
   
class ArnisLabananPlayers(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    playerID = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=150)
    collegeID = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.player_name

class ArnisFormPlayers(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    playerID = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=150)
    collegeID = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.player_name

class ArnisReferee(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    refereeID = models.AutoField(primary_key=True)
    referee_name = models.CharField(max_length=150)

    def __str__(self):
        return self.referee_name

class ArnisRecorder(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    recorderID = models.AutoField(primary_key=True)
    recorder_name = models.CharField(max_length=150)

    def __str__(self):
        return self.recorder_name

class ArnisTabulator(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    tabulatorID = models.AutoField(primary_key=True)
    tabulator_name = models.CharField(max_length=150)

    def __str__(self):
        return self.tabulator_name

class ArnisJudge(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    judgeID = models.AutoField(primary_key=True)
    judge_name = models.CharField(max_length=150)

    def __str__(self):
        return self.judge_name

class ArnisTimer(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    timerID = models.AutoField(primary_key=True)
    timer_name = models.CharField(max_length=150)

    def __str__(self):
        return self.timer_name
    
class ArnisManager(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    managerID = models.AutoField(primary_key=True)
    manager_name = models.CharField(max_length=150)

    def __str__(self):
        return self.manager_name

class VolleyballTeam(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    teamID = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=150)
    collegeID = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.team_name

class VolleyballPlayer(models.Model):
    playerID = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=150)
    player_role = models.CharField(max_length=150)
    teamID = models.ForeignKey(VolleyballTeam, on_delete=models.CASCADE)

    def __str__(self):
        return self.player_name

class VolleyballReferee(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    refereeID = models.AutoField(primary_key=True)
    referee_name = models.CharField(max_length=150)

    def __str__(self):
        return self.referee_name
    
class VolleyballJudge(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    judgeID = models.AutoField(primary_key=True)
    judge_name = models.CharField(max_length=150)

    def __str__(self):
        return self.judge_name

class VolleyballScorer(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    scorerID = models.AutoField(primary_key=True)
    scorer_name = models.CharField(max_length=150)

    def __str__(self):
        return self.scorer_name

class TennisPlayers(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    playerID = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=150)
    collegeID = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.player_name
    
class TennisCoach(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    coachID = models.AutoField(primary_key=True)
    coach_name = models.CharField(max_length=150)

    def __str__(self):
        return self.coach_name
    
class TennisUmpire(models.Model):
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    umpireID = models.AutoField(primary_key=True)
    umpire_name = models.CharField(max_length=150)

    def __str__(self):
        return self.umpire_name

class LabananMatch(models.Model):
    matchID = models.AutoField(primary_key=True)
    match_no = models.IntegerField(null=True, blank=True)
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, null=True, blank=True)
    event = models.CharField(max_length=255, null=True, blank=True)
    venue = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    division = models.CharField(max_length=255, null=True, blank=True)
    weight_category = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    blue_team = models.ForeignKey(College, related_name='blue_team_matches', on_delete=models.CASCADE, null=True, blank=True)
    red_team = models.ForeignKey(College, related_name='red_team_matches', on_delete=models.CASCADE, null=True, blank=True)
    blue_player = models.ForeignKey(ArnisLabananPlayers, related_name='blue_player_matches', on_delete=models.CASCADE, null=True, blank=True)
    red_player = models.ForeignKey(ArnisLabananPlayers, related_name='red_player_matches', on_delete=models.CASCADE, null=True, blank=True)
    judge1 = models.ForeignKey(ArnisJudge, related_name='judge1_matches',  on_delete=models.CASCADE, null=True, blank=True)
    judge2 = models.ForeignKey(ArnisJudge, related_name='judge2_matches',  on_delete=models.CASCADE, null=True, blank=True)
    judge3 = models.ForeignKey(ArnisJudge, related_name='judge3_matches',  on_delete=models.CASCADE, null=True, blank=True)
    referee = models.ForeignKey(ArnisReferee, related_name='referee_matches', on_delete=models.CASCADE, null=True, blank=True)
    recorder = models.ForeignKey(ArnisRecorder, related_name='recorder_matches', on_delete=models.CASCADE, null=True, blank=True)
    final_winner = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Match {self.matchID} - {self.event}"

class LabananRound(models.Model):
    roundID = models.AutoField(primary_key=True)
    matchID = models.ForeignKey(LabananMatch, on_delete=models.CASCADE, null=True, blank=True)
    round_num = models.IntegerField(null=True, blank=True)
    time = models.CharField(max_length=50, null=True, blank=True)  # Use DurationField for time duration
    winner = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Round {self.round_num} of Match {self.matchID}"

class LabananScore(models.Model):
    scoreID = models.AutoField(primary_key=True)
    roundID = models.ForeignKey(LabananRound, on_delete=models.CASCADE, null=True, blank=True)
    playerID = models.ForeignKey(ArnisLabananPlayers, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=0, null=True, blank=True)
    foul = models.IntegerField(default=0, null=True, blank=True)
    disarmed = models.IntegerField(default=0, null=True, blank=True)
    total_score = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"Score for Player {self.playerID} in Round {self.roundID.round_num}"
    
class FormMatch(models.Model):
    formID = models.AutoField(primary_key=True)
    form_type = models.CharField(max_length=255, null=True, blank=True)
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, null=True, blank=True)
    form_no = models.IntegerField(null=True, blank=True)
    venue = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    division = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    preference = models.CharField(max_length=255, blank=True, null=True)
    tabulator = models.ForeignKey(ArnisTabulator, related_name='tabulator_matches', on_delete=models.CASCADE, null=True, blank=True)
    timer = models.ForeignKey(ArnisTimer, related_name='timer_matches', on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(ArnisManager, related_name='manager_matches', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Form {self.formID} - {self.form_type}"

class FormPlayers(models.Model):
    formplayersID = models.AutoField(primary_key=True)
    formID = models.ForeignKey(FormMatch, on_delete=models.CASCADE, null=True, blank=True)
    playerID = models.ForeignKey(ArnisFormPlayers, on_delete=models.CASCADE, null=True, blank=True)
    judgeScores1 = models.IntegerField(default=0, null=True, blank=True)
    judgeScores2 = models.IntegerField(default=0, null=True, blank=True)
    judgeScores3 = models.IntegerField(default=0, null=True, blank=True)
    judgeScores4 = models.IntegerField(default=0, null=True, blank=True)
    judgeScores5 = models.IntegerField(default=0, null=True, blank=True)
    time = models.IntegerField(default=0, null=True, blank=True)
    lost_control = models.IntegerField(default=0, null=True, blank=True)
    outside = models.IntegerField(default=0, null=True, blank=True)
    other = models.IntegerField(default=0, null=True, blank=True)
    time_consumed = models.CharField(max_length=255, null=True, blank=True)
    rank = models.IntegerField(default=0, null=True, blank=True)
    total_score = models.FloatField(default=0, null=True, blank=True)
    
    def __str__(self):
        return f"Data for Player {self.playerID} in form {self.formID}"
    
class VolleyballMatch(models.Model):
    matchID = models.AutoField(primary_key=True)
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, null=True, blank=True)
    event = models.CharField(max_length=100, blank=True)
    place = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    match_no = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    start = models.TimeField(blank=True, null=True)
    finish = models.TimeField(blank=True, null=True)
    home_team = models.CharField(max_length=100, blank=True)
    away_team = models.CharField(max_length=100, blank=True)
    winning_team = models.CharField(max_length=100, blank=True)
    losing_team = models.CharField(max_length=100, blank=True)
    referee1 = models.ForeignKey(VolleyballReferee, related_name='refereed_matches1', on_delete=models.CASCADE, blank=True, null=True)
    referee2 = models.ForeignKey(VolleyballReferee, related_name='refereed_matches2', on_delete=models.CASCADE, blank=True, null=True)
    line_judge1 = models.ForeignKey(VolleyballJudge, related_name='judged_matches1', on_delete=models.CASCADE, blank=True, null=True)
    line_judge2 = models.ForeignKey(VolleyballJudge, related_name='judged_matches2', on_delete=models.CASCADE, blank=True, null=True)
    scorer = models.ForeignKey(VolleyballScorer, related_name='scored_matches', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Match {self.matchID} - {self.match_no}"
    
class VolleyballSet(models.Model):
    matchID = models.ForeignKey(VolleyballMatch, on_delete=models.CASCADE, null=True, blank=True)
    setID = models.AutoField(primary_key=True)
    set_no = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    winner = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Set {self.set_no} of {self.matchID}"

class VolleyballScore(models.Model):
    scoreID = models.AutoField(primary_key=True)
    setID = models.ForeignKey(VolleyballSet, on_delete=models.CASCADE, blank=True, null=True)
    team= models.CharField(max_length=100, blank=True)
    timeout_used = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.team} - {self.score} in {self.setID}"

class VolleyballMatchPlayers(models.Model):
    player =  models.CharField(max_length=100, null=True, blank=True)
    matchID = models.ForeignKey(VolleyballMatch, on_delete=models.CASCADE, blank=True, null=True)
    team = models.CharField(max_length=100,null=True, blank=True)
    points = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.player} point {self.points} in {self.matchID}"
    
class SingleTennisMatch(models.Model):
    matchID = models.AutoField(primary_key=True)
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, null=True, blank=True)
    group = models.CharField(max_length=100, blank=True)
    table = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    match_no = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    stage = models.CharField(max_length=100, blank=True, null=True)
    player1_name = models.CharField(max_length=100, blank=True)
    player2_name = models.CharField(max_length=100, blank=True)
    winning_team = models.CharField(max_length=100, blank=True)
    losing_team = models.CharField(max_length=100, blank=True)
    coach1 = models.ForeignKey(TennisCoach, related_name='coach1', on_delete=models.CASCADE, blank=True, null=True)
    coach2 = models.ForeignKey(TennisCoach, related_name='coach2', on_delete=models.CASCADE, blank=True, null=True)
    umpire = models.ForeignKey(TennisUmpire, related_name='umpire', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Match {self.matchID} - {self.match_no}"
    
class SingleTennisSet(models.Model):
    matchID = models.ForeignKey(SingleTennisMatch, on_delete=models.CASCADE, null=True, blank=True)
    setID = models.AutoField(primary_key=True)
    set_no = models.IntegerField(blank=True, null=True)
    winner = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Set {self.set_no} of {self.matchID}"

class SingleTennisScore(models.Model):
    scoreID = models.AutoField(primary_key=True)
    setID = models.ForeignKey(SingleTennisSet, on_delete=models.CASCADE, blank=True, null=True)
    player = models.CharField(max_length=100, null=True, blank=True)
    timeout_used = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.player} - {self.score} in {self.setID}"
    
class DoubleTennisMatch(models.Model):
    matchID = models.AutoField(primary_key=True)
    yearID = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, null=True, blank=True)
    group = models.CharField(max_length=100, blank=True)
    table = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    match_no = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    stage = models.CharField(max_length=100, blank=True, null=True)
    player1_name = models.CharField(max_length=100, blank=True)
    player2_name = models.CharField(max_length=100, blank=True)
    player3_name = models.CharField(max_length=100, blank=True)
    player4_name = models.CharField(max_length=100, blank=True)
    winning_team = models.CharField(max_length=100, blank=True)
    losing_team = models.CharField(max_length=100, blank=True)
    coach1 = models.ForeignKey(TennisCoach, related_name='doubles_coach1', on_delete=models.CASCADE, blank=True, null=True)
    coach2 = models.ForeignKey(TennisCoach, related_name='doubles_coach2', on_delete=models.CASCADE, blank=True, null=True)
    umpire = models.ForeignKey(TennisUmpire, related_name='doubles_umpire', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Match {self.matchID} - {self.match_no}"
    
class DoubleTennisSet(models.Model):
    matchID = models.ForeignKey(DoubleTennisMatch, on_delete=models.CASCADE, null=True, blank=True)
    setID = models.AutoField(primary_key=True)
    set_no = models.IntegerField(blank=True, null=True)
    winner = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Set {self.set_no} of {self.matchID}"

class DoubleTennisScore(models.Model):
    scoreID = models.AutoField(primary_key=True)
    setID = models.ForeignKey(DoubleTennisSet, on_delete=models.CASCADE, blank=True, null=True)
    player = models.CharField(max_length=100, null=True, blank=True)
    timeout_used = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.player} - {self.score} in {self.setID}"