from backend.api.database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        cols_users = [
            ("full_name", "VARCHAR(100)"),
            ("phone", "VARCHAR(20)"),
            ("location", "VARCHAR(100)"),
            ("address", "VARCHAR(255)"),
            ("highest_degree", "VARCHAR(100)"),
            ("university", "VARCHAR(150)"),
            ("year_of_passing", "VARCHAR(10)"),
            ("cgpa", "VARCHAR(20)"),
            ("skills", "JSON"),
            ("projects", "JSON")
        ]
        
        cols_apps = [
            ("university", "VARCHAR(150)"),
            ("year_of_passing", "VARCHAR(10)"),
            ("cgpa", "VARCHAR(20)")
        ]
        
        for col, dtype in cols_users:
            res = conn.execute(text(f"SHOW COLUMNS FROM users LIKE '{col}';")).fetchone()
            if not res:
                print(f"Adding column users.{col}")
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {dtype} NULL;"))
                
        for col, dtype in cols_apps:
            res = conn.execute(text(f"SHOW COLUMNS FROM applications LIKE '{col}';")).fetchone()
            if not res:
                print(f"Adding column applications.{col}")
                conn.execute(text(f"ALTER TABLE applications ADD COLUMN {col} {dtype} NULL;"))
                
        conn.commit()
        print("Database migration completed successfully!")

if __name__ == "__main__":
    migrate()
