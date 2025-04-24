from app import create_app, db
from app import models

app = create_app()
app.app_context().push()
db.create_all()