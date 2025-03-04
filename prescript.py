from app.auth import hash_password
from app.db_config import SessionLocal
from app.models import User, Presentation, Conference

session = SessionLocal()

admin = User(is_superuser=True,
             login='admin',
             first_name='admin',
             last_name='admin',
             hashed_password=hash_password('secret'))

session.add(admin)
session.commit()
session.close()
