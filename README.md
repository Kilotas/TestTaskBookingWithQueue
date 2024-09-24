# Resource Booking API with Queue System

This project is a REST API for booking resources with a queuing system for managing resource availability. The system allows users to book resources, join a queue if all slots are full, and automatically handles booking cancellations and queue management.

## Features

- **Resource Management**: Add, edit, and manage resources, each with slot duration, maximum booking duration, and capacity.
- **Booking System**: Users can book available slots for a resource. If slots are full, they are added to a queue.
- **Queue Management**: If all slots are booked, users can be added to a queue and will be notified when a slot becomes available.
- **Booking Cancellation**: Users can cancel their bookings, which will free up slots for others and notify users in the queue.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    Create a `.env` file in the project root with the following variables:

    ```bash
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    ```

    Alternatively, if you want to use SQLite for development:

    ```bash
    DB_ENGINE=django.db.backends.sqlite3
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser (optional, for admin access):

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Booking Endpoints

- **Create a booking**  
  `POST /bookings/`  
  Creates a booking for a resource. If all slots are full, the user is added to the queue.

  Example request body:

  ```json
  {
    "resource": 1,
    "start_time": "2024-09-24T12:00:00"
  }
{
  "id": 1,
  "resource": 1,
  "start_time": "2024-09-24T12:00:00",
  "end_time": "2024-09-24T14:00:00",
  "status": "active",
  "user": 1
}


Cancel a booking
DELETE /bookings/{booking_id}/
Cancels the booking and releases the slot.
Queue Endpoints
Get user queue
GET /queue/
Retrieves the list of queue entries for the authenticated user.
Authentication
This API supports the following authentication methods:

JWT Authentication
Session Authentication (for development purposes)
Basic Authentication (for development purposes)
To use JWT, you'll need to obtain a token using the /api/token/ endpoint, then include it in the Authorization header of each request:


Swagger Documentation
You can explore the API using the automatically generated Swagger documentation:

Swagger UI: http://localhost:8000/swagger/
Models
Resource
name: The name of the resource.
slot_duration: The duration of each booking slot (in minutes).
max_duration: The maximum allowable duration for a booking (in minutes).
max_capacity: The maximum number of concurrent bookings for this resource.
Booking
user: The user who made the booking.
resource: The resource being booked.
start_time: The start time of the booking.
end_time: The end time of the booking.
status: The current status of the booking (active, queued, completed).
QueueEntry
user: The user in the queue.
resource: The resource for which the user is queued.
queue_position: The user's position in the queue.
created_at: The timestamp when the user was added to the queue.
