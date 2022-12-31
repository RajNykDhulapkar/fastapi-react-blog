from app.core.security import get_password_hash
from faker import Faker

fake = Faker()


# The simplest solution I found is to set up an event for each table that executes a method after the table is created.

# Database initial data
INITIAL_DATA = {
    'user': [
        {
            "name": "John Doe",
            "email": "johndoe@example.com",
            'hashed_password': get_password_hash('password123')
        }
    ],
    'post': []
}

for _ in range(10):
    INITIAL_DATA['user'].append({
        'name': fake.name(),
        'email': fake.email(),
        'hashed_password': get_password_hash('password123')
    })


# list of unsplash image urls for blog banner
image_urls = [
]

for _ in range(100):
    INITIAL_DATA['post'].append({
        'title': fake.sentence(),
        'content': fake.text(1000),
        "image_url": f"https://source.unsplash.com/random/800x600?sig={fake.random_int(min=1, max=1000)}",
        'author_id': fake.random_int(min=1, max=10)
    })


# This method receives a table, a connection and inserts data to that table.
def initialize_table(target, connection, **kw):
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        connection.execute(target.insert(), INITIAL_DATA[tablename])
        print(f"Table {tablename} initialized")
