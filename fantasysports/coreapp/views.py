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
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


logger = logging.getLogger(__name__)

def is_admin(user):
    """Helper function to check if the user is an admin."""
    return user.email.endswith('@admin.com')

def home(request):
    if request.user.is_authenticated:
        return query(request)
    else:
        return render(request, 'coreapp/home.html')
    
    
@csrf_protect
@login_required
def teams_view(request):
    if request.method == 'POST':
        operation = request.POST.get('operation')
        record_id = request.POST.get('team_id')
        league_id = request.POST.get('league_id')
        user_id = request.POST.get('user_id')
        team_name = request.POST.get('team_name')
        total_points_scored = request.POST.get('total_points_scored')
        status = request.POST.get('status')
        
        try:
            with connection.cursor() as cursor:
                if operation == 'create':
                    cursor.execute("""
                        INSERT INTO team (league_id, user_id, team_name, total_points_scored, status)
                        VALUES (%s, %s, %s, %s, %s)
                    """, [league_id, user_id, team_name, total_points_scored, status])
                    messages.success(request, f"Team '{team_name}' created successfully.")
                
                elif operation == 'update':
                    if not record_id:
                        messages.error(request, "Team ID is required for update.")
                    else:
                        cursor.execute("""
                            UPDATE team
                            SET league_id = %s, user_id = %s, team_name = %s, total_points_scored = %s, status = %s
                            WHERE team_id = %s
                        """, [league_id, user_id, team_name, total_points_scored, status, record_id])
                        messages.success(request, f"Team with ID {record_id} updated successfully.")
                
                elif operation == 'delete':
                    if not record_id:
                        messages.error(request, "Team ID is required for delete.")
                    else:
                        cursor.execute("DELETE FROM team WHERE team_id = %s", [record_id])
                        messages.success(request, f"Team with ID {record_id} deleted successfully.")
                
                else:
                    messages.error(request, "Invalid operation type selected.")

                # Update rankings
                cursor.execute("SELECT updateRankings();")
                messages.success(request, "Rankings updated successfully.")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    try:
        # Fetch all teams for the table display
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT team_id, team_name, league_id, total_points_scored, ranking, status, user_id
                FROM team
                ORDER BY ranking ASC
            """)
            teams = cursor.fetchall()
    except Exception as e:
        messages.error(request, f"An error occurred while fetching teams: {str(e)}")
        teams = []

    return render(request, 'coreapp/user/teams.html', {'teams': teams})


@csrf_protect
@login_required
def players_view(request):
    if request.method == 'POST':
        operation = request.POST.get('operation')
        player_id = request.POST.get('player_id')  # Updated to fetch player ID
        fantasy_team = request.POST.get('fantasy_team')  # Player's fantasy team

        try:
            with connection.cursor() as cursor:
                if operation == 'update':
                    if not player_id:
                        messages.error(request, "Player ID is required for update.")
                    elif not fantasy_team:
                        messages.error(request, "Fantasy Team name is required for update.")
                    else:
                        cursor.execute("""
                            UPDATE player
                            SET fantasy_team = %s
                            WHERE player_id = %s
                        """, [fantasy_team, player_id])
                        messages.success(request, f"Player with ID {player_id} updated successfully.")
                else:
                    messages.error(request, "Invalid operation type selected.")

                # Update rankings if applicable
                cursor.execute("SELECT updateRankings();")
                messages.success(request, "Rankings updated successfully.")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    try:
        # Fetch all players for the table display
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT player_id, full_name, fantasy_team
                FROM player
                ORDER BY player_id ASC
            """)
            players = cursor.fetchall()
    except Exception as e:
        messages.error(request, f"An error occurred while fetching players: {str(e)}")
        players = []

    try:
        # Fetch all teams for the table display
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT team_id, team_name, league_id, total_points_scored, ranking, status, user_id
                FROM team
                ORDER BY ranking ASC
            """)
            teams = cursor.fetchall()
    except Exception as e:
        messages.error(request, f"An error occurred while fetching teams: {str(e)}")
        teams = []

    return render(request, 'coreapp/user/players_teams.html', {
        'players': players,
        'teams': teams
    })



@csrf_exempt
@login_required
def edit_record(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

    data = json.loads(request.body)
    table = data.get('table')
    record_id = data.get('id')
    updates = data.get('updates')

    allowed_tables = ['player', 'team', 'league', 'match_data']
    if table not in allowed_tables:
        return JsonResponse({'success': False, 'error': 'Invalid table selected.'}, status=400)

    try:
        # Dynamically update based on the table and fields
        set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values()) + [record_id]

        query = f"UPDATE {table} SET {set_clause} WHERE {table}_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, values)

        return JsonResponse({'success': True, 'message': 'Record updated successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f"An error occurred: {str(e)}"}, status=400)


@csrf_protect
@login_required
def manage_view(request):
    """
    Handles create, update, and delete operations for team, player, and league tables.
    """
    if not is_admin(request.user):
        return redirect('home')

    if request.method == 'POST':
        operation = request.POST.get('operation')
        table = request.POST.get('table')
        record_id = request.POST.get('record_id')

        try:
            with connection.cursor() as cursor:
                if table == 'team':  # Manage Team operations
                    league_id = request.POST.get('league_id')
                    user_id = request.POST.get('user_id')
                    team_name = request.POST.get('team_name')
                    total_points_scored = request.POST.get('total_points_scored')
                    status = request.POST.get('status')

                    if operation == 'create':
                        cursor.execute("""
                            INSERT INTO team (league_id, user_id, team_name, total_points_scored, status)
                            VALUES (%s, %s, %s, %s, %s)
                        """, [league_id, user_id, team_name, total_points_scored, status])
                        messages.success(request, f"Team '{team_name}' created successfully.")
                    
                    elif operation == 'update':
                        if not record_id:
                            messages.error(request, "Team ID is required for update.")
                        else:
                            cursor.execute("""
                                UPDATE team
                                SET league_id = %s, user_id = %s, team_name = %s, total_points_scored = %s, status = %s
                                WHERE team_id = %s
                            """, [league_id, user_id, team_name, total_points_scored, status, record_id])
                            messages.success(request, f"Team with ID {record_id} updated successfully.")
                    
                    elif operation == 'delete':
                        if not record_id:
                            messages.error(request, "Team ID is required for delete.")
                        else:
                            cursor.execute("DELETE FROM team WHERE team_id = %s", [record_id])
                            messages.success(request, f"Team with ID {record_id} deleted successfully.")
                    
                    # Update rankings after team operations
                    cursor.execute("SELECT updateRankings();")
                    messages.success(request, "Rankings updated successfully.")

                elif table == 'player':  # Manage Player operations
                    full_name = request.POST.get('full_name')
                    sport = request.POST.get('sport')
                    real_team = request.POST.get('real_team')
                    position = request.POST.get('position')
                    fantasy_points = request.POST.get('fantasy_points')
                    availability_status = request.POST.get('availability_status')

                    if operation == 'create':
                        cursor.execute("""
                            INSERT INTO player (full_name, sport, real_team, position, fantasy_points, availability_status)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, [full_name, sport, real_team, position, fantasy_points, availability_status])
                        messages.success(request, f"Player '{full_name}' created successfully.")
                    
                    elif operation == 'update':
                        if not record_id:
                            messages.error(request, "Player ID is required for update.")
                        else:
                            cursor.execute("""
                                UPDATE player
                                SET full_name = %s, sport = %s, real_team = %s, position = %s, fantasy_points = %s, availability_status = %s
                                WHERE player_id = %s
                            """, [full_name, sport, real_team, position, fantasy_points, availability_status, record_id])
                            messages.success(request, f"Player with ID {record_id} updated successfully.")
                    
                    elif operation == 'delete':
                        if not record_id:
                            messages.error(request, "Player ID is required for delete.")
                        else:
                            cursor.execute("DELETE FROM player WHERE player_id = %s", [record_id])
                            messages.success(request, f"Player with ID {record_id} deleted successfully.")

                elif table == 'league':  # Manage League operations
                    league_name = request.POST.get('league_name')
                    league_type = request.POST.get('league_type')
                    draft_date = request.POST.get('draft_date')
                    max_teams = request.POST.get('max_teams')
                    user_id = request.POST.get('user_id')

                    if operation == 'create':
                        cursor.execute("""
                            INSERT INTO league (league_name, league_type, draft_date, max_teams, user_id)
                            VALUES (%s, %s, %s, %s, %s)
                        """, [league_name, league_type, draft_date, max_teams, user_id])
                        messages.success(request, f"League '{league_name}' created successfully.")
                    
                    elif operation == 'update':
                        if not record_id:
                            messages.error(request, "League ID is required for update.")
                        else:
                            cursor.execute("""
                                UPDATE league
                                SET league_name = %s, league_type = %s, draft_date = %s, max_teams = %s, user_id = %s
                                WHERE league_id = %s
                            """, [league_name, league_type, draft_date, max_teams, user_id, record_id])
                            messages.success(request, f"League with ID {record_id} updated successfully.")
                    
                    elif operation == 'delete':
                        if not record_id:
                            messages.error(request, "League ID is required for delete.")
                        else:
                            cursor.execute("DELETE FROM league WHERE league_id = %s", [record_id])
                            messages.success(request, f"League with ID {record_id} deleted successfully.")
                else:
                    messages.error(request, "Invalid table selected.")

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
            if not is_admin(request.user):
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'fantasy_sports'
                    AND table_name NOT LIKE 'coreapp_%'
                    AND table_name != 'user_data'
                """)
            else:
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'fantasy_sports'
                    AND table_name NOT LIKE 'coreapp_%'
                """)
            tables = cursor.fetchall()

            for table_name in tables:
                cursor.execute(f"SELECT * FROM {table_name[0]}")
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                if rows:
                    data[table_name[0]] = {'columns': columns, 'rows': rows}
                else:
                    data[table_name[0]] = {'columns': columns, 'rows': 'No data found in this table.'}

    except Exception as e:
        data['error'] = f"Error fetching data: {str(e)}"

    return render(request, 'coreapp/activity.html', {'tables': data})


@csrf_protect
@login_required
def update_rankings_view(request):
    if request.method == "POST":
        call_update_rankings(request)
        return redirect('teams')  # Redirect back to the teams page


@csrf_exempt
@login_required
def delete_record(request):
    """
    Deletes a record from the specified table, ensuring related records are handled manually.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

    data = json.loads(request.body)
    table = data.get('table')
    record_id = data.get('id')

    dependency_cleanup = {
        'player': [
            {"table": "player_stats", "column": "player_id"},
            {"table": "match_event", "column": "player_id"},
            {"table": "trade", "column": "player_id"},
        ],
        'league': [
            {"table": "draft", "column": "league_id"},
        ],
        'team': [
            {"table": "match_data", "column": "team_id"},
            {"table": "waiver", "column": "team_id"},
            {"table": "match_team", "column": "team_id"},
            {"table": "trade", "column": "team_id"}, 
        ],
        'match_data': [
            {"table": "match_event", "column": "match_id"},
            {"table": "match_team", "column": "match_id"},
        ],
    }

    query_dict = {
        'league': "DELETE FROM league WHERE league_id = %s",
        'team': "DELETE FROM team WHERE team_id = %s",
        'player': "DELETE FROM player WHERE player_id = %s",
        'match_data': "DELETE FROM match_data WHERE match_id = %s",
    }

    query = query_dict.get(table)

    try:
        with connection.cursor() as cursor:
            if table in dependency_cleanup:
                for dependency in dependency_cleanup[table]:
                    dep_table = dependency['table']
                    dep_column = dependency['column']
                    cursor.execute(f"DELETE FROM {dep_table} WHERE {dep_column} = %s", [record_id])

            if not query:
                return JsonResponse({'success': False, 'error': 'Invalid table selected.'}, status=400)

            cursor.execute(query, [record_id])

        return JsonResponse({'success': True, 'message': f'Record deleted successfully from {table}.'})

    except Exception as e:
        if "violates foreign key constraint" in str(e):
            return JsonResponse({
                'success': False,
                'error': f"Cannot delete {table} record because it is still referenced in another table. "
                         f"Ensure all dependencies are removed first."
            }, status=400)
        return JsonResponse({'success': False, 'error': f'An error occurred: {str(e)}'}, status=400)


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
                        role = 'admin' if '@admin.com' in username else 'read_only'

                        with connection.cursor() as cursor:
                            cursor.execute(f"CREATE USER \"{username}\" WITH PASSWORD %s", [password])
                            cursor.execute(f"GRANT {role} TO \"{username}\"")
                            if role == 'admin':
                                cursor.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA fantasy_sports TO \"{username}\"")
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
        full_name = request.POST.get('full_name')
        sport = request.POST.get('sport')
        real_team = request.POST.get('real_team')
        position = request.POST.get('position')
        fantasy_points = request.POST.get('fantasy_points')
        availability_status = request.POST.get('availability_status')

        logger.info(f"Received player data: {full_name}, {sport}, {real_team}, {position}, {fantasy_points}, {availability_status}")

        try:
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
    record_id = data.get('id')
    updates = data.get('updates')

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

        set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values())
        values.append(record_id)
        query = query.replace("{updates}", set_clause)

        with connection.cursor() as cursor:
            cursor.execute(query, values)

        return JsonResponse({'success': True, 'message': 'Record updated successfully.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An error occurred: ' + str(e)}, status=400)

@csrf_protect
@login_required
def front_page(request):
    data = {}
    if request.method == 'POST':
        table_name = request.POST.get('table')  # Get the selected table
        
        valid_tables = ['player', 'team', 'league', 'match_data']
        if table_name not in valid_tables:
            return JsonResponse({'error': 'Invalid table name'}, status=400)

        try:
            with connection.cursor() as cursor:
                # Fetch data from the specified table
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 20")  
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]  

                if rows:
                    data = {'columns': columns, 'rows': rows}
                else:
                    data = {'columns': columns, 'rows': 'Null.'}

        except Exception as e:
            data['error'] = f"Error fetching data: {str(e)}"

    return render(request, 'coreapp/front_page.html', {'data': data})
