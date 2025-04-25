from app.db.session import engine, Base
from app.models.user import User
from app.models.post import Post


print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
