import requests
import random
import pprint
import json

from faker import Faker  # Import Faker library for generating fake data
from datetime import datetime, timedelta

fake = Faker()

UNKNOWN_AUTHOR_ID = 132
UNKNOWN_PUBLISHER_ID = 74 

GANRES_IDS = {
    "fiction": 1,
    "nonfiction": 2,
    "science-fiction": 3, 
    "mystery": 4,
    "romance": 5,
    "history": 6,
    "biography": 7
}

def transform_date(date_str):
    try:
        # Parse the date string into a datetime object
        date_obj = datetime.fromisoformat(date_str)

        # Format the datetime object into "YYYY-MM-DD" format
        formatted_date = date_obj.strftime("%Y-%m-%d")
        return formatted_date
    except:
        return ""


def generate_random_birthdate():
    start_date = datetime(1900, 1, 1)
    end_date = datetime.now() - timedelta(days=365*18)  # Assuming authors are at least 18 years old
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")

def generate_random_nationality():
    nationalities = ["American", "British", "Canadian", "French", "German", "Japanese", "Russian", "Chinese", "Indian"]
    return random.choice(nationalities)

def generate_random_address():
    return fake.address()

def generate_random_phone_number():
    return fake.phone_number()

def fetch_random_books(num_books, ganre):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    books = []
    iterations = 0

    while len(books) < num_books:
        # Generate a random index to get a random page of books
        random_index = str(random.randint(1, 100))
        params = {
            "q": f"subject:{ganre}",  # You can adjust the query to fit your needs
            "startIndex": random_index,
            "maxResults": min(40, num_books - len(books)),  
            # "orderBy": "relevance"  
            "orderBy": "newest"  
        }
        response = requests.get(base_url, params=params)
        iterations += 1

        if response.status_code == 200:
            data = response.json()
            books.extend(data.get("items", []))
        else:
            print("Failed to fetch books:", response.status_code)
            break

    all_books_data = []

    for i, book in enumerate(books[:num_books], start=1):
        title = book['volumeInfo']['title']
        authors_info = book['volumeInfo'].get('authors', ['Unknown'])
        authors = ", ".join(authors_info)
        publisher = book['volumeInfo'].get('publisher', 'Unknown Publisher')
        published_date = transform_date(book['volumeInfo'].get('publishedDate', '1000-01-01'))
        isbn_13 = next((identifier['identifier'] for identifier in book['volumeInfo'].get('industryIdentifiers', []) if identifier['type'] == 'ISBN_13'), 'Unknown')
        page_count = book['volumeInfo'].get('pageCount', 0)
        average_rating = book['volumeInfo'].get('averageRating', 0)
        
        # Generate random birthdate and nationality for each author
        authors_birthdates = [generate_random_birthdate() for _ in authors_info]
        authors_nationalities = [generate_random_nationality() for _ in authors_info]
        
        publisher_address = generate_random_address()
        publisher_phone = generate_random_phone_number()

        book_data = {
            "title": title,
            "authors": [{"name": author, "birthdate": birthdate, "nationality": nationality} for author, birthdate, nationality in zip(authors_info, authors_birthdates, authors_nationalities)],
            "publisher": {"name": publisher, "address": publisher_address, "phone": publisher_phone},
            "publication_date": published_date,
            "isbn": isbn_13,
            "page_count": page_count,
            "rating": average_rating,
            "price": random.randint(4, 50)
        }

        all_books_data.append(book_data)

    return all_books_data

def add_publishers(publisher):
    response = requests.post('http://127.0.0.1:8000/api/v1/publishers/', publisher)
    print(f"{response.status_code} | {response.text}")

def add_authors(authors):
    for author in authors: 
        name = author['name'].split()
        if len(name) < 2:
            name.append("")
        body = {
            "first_name": name[0],
            "last_name": name[1],
            "birthdate": author["birthdate"],
            "nationality": author["nationality"]
        }
        response = requests.post('http://127.0.0.1:8000/api/v1/authors/', body)
        print(f"{response.status_code} | {response.text}")

def add_books(book_payload, ganre):
    authors_json = dict() 
    publishers_json = dict() 

    response = requests.get('http://127.0.0.1:8000/api/v1/authors/')
    response_json = response.json()

    for author in response_json:
        authors_json[f"{author['first_name']} {author['last_name']}"] = author["id"]  

    response = requests.get('http://127.0.0.1:8000/api/v1/publishers/')
    response_json = response.json()

    for publisher in response_json:
        publishers_json[publisher["name"]] = publisher["id"] 

    book_payload['publisher'] = publishers_json.get(book_payload['publisher']['name'], UNKNOWN_PUBLISHER_ID)

    name = book_payload["authors"][0]["name"].split() 
    if len(name) < 2:
        name.append("")
    authors_list = []
    authors_list.append(authors_json.get(f"{name[0]} {name[1]}", UNKNOWN_AUTHOR_ID))
    book_payload['author'] = authors_list 
    book_payload['ganres'] = [GANRES_IDS[ganre]] 
    
    response = requests.post('http://127.0.0.1:8000/api/v1/books/', book_payload)
    print(f"{response.status_code} | {response.text}")


def set_ganre():
    response = requests.get('http://127.0.0.1:8000/api/v1/books/')
    books_json = response.json()

    books_ids= [book["id"] for book in books_json] 
    

    for id in books_ids:
        response = requests.patch(f"http://127.0.0.1:8000/api/v1/books/{id}/", {"ganres": [1]})
        print(f"{response.status_code} | {response.text}")

ganres = ["mystery", "romance", "history", "biography"]

for ganre in ganres:
    books = fetch_random_books(2000, ganre) 
    for book in books:
        add_publishers(book['publisher'])
        add_authors(book['authors'])

        add_books(book, ganre)

