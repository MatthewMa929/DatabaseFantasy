import json
from django.contrib.auth import authenticate, login, logout
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UserRegisterForm
from django.db import connection
import logging
from django.views.decorators.cache import never_cache

logger = logging.getLogger(__name__)



def home(request):
    if request.user.is_authenticated:
        return query(request)
    else:
        return render(request, 'coreapp/home.html')
    
@csrf_exempt
@login_required
def edit_record(request):
    """
    Updates an existing record in the database.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

    data = json.loads(request.body)
    table = data.get('table')
    player_id = data.get('id')  # The unique identifier for the record
    updates = data.get('updates')  # Dictionary of fields to update

    query_dict = {
        'player': "UPDATE player SET {updates} WHERE player_id = %s",
        'team': "UPDATE team SET {updates} WHERE team_id = %s",
        'league': "UPDATE league SET {updates} WHERE league_id = %s",
        'match_data': "UPDATE match_data SET {updates} WHERE match_id = %s",
    }

    try:
        query = query_dict.get(table)
        if not query:
            return JsonResponse({'success': False, 'error': 'Invalid table selected.'}, status=400)

        # Dynamically create the SET clause and parameters
        set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values())
        values.append(player_id)  # Add player_id as the last parameter
        query = query.replace("{updates}", set_clause)

        with connection.cursor() as cursor:
            cursor.execute(query, values)

        return JsonResponse({'success': True, 'message': 'Record updated successfully.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An error occurred: ' + str(e)}, status=400)

from django.db import connection
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_protect
@login_required
def manage_view(request):
    if request.method == 'POST':
        # #Change this to fit whatever the dropdown bar value is
        # # Draft table
        # draft_id = request.POST.get('DraftID')
        # league_id = request.POST.get('LeagueID')
        # player_id = request.POST.get('PlayerID')
        # draft_date = request.POST.get('draft_date')
        # draft_order = request.POST.get('draft_order')
        # draft_status = request.POST.get('draft_status')

        # # League table
        # league_id = request.POST.get('LeagueID')
        # user_id = request.POST.get('UserID')
        # league_name = request.POST.get('league_name')
        # league_type = request.POST.get('league_type')
        # draft_date = request.POST.get('draft_date')
        # max_teams = request.POST.get('max_teams')

        # # Match data table
        # match_id = request.POST.get('MatchID')
        # team_id = request.POST.get('TeamID')
        # match_date = request.POST.get('match_date')
        # final_score = request.POST.get('final_score')
        # winner = request.POST.get('winner')

        # # Match event table
        # match_event_id = request.POST.get('MatchEventID')
        # match_id = request.POST.get('MatchID')
        # player_id = request.POST.get('PlayerID')
        # event_type = request.POST.get('event_type')
        # event_time = request.POST.get('event_time')
        # fantasy_points = request.POST.get('fantasy_points')

        # # Match team table
        # match_team_id = request.POST.get('MatchTeamID')
        # match_id = request.POST.get('MatchID')
        # team_id = request.POST.get('TeamID')

        # Player table
        player_id = request.POST.get('PlayerID')
        full_name = request.POST.get('full_name')
        sport = request.POST.get('sport')
        real_team = request.POST.get('real_team')
        position = request.POST.get('position')
        fantasy_points = request.POST.get('fantasy_points')
        availability_status = request.POST.get('availability_status')

        # # Player stats table
        # player_stats_id = request.POST.get('PlayerStatsID')
        # player_id = request.POST.get('PlayerID')
        # game_date = request.POST.get('game_date')
        # performance_stats = request.POST.get('performance_stats')
        # injury_status = request.POST.get('injury_status')

        # # Team table
        # team_id = request.POST.get('TeamID')
        # league_id = request.POST.get('LeagueID')
        # user_id = request.POST.get('UserID')
        # team_name = request.POST.get('team_name')
        # total_points_scored = request.POST.get('total_points_scored')
        # ranking = request.POST.get('ranking')
        # status = request.POST.get('status')

        # # Trade table
        # trade_id = request.POST.get('TradeID')
        # player_id = request.POST.get('PlayerID')
        # trade_date = request.POST.get('trade_date')
        # teams_involved = request.POST.get('teams_involved')

        # # User data table
        # user_id = request.POST.get('UserID')
        # full_name = request.POST.get('full_name')
        # email = request.POST.get('email')
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # profile_settings = request.POST.get('profile_settings')

        # # Waiver table
        # waiver_id = request.POST.get('WaiverID')
        # team_id = request.POST.get('TeamID')
        # waiver_status = request.POST.get('waiver_status')
        # waiver_pickup_date = request.POST.get('waiver_pickup_date')


        try:
            with connection.cursor() as cursor:
                if operation == 'create':
                    # Create a new player
                    cursor.execute("""
                        INSERT INTO player (full_name, sport, real_team, position, fantasy_points, availability_status)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, [full_name, sport, real_team, position, fantasy_points, availability_status])
                    messages.success(request, f"Player '{full_name}' created successfully.")

                elif operation == 'update':
                    # Update an existing player
                    if not player_id:
                        messages.error(request, "Record ID is required for update.")
                    else:
                        cursor.execute("""
                            UPDATE player
                            SET full_name = %s, sport = %s, real_team = %s, position = %s, fantasy_points = %s, availability_status = %s
                            WHERE player_id = %s
                        """, [full_name, sport, real_team, position, fantasy_points, availability_status, player_id])
                        messages.success(request, f"Player with ID {player_id} updated successfully.")

                elif operation == 'delete':
                    # Delete an existing player
                    if not player_id:
                        messages.error(request, "Record ID is required for delete.")
                    else:
                        cursor.execute("DELETE FROM player WHERE player_id = %s", [player_id])
                        messages.success(request, f"Player with ID {player_id} deleted successfully.")

                else:
                    messages.error(request, "Invalid operation type selected.")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'coreapp/manage.html')


@never_cache
@csrf_protect
@login_required
def activity_view(request):
    data = {}
    try:
        with connection.cursor() as cursor:
            # Fetch table names excluding coreapp_ prefixed tables
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'fantasy_sports'
                AND table_name NOT LIKE 'coreapp_%'
            """)
            tables = cursor.fetchall()

            for table_name in tables:
                cursor.execute(f"SELECT * FROM {table_name[0]} LIMIT 10")
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                if rows:
                    data[table_name[0]] = {'columns': columns, 'rows': rows}
                else:
                    data[table_name[0]] = {'columns': columns, 'rows': 'No data found in this table.'}

    except Exception as e:
        data['error'] = f"Error fetching data: {str(e)}"

    return render(request, 'coreapp/activity.html', {'tables': data})



@csrf_exempt
@login_required
def delete_record(request):
    """
    Deletes an existing record from the database.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

    data = json.loads(request.body)
    table = data.get('table')
    player_id = data.get('id')  # The unique identifier for the record

    query_dict = {
        'player': "DELETE FROM player WHERE player_id = %s",
        'team': "DELETE FROM team WHERE team_id = %s",
        'league': "DELETE FROM league WHERE league_id = %s",
        'match_data': "DELETE FROM match_data WHERE match_id = %s",
    }

    try:
        query = query_dict.get(table)
        if not query:
            return JsonResponse({'success': False, 'error': 'Invalid table selected.'}, status=400)

        with connection.cursor() as cursor:
            cursor.execute(query, [player_id])

        return JsonResponse({'success': True, 'message': 'Record deleted successfully.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An error occurred: ' + str(e)}, status=400)

@csrf_protect
@login_required
def search_view(request):
    has_write_access = check_write_access(request)
    return render(request, 'coreapp/search.html', {'has_write_access': has_write_access})

@csrf_protect
@login_required
def create_view(request):
    return render(request, 'coreapp/create.html')

def user_profile(request):
    return render(request, 'coreapp/user/profile.html')

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('query')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'coreapp/user/login.html')

def check_write_access(request):
    """Checks if the user has write access based on their privileges in the database."""
    if not request.user.is_authenticated or not request.user.id:
        return False

    try:
        with connection.cursor() as cursor:
            # Check if the user has INSERT privileges on the 'player' table
            cursor.execute(
                "SELECT has_table_privilege(%s, 'player', 'INSERT')", 
                [request.user.username]
            )
            has_write_access = cursor.fetchone()
            return has_write_access[0] if has_write_access else False
    except Exception as e:
        logger.error(f"Error checking write access: {e}")
        return False


def user_register(request):
    """Handles user registration and assigns roles based on email."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            try:
                with transaction.atomic():
                    if User.objects.filter(username=username).exists():
                        form.add_error('email', 'Email already in use. Please choose a different one.')
                    else:
                        user = form.save()
                        # Assign role based on email domain
                        role = 'admin' if '@admin.com' in username else 'read_only'

                        with connection.cursor() as cursor:
                            cursor.execute(f"CREATE USER \"{username}\" WITH PASSWORD %s", [password])
                            cursor.execute(f"GRANT {role} TO \"{username}\"")
                            if role == 'admin':
                                cursor.execute(f"GRANT INSERT ON ALL TABLES IN SCHEMA fantasy_sports TO \"{username}\"")
                        login(request, user)
                        return redirect(reverse('query'))

            except IntegrityError:
                form.add_error('email', 'This username is already taken. Please try again.')
    else:
        form = UserRegisterForm()

    return render(request, 'coreapp/user/register.html', {'form': form})

@login_required
def query(request):
    if request.method == 'POST':
        sql_query = request.POST.get('query')
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                return JsonResponse({'success': 'Query executed successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    has_write_access = check_write_access(request)
    return render(request, 'coreapp/query.html', {'has_write_access': has_write_access})

@csrf_exempt
@login_required
def execute_query(request):
    if request.method == 'POST':
        sql_query = request.POST.get('query')
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                
                if sql_query.lower().startswith('select'):
                    rows = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]
                    results = [dict(zip(columns, row)) for row in rows]
                    return JsonResponse({'success': True, 'results': results})
                else:
                    return JsonResponse({'success': True, 'message': 'Query executed successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@csrf_exempt
@login_required
def execute_raw_sql(request):
    if request.method == 'POST':
        sql_command = request.POST.get('sql_command')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SET ROLE %s", [request.user.username])
                cursor.execute(sql_command)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


def logout_view(request):
    logout(request)
    return redirect('home')

@csrf_protect
@login_required
def create_view(request):
    if not check_write_access(request):
        messages.error(request, 'You do not have write access.')
        return redirect('home')

    if request.method == 'POST':
        # Extract player data from POST request
        full_name = request.POST.get('full_name')
        sport = request.POST.get('sport')
        real_team = request.POST.get('real_team')
        position = request.POST.get('position')
        fantasy_points = request.POST.get('fantasy_points')
        availability_status = request.POST.get('availability_status')

        logger.info(f"Received player data: {full_name}, {sport}, {real_team}, {position}, {fantasy_points}, {availability_status}")

        try:
            # Insert the player into the database
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO player (full_name, sport, real_team, position, fantasy_points, availability_status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [full_name, sport, real_team, position, fantasy_points, availability_status])

            messages.success(request, f"Player '{full_name}' created successfully.")
        except Exception as e:
            logger.error(f"Error creating player: {str(e)}")
            messages.error(request, f"Error creating player: {str(e)}")

    return render(request, 'coreapp/create.html')



@csrf_exempt
@login_required
def perform_search(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
    data = json.loads(request.body)
    table = data.get('table')
    search_value = data.get('search_value', '')

    query_dict = {
        'player': "SELECT full_name, sport, real_team, position, fantasy_points, availability_status FROM player WHERE full_name ILIKE %s",
        'team': "SELECT team_name, total_points_scored, ranking, status FROM team WHERE team_name ILIKE %s",
        'league': "SELECT league_name, league_type, draft_date, max_teams FROM league WHERE league_name ILIKE %s",
        'match_data': "SELECT match_date, final_score, winner FROM match_data WHERE team_id IN (SELECT team_id FROM team WHERE team_name ILIKE %s",
    }

    try:
        query = query_dict.get(table)
        if not query:
            return JsonResponse({'success': False, 'error': 'Invalid table selected.'}, status=400)
        
        params = [search_value] + ['%' + search_value + '%'] * (query.count('%s') - 1)
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]

        return JsonResponse({'success': True, 'results': results})

    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An error occurred: ' + str(e)}, status=400)

@csrf_exempt
@login_required
def edit_record(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

    data = json.loads(request.body)
    table = data.get('table')
    player_id = data.get('id')  # The unique identifier for the record
    updates = data.get('updates')  # Dictionary of fields to update

    query_dict = {
        'player': "UPDATE player SET {updates} WHERE player_id = %s",
        'team': "UPDATE team SET {updates} WHERE team_id = %s",
        'league': "UPDATE league SET {updates} WHERE league_id = %s",
        'match_data': "UPDATE match_data SET {updates} WHERE match_id = %s",
    }

    try:
        query = query_dict.get(table)
        if not query:
            return JsonResponse({'success': False, 'error': 'Invalid table selected.'}, status=400)

        # Dynamically create the SET clause and parameters
        set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values())
        values.append(player_id)  # Add player_id as the last parameter
        query = query.replace("{updates}", set_clause)

        with connection.cursor() as cursor:
            cursor.execute(query, values)

        return JsonResponse({'success': True, 'message': 'Record updated successfully.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An error occurred: ' + str(e)}, status=400)
