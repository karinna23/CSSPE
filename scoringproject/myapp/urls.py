from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myapp'

urlpatterns = [    
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('', views.landing, name='landing'),
    path('login/', views.user_login, name='login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('sports/', views.sports, name='sports'),
    path('arnis/', views.arnis, name='arnis'),
    path('arnis_sport/', views.arnis_sport, name='arnis_sport'),
    path('tennis_sport/', views.tennis_sport, name='tennis_sport'),
    path('volleyball/', views.volleyball, name='volleyball'),
    path('table_tennis/', views.tennis, name='table_tennis'),
    path('arnis_labanan/', views.arnis_labanan, name='arnis_labanan'),
    path('labanan_auth/', views.labanan_auth, name='labanan_auth'),
    path('labanan_display/', views.labanan_display, name='labanan_display'),
    path('labanan_sheet/', views.labanan_sheet, name='labanan_sheet'),
    path('arnis_anyo/', views.arnis_anyo, name='arnis_anyo'),
    path('anyo_display/', views.anyo_display, name='anyo_display'),    
    path('anyo_sheet/', views.anyo_sheet, name='anyo_sheet'),
    path('anyo_auth/', views.anyo_auth, name='anyo_auth'),
    path('arnis_sport_data/', views.arnis_school_year, name='arnis_sport_data'),
    path('arnis_sport_details/<int:year_id>/', views.arnis_details, name='arnis_sport_details'),
    path('volleyball_display/', views.volleyball_display, name='volleyball_display'),
    path('volleyball_sport_data/', views.volleyball_school_year, name='volleyball_sport_data'),
    path('volleyball_sport_details/<int:year_id>/', views.volleyball_details, name='volleyball_sport_details'),
    path('add_form_player/<int:year_id>/', views.add_form_player, name='add_form_player'),
    path('add_labanan_player/<int:year_id>/', views.add_labanan_player, name='add_labanan_player'),
    path('edit_form_player/<int:player_id>/', views.edit_form_player, name='edit_form_player'),
    path('edit_labanan_player/<int:player_id>/', views.edit_labanan_player, name='edit_labanan_player'),
    path('add_referee/<int:year_id>/', views.add_referee, name='add_referee'),
    path('edit_referee/<int:referee_id>/', views.edit_referee, name='edit_referee'),
    path('add_judge/<int:year_id>/', views.add_judge, name='add_judge'),
    path('edit_judge/<int:judge_id>/', views.edit_judge, name='edit_judge'),
    path('add_recorder/<int:year_id>/', views.add_recorder, name='add_recorder'),
    path('edit_recorder/<int:recorder_id>/', views.edit_recorder, name='edit_recorder'),
    path('add_tabulator/<int:year_id>/', views.add_tabulator, name='add_tabulator'),
    path('edit_tabulator/<int:tabulator_id>/', views.edit_tabulator, name='edit_tabulator'),
    path('add_timer/<int:year_id>/', views.add_timer, name='add_timer'),
    path('edit_timer/<int:timer_id>/', views.edit_timer, name='edit_timer'),
    path('add_manager/<int:year_id>/', views.add_manager, name='add_manager'),
    path('edit_manager/<int:manager_id>/', views.edit_manager, name='edit_manager'),
    path('add_college/', views.add_college, name='add_college'),
    path('edit_college/<int:college_id>/', views.edit_college, name='edit_college'),
    path('delete_college/<int:college_id>/', views.delete_college, name='delete_college'),
    path('add_year/', views.add_year, name='add_year'),
    path('school_years/delete/<int:year_id>/', views.delete_school_year, name='delete_school_year'),
    path('api/anyo_players/', views.players_list, name='players_list'),
    path('api/labanan_players/', views.bracket_list, name='bracket_list'),
    path('api/form_players/', views.bracket_list1, name='bracket_list1'),
    path('arnis_bracket/', views.arnis_bracket, name='arnis_bracket'),
    path('volleyball_scoreboard/', views.volleyball_scoreboard, name='volleyball_scoreboard'),
    path('add_team/<int:year_id>/', views.add_team, name='add_team'),
    path('edit_team/<int:team_id>/', views.edit_team, name='edit_team'),
    path('view_players/<int:team_id>/', views.view_players, name='view_players'),
    path('add_volleyball_player/<int:team_id>/', views.add_volleyball_player, name='add_volleyball_player'),
    path('edit_volleyball_player/<int:player_id>/', views.edit_volleyball_player, name='edit_volleyball_player'),
    path('timer/', views.timer, name='timer'),
    path('volleyball_sheet/', views.volleyball_sheet, name='volleyball_sheet'),
    path('volleyball_auth/', views.volleyball_auth, name='volleyball_auth'),
    path('single_tennis_scoreboard/', views.stennis_scoreboard, name='stennis_scoreboard'),
    path('single_tennis_display/', views.stennis_display, name='stennis_display'),
    path('single_tennis_sheet/', views.stennis_sheet, name='stennis_sheet'),
    path('stennis_auth/', views.stennis_auth, name='stennis_auth'),
    path('dtennis_auth/', views.dtennis_auth, name='dtennis_auth'),
    path('double_tennis_scoreboard/', views.dtennis_scoreboard, name='stennis_scoreboard'),
    path('double_tennis_display/', views.dtennis_display, name='dtennis_display'),
    path('double_tennis_sheet/', views.dtennis_sheet, name='dtennis_sheet'),
    path('add_volleyball_judge/<int:year_id>/', views.add_volleyball_judge, name='add_volleyball_judge'),
    path('edit_volleyball_judge/<int:judge_id>/', views.edit_volleyball_judge, name='edit_volleyball_judge'),
    path('add_volleyball_referee/<int:year_id>/', views.add_volleyball_referee, name='add_volleyball_referee'),
    path('edit_volleyball_referee/<int:referee_id>/', views.edit_volleyball_referee, name='edit_volleyball_referee'),
    path('add_volleyball_scorer/<int:year_id>/', views.add_volleyball_scorer, name='add_volleyball_scorer'),
    path('edit_volleyball_scorer/<int:scorer_id>/', views.edit_volleyball_scorer, name='edit_volleyball_scorer'),
    path('api/volleyball_players/', views.bracket_list2, name='bracket_list2'),
    path('volleyball_bracket/', views.volleyball_bracket, name='volleyball_bracket'),
    path('tennis_sport_data/', views.tennis_school_year, name='tennis_sport_data'),
    path('tennis_sport_details/<int:year_id>/', views.tennis_details, name='tennis_sport_details'),
    path('add_tennis_coach/<int:year_id>/', views.add_tennis_coach, name='add_tennis_coach'),
    path('edit_tennis_coach/<int:coach_id>/', views.edit_tennis_coach, name='edit_tennis_coach'),
    path('add_tennis_umpire/<int:year_id>/', views.add_tennis_umpire, name='add_tennis_umpire'),
    path('edit_tennis_umpire/<int:umpire_id>/', views.edit_tennis_umpire, name='edit_tennis_umpire'),
    path('add_tennis_player/<int:year_id>/', views.add_tennis_player, name='add_tennis_player'),
    path('edit_tennis_player/<int:player_id>/', views.edit_tennis_player, name='edit_tennis_player'),
    path('api/tennis_players/', views.bracket_list3, name='bracket_list3'),
    path('tennis_bracket/', views.tennis_bracket, name='tennis_bracket'),
    path('arnis_history/', views.arnis_history, name='arnis_history'),
    path('labanan_match_view/<int:match_id>/', views.labanan_match_view, name='labanan_match_view'),
    path('anyo_match_view/<int:form_id>/', views.anyo_match_view, name='anyo_match_view'),
    path('tennis_history/', views.tennis_history, name='tennis_history'),
    path('single_match_view/<int:match_id>/', views.single_match_view, name='single_match_view'),
    path('double_match_view/<int:match_id>/', views.double_match_view, name='double_match_view'),
    path('volleyball_history/', views.volleyball_history, name='volleyball_history'),
    path('volleyball_match_view/<int:match_id>/', views.volleyball_match_view, name='volleyball_match_view'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_school_year/', views.admin_school_year, name='admin_school_year'),
    path('admin_analytics/<int:year_id>/', views.admin_analytics_view, name='admin_analytics'),
    path('admin_users/', views.admin_user_management_view, name='admin_users'),
    path('admin_users/add/', views.admin_add_user_view, name='admin_add_user'),
    path('admin_users/edit/<int:user_id>/', views.admin_edit_user_view, name='admin_edit_user'),
    path('admin_users/delete/<int:user_id>/', views.admin_delete_user_view, name='admin_delete_user'),
    path('admin_users/view/<int:user_id>/', views.admin_view_user_view, name='admin_view_user'),
    path('admin_other_data/', views.admin_other_data, name='admin_other_data'),
    path('delete-form_player/<int:player_id>/', views.delete_arnis_form_player, name='delete_form_player'),
    path('delete-labanan_player/<int:player_id>/', views.delete_arnis_labanan_player, name='delete_labanan_player'),
    path('delete-manager/<int:manager_id>/', views.delete_manager, name='delete_manager'),
    path('delete-referee/<int:referee_id>/', views.delete_referee, name='delete_referee'),
    path('delete-judge/<int:judge_id>/', views.delete_judge, name='delete_judge'),
    path('delete-recorder/<int:recorder_id>/', views.delete_recorder, name='delete_recorder'),
    path('delete-tabulator/<int:tabulator_id>/', views.delete_tabulator, name='delete_tabulator'),
    path('delete-timer/<int:timer_id>/', views.delete_timer, name='delete_timer'),
    path('delete-tennis_player/<int:player_id>/', views.delete_tennis_player, name='delete_tennis_player'),
    path('delete-coach/<int:coach_id>/', views.delete_coach, name='delete_coach'),
    path('delete-umpire/<int:umpire_id>/', views.delete_umpire, name='delete_umpire'),
    path('delete-team/<int:team_id>/', views.delete_team, name='delete_team'),
    path('delete-volley-judge/<int:judge_id>/', views.delete_volley_judge, name='delete_volley_judge'),
    path('delete-volley-referee/<int:referee_id>/', views.delete_volley_referee, name='delete_volley_referee'),
    path('delete-volley-scorer/<int:scorer_id>/', views.delete_volley_scorer, name='delete_volley_scorer'),
    path('delete-player/<int:player_id>/', views.delete_volley_player, name='delete_volley_player'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)