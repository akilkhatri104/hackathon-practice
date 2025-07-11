from app.db import metadata,engine

metadata.create_all(engine)