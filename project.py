import uuid
from datetime import datetime, timedelta

class Movie:
    def __init__(self, title, duration, genre):
        self.movie_id = str(uuid.uuid4())[:8]
        self.title = title
        self.duration = duration
        self.genre = genre

class Showtime:
    def __init__(self, movie, start_time, total_seats=50):
        self.showtime_id = str(uuid.uuid4())[:8]
        self.movie = movie
        self.start_time = start_time
        self.total_seats = total_seats
        self.available_seats = list(range(1, total_seats + 1))
        self.booked_seats = {}

class Theater:
    def __init__(self):
        self.movies = []
        self.showtimes = []
        self.bookings = {}

    def add_movie(self, title, duration, genre):
        movie = Movie(title, duration, genre)
        self.movies.append(movie)
        return movie

    def add_showtime(self, movie, start_time):
        showtime = Showtime(movie, start_time)
        self.showtimes.append(showtime)
        return showtime

    def display_movies(self):
        print("\n--- Available Movies ---")
        for movie in self.movies:
            print(f"ID: {movie.movie_id} | Title: {movie.title} | Genre: {movie.genre} | Duration: {movie.duration} mins")

    def display_showtimes(self, movie):
        print(f"\nShowtimes for {movie.title}")
        matching_showtimes = [st for st in self.showtimes if st.movie == movie]
        for showtime in matching_showtimes:
            print(f"Showtime ID: {showtime.showtime_id} | Time: {showtime.start_time}")

    def book_ticket(self, showtime, seat_number, customer_name):
        if seat_number not in showtime.available_seats:
            print("Sorry, this seat is already booked or doesn't exist.")
            return None

        booking_id = str(uuid.uuid4())[:8]
        booking = {
            'booking_id': booking_id,
            'customer_name': customer_name,
            'movie': showtime.movie.title,
            'showtime': showtime.start_time,
            'seat_number': seat_number
        }

        showtime.available_seats.remove(seat_number)
        showtime.booked_seats[seat_number] = customer_name
        self.bookings[booking_id] = booking

        return booking

    def cancel_booking(self, booking_id):
        if booking_id not in self.bookings:
            print("Invalid booking ID.")
            return False

        booking = self.bookings[booking_id]
        for showtime in self.showtimes:
            if showtime.movie.title == booking['movie'] and showtime.start_time == booking['showtime']:
                showtime.available_seats.append(booking['seat_number'])
                del showtime.booked_seats[booking['seat_number']]
                break

        del self.bookings[booking_id]
        print(f"Booking {booking_id} has been cancelled.")
        return True

def main():
    theater = Theater()

  
    avengers = theater.add_movie("Avengers: Endgame", 181, "Action")
    inception = theater.add_movie("Inception", 148, "Sci-Fi")

   
    theater.add_showtime(avengers, datetime(2024, 6, 15, 18, 0))
    theater.add_showtime(avengers, datetime(2024, 6, 15, 21, 0))
    theater.add_showtime(inception, datetime(2024, 6, 15, 19, 30))

    while True:
        print("\n--- Movie Booking System ---")
        print("1. View Movies")
        print("2. View Showtimes")
        print("3. Book a Ticket")
        print("4. Cancel a Booking")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            theater.display_movies()
        
        elif choice == '2':
            theater.display_movies()
            movie_id = input("Enter movie ID to view showtimes: ")
            selected_movie = next((m for m in theater.movies if m.movie_id == movie_id), None)
            if selected_movie:
                theater.display_showtimes(selected_movie)
        
        elif choice == '3':
            theater.display_movies()
            movie_id = input("Enter movie ID: ")
            selected_movie = next((m for m in theater.movies if m.movie_id == movie_id), None)
            
            if selected_movie:
                theater.display_showtimes(selected_movie)
                showtime_id = input("Enter showtime ID: ")
                selected_showtime = next((st for st in theater.showtimes if st.showtime_id == showtime_id), None)
                
                if selected_showtime:
                    print(f"Available seats: {selected_showtime.available_seats}")
                    seat_number = int(input("Choose a seat number: "))
                    customer_name = input("Enter your name: ")
                    
                    booking = theater.book_ticket(selected_showtime, seat_number, customer_name)
                    if booking:
                        print(f"Booking successful! Your booking ID is {booking['booking_id']}")
        
        elif choice == '4':
            booking_id = input("Enter your booking ID to cancel: ")
            theater.cancel_booking(booking_id)
        
        elif choice == '5':
            print("Thank you for using the Movie Booking System!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()