from app.settings import *

# In CircleCI the postgres is part of primary container
# hence update the host value to match this
DATABASES["default"]["HOST"] = "localhost"
