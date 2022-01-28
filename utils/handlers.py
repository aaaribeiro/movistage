from models.database import SessionLocal

# context manager to handle database connections
class DbHandler:
    def __enter__(self):
       self.db = SessionLocal()
       return self.db
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.db.close()


# get_db function that yeilds db for endpoints
def get_db():
    with DbHandler() as db:
        yield db