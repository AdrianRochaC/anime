from app.routes import app
import os
os.makedirs("instance", exist_ok=True)


if __name__ == "__main__":
    app.run(debug=True)
