import json
from datetime import date

# ---------------------- Helper Functions ----------------------
def read_json(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
# ---------------------- User Functions ----------------------
def add_user():
    new_user = input("Enter New User Name: ")
    project = "project_users.json"
    field_names = ["user_id", "user_name"]
    with open(project, "r") as project_users:
        names = json.load(project_users)
        i = len(names) + 1
    users_json = {"user_id": i, "user_name": new_user}
    names.append(users_json)
    with open(project, "w") as project_users:
        json.dump(names, project_users, indent=4)
        
    print(f"User {new_user} is added with the User ID {i}.")

def view_user():
    with open("project_users.json", "r") as project_users:
        users_json = json.load(project_users)
        for u in users_json:
            print("...".join(str(val) for val in u.values()))

# ---------------------- Movie Functions ----------------------
def add_movie():
    movie_title = input("Enter New Movie Title: ")
    movie_director = input("Enter New Movie Director: ")
    movie_year = int(input("Enter New Movie Year: "))
    movie_copies = int(input("Enter New Movie Available Copies: "))
    project = "project_movies.json"
    with open(project, "r") as project_movies:
        movies = json.load(project_movies)
        movie_id = 101 + len(movies)

    new_movies = {
        "movie_id": movie_id,
        "title": movie_title,
        "director": movie_director,
        "year": movie_year,
        "available_copies": movie_copies
    }
    movies.append(new_movies)
    with open(project, "w") as project_movies:
        json.dump(movies, project_movies, indent=4)

    print(f"Movie {movie_title} is added with the Movie ID {movie_id}")

def view_movie():
    with open("project_movies.json", "r") as project_movies:
        movies = json.load(project_movies)
        for m in movies:
            print(",".join(str(value) for value in m.values()))
# ---------------------- Borrow Functions ----------------------
def borrow_movies():
    user_id = input("Enter User ID: ")
    movie_ids = input("Enter Movie IDs to borrow (comma-separated): ").split(",")
    movie_ids = [int(m.strip()) for m in movie_ids]
    movies = read_json("project_movies.json")
    
    available = [] # start with empty list
    unavailable = [] # start with empty list
    borrowed_titles = [] # list to store borrowed movie titles

    #Loop through each entered movie ID to check if it's available
    for movie_id in movie_ids:
        found = False # Used to check if the movie exists in the system
        for movie in movies: # Match entered movie_id with data in file 
            if movie["movie_id"] == movie_id:
                found = True # Check if the movie has copies available
                if movie["available_copies"] > 0:  # Check if the movie is available
                    available.append(movie_id) # ← Movie is available
                    movie["available_copies"] = (movie["available_copies"]) - 1
                    borrowed_titles.append(movie["title"])

                else:
                    unavailable.append(movie_id)  # ← Movie is found
                break # Stop searching after the movie is found

         # After checking all entered movie IDs
        if not found:
            unavailable.append(movie_id) # ← Movie ID does not exist in the system
    if not available:
        print("None of the selected movies are available or valid. Please try again.")
        return # Repeat the loop from the beginning
    
    # Save the updated list of movies back to 'available_copies.json'
    save_json("project_movies.json", movies)
    borrow_data = read_json("borrowings.json")
    borrow_data.append({
        "user_id": int(user_id),
        "movie_ids": available,
        "borrow_date": date.today().isoformat()
    })
    save_json("borrowings.json", borrow_data)
    print("Movie(s) successfully borrowed: " + ', '.join(borrowed_titles))
    if unavailable:
        print("Movie(s) not available or not found: " + ', '.join(unavailable))
        
# ---------------------- Return Movies ----------------------
def return_movies():
    user_id = int(input("Enter User ID: "))
    movie_ids = input("Enter Movie IDs to return (comma-separated): ").split(",")
    movie_ids = [int(mid.strip()) for mid in movie_ids]
    borrowings = read_json("borrowings.json")
    movies = read_json("project_movies.json")
    found_record = False
    updated = False
    for record in borrowings:
        if record.get("user_id") == user_id:
            found_record = True
            original_movie_ids = record["movie_ids"]
            for movie_id in movie_ids:
                if movie_id in original_movie_ids:
                    for movie in movies:
                        if movie["movie_id"] == movie_id:
                            movie["available_copies"] = movie["available_copies"] + 1
                            break
                    original_movie_ids.remove(movie_id)
                    updated = True
                    print(f"Movie {movie_id} returned successfully.")
                else:
                    print(f"Movie {movie_id} was not borrowed by user {user_id}.")
            if not original_movie_ids:
                borrowings.remove(record)
            break
    if not found_record:
        print("No borrowing record found for this user.")
    if updated:
        save_json("borrowings.json", borrowings)
        save_json("project_movies.json", movies)
        print("Return process completed.")
    else:
        print("No valid movie returns were processed.")
# ---------------------- Borrowed Movies ----------------------
def list_borrowed_movies():
    user_id = int(input("Enter User ID to view borrowed movies: "))
    borrowings = read_json("borrowings.json")
    movies = read_json("project_movies.json")
    
    borrowed_movie_ids = []
    borrow_dates = []
    
    for record in borrowings:
        if record["user_id"] == user_id:
            
            borrowed_movie_ids.extend(record["movie_ids"])
            borrow_dates.append(record["borrow_date"])
            borrowed_movie_ids = list(set(borrowed_movie_ids))
            
    if not borrowed_movie_ids:
        print(f"No borrowings found for User ID: {user_id}")
        return
    
    borrowed_movie_ids = list(set(borrowed_movie_ids))

    print(f"\nUser {user_id} borrowed {len(borrowed_movie_ids)} movie(s):")
    for movie_id in borrowed_movie_ids:
        title = next((m["title"] for m in movies if m["movie_id"] == movie_id), "(Title not found)")
        print(f"- {movie_id}: {title}")
    
    
    print(f"Borrow date(s): {', '.join(set(borrow_dates))}")

# ---------------------- Main Menu ----------------------
def project_redi():
    while True:
        print("------Movie Management System-----")
        print("1. Add User")
        print("2. View Users")
        print("3. Add Movie")
        print("4. View Movies")
        print("5. Borrow Movies")
        print("6. Return Movies")
        print("7. List Borrowed Movies")
        print("8. Exit")
        
        try:
            number = int(input("Enter your choice: "))
        except ValueError:
            number = 0
        if number >= 1 and number <= 8:
            pass
        else:
            print("Invalid input. Enter a number from 1 to 8.")

        if number == 1:
            add_user()

        elif number == 2:
            view_user()

        elif number == 3:
            add_movie()

        elif number == 4:
            view_movie()

        elif number == 5:
            borrow_movies()

        elif number == 6:
            return_movies()

        elif number == 7:
            list_borrowed_movies()

        elif number == 8:
            print("Exiting program")
            exit(0)
            
if __name__ == "__main__":
    project_redi()