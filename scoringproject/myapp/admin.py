from django.contrib import admin
from .models import SchoolYear, College, ArnisLabananPlayers, ArnisFormPlayers, ArnisJudge, ArnisRecorder, ArnisReferee, ArnisTabulator, ArnisTimer, VolleyballJudge, VolleyballPlayer, VolleyballTeam, VolleyballReferee,\
    VolleyballScorer, TennisPlayers, TennisUmpire, LabananRound, LabananMatch, LabananScore, FormPlayers, FormMatch, VolleyballMatch, VolleyballMatchPlayers, VolleyballScore, VolleyballSet, TennisCoach, \
    SingleTennisMatch, SingleTennisScore, SingleTennisSet, DoubleTennisMatch, DoubleTennisScore, DoubleTennisSet, CustomUser, ArnisManager

admin.site.register(CustomUser)
admin.site.register(SchoolYear)
admin.site.register(College)
admin.site.register(ArnisLabananPlayers)
admin.site.register(ArnisFormPlayers)
admin.site.register(ArnisManager)
admin.site.register(ArnisJudge)
admin.site.register(ArnisRecorder)
admin.site.register(ArnisReferee)
admin.site.register(ArnisTabulator)
admin.site.register(ArnisTimer)
admin.site.register(LabananScore)
admin.site.register(LabananMatch)
admin.site.register(LabananRound)
admin.site.register(FormMatch)
admin.site.register(FormPlayers)
admin.site.register(VolleyballJudge)
admin.site.register(VolleyballPlayer)
admin.site.register(VolleyballScorer)
admin.site.register(VolleyballReferee)
admin.site.register(VolleyballTeam)
admin.site.register(VolleyballMatch)
admin.site.register(VolleyballMatchPlayers)
admin.site.register(VolleyballScore)
admin.site.register(VolleyballSet)
admin.site.register(TennisPlayers)
admin.site.register(TennisUmpire)
admin.site.register(TennisCoach)
admin.site.register(SingleTennisMatch)
admin.site.register(SingleTennisScore)
admin.site.register(SingleTennisSet)
admin.site.register(DoubleTennisSet)
admin.site.register(DoubleTennisMatch)
admin.site.register(DoubleTennisScore)
