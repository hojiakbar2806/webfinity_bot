# Assuming your Docker container is already running
# Step into your Docker container shell
docker exec -it <container_id_or_name> /bin/bash

# Navigate to your application directory
cd /path/to/your/application

# If using a virtual environment, activate it
source /path/to/venv/bin/activate

# Run Alembic upgrade
alembic upgrade head