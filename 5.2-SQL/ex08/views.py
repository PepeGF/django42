from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.conf import settings
import psycopg2

def connect_db()-> psycopg2.extensions.connection | None:
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
def init(request: HttpRequest):
    conn = connect_db()
    if conn is None:
        return HttpResponse("DB connection error")
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex08_planets (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                climate TEXT,
                diameter INTEGER,
                orbital_period INTEGER,
                population BIGINT,
                rotation_period INTEGER,
                surface_water NUMERIC,
                terrain VARCHAR(128)
            );
                    
            CREATE TABLE IF NOT EXISTS ex08_people (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                birth_year VARCHAR(32),
                gender VARCHAR(32),
                eye_color VARCHAR(32),
                hair_color VARCHAR(32),
                height INTEGER,
                mass NUMERIC,
                homeworld VARCHAR(64),
                CONSTRAINT fk_homeworld FOREIGN KEY (homeworld) REFERENCES ex08_planets(name) ON DELETE SET NULL
            );
        """)
        conn.commit()
        return HttpResponse("OK")
    except Exception as e:
        conn.rollback()
        return HttpResponse(f"Error: {e}")
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass

def parse_planets_data(raw_data) -> list[dict]:
    planets = []
    for line in raw_data:  # Skip header
        if len(line) != 8:
            continue  # Skip malformed lines
        name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain = line
        planets.append({
            'name': name,
            'climate': climate if climate != 'NULL' else None,
            'diameter': int(diameter) if diameter.isdigit() else None,
            'orbital_period': int(orbital_period) if orbital_period.isdigit() else None,
            'population': int(population) if population.isdigit() else None,
            'rotation_period': int(rotation_period) if rotation_period.isdigit() else None,
            'surface_water': float(surface_water) if surface_water.replace('.', '', 1).isdigit() else None,
            'terrain': terrain
        })
    return planets

def parse_people_data(raw_data) -> list[dict]:
    people = []
    for line in raw_data:  # Skip header
        if len(line) != 8:
            continue  # Skip malformed lines
        name, birth_year, gender, eye_color, hair_color, height, mass, homeworld = line
        people.append({
            'name': name,
            'birth_year': birth_year if birth_year not in ('NULL', 'n/a') else None,
            'gender': gender if gender not in ('NULL', 'n/a') else None,
            'eye_color': eye_color if eye_color not in ('NULL', 'n/a') else None,
            'hair_color': hair_color if hair_color not in ('NULL', 'n/a') else None,
            'height': int(height) if height.isdigit() else None,
            'mass': float(mass) if mass.replace('.', '', 1).isdigit() else None,
            'homeworld': homeworld if homeworld not in ('NULL', 'n/a') else None
        })
    return people

def populate(request: HttpRequest):
    with open('ex08/planets.csv', 'r') as f:
        planets_data_raw = [line.strip().split('\t') for line in f]
    planets_data = parse_planets_data(planets_data_raw)
    with open('ex08/people.csv', 'r') as f:
        people_data_raw = [line.strip().split('\t') for line in f]
    people_data = parse_people_data(people_data_raw)
    conn = connect_db()
    if conn is None:
        return HttpResponse("No data available")
    cur = conn.cursor()
    try:
        for planet in planets_data:
            try:
                cur.execute("""
                    INSERT INTO ex08_planets (name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    planet['name'],
                    planet['climate'],
                    planet['diameter'],
                    planet['orbital_period'],
                    planet['population'],
                    planet['rotation_period'],
                    planet['surface_water'],
                    planet['terrain']
                ))
            except Exception as e:
                conn.rollback()
                return HttpResponse(f"Error inserting planet {planet['name']}: {e}")
        conn.commit()
        for person in people_data:
            try:
                cur.execute("""
                    INSERT INTO ex08_people (name, birth_year, gender, eye_color, hair_color, height, mass, homeworld)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    person['name'],
                    person['birth_year'],
                    person['gender'],
                    person['eye_color'],
                    person['hair_color'],
                    person['height'],
                    person['mass'],
                    person['homeworld']
                ))
            except Exception as e:
                conn.rollback()
                return HttpResponse(f"Error inserting person {person['name']}: {e}")
        conn.commit()
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass
    return HttpResponse("OK")

def display(request: HttpRequest):
    try:
        conn = connect_db()
        if conn is None:
            return HttpResponse("No data available")
        cur = conn.cursor()
        cur.execute("""
            SELECT p.name, p.homeworld, pl.climate
            FROM ex08_people p
            LEFT JOIN ex08_planets pl ON p.homeworld = pl.name
                WHERE pl.climate LIKE '%windy%'
            ORDER BY p.name;
            """)
        results = cur.fetchall()
        if not results:
            return HttpResponse("No data available")
        return render(request, 'ex08/display.html', {'results': results})
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass