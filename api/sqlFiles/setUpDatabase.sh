#!/bin/bash

# MySQL credentials
USER=""       # Replace with your MySQL username
PASSWORD=""   # Replace with your MySQL password

# Database name
DB_NAME="carRental"

# Create the database
echo "Creating database '$DB_NAME'..."
mysql -u "$USER" -p"$PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

# Array of SQL files to import (ensure the filenames match exactly)
SQL_FILES=(
    "testdb_cars.sql"
    "testdb_feedback.sql"
    "testdb_insurance.sql"
    "testdb_rentals.sql"
    "testdb_sessions.sql"
    "updated_testdb_cars_with_city.sql"
)

# Import each SQL file into the database
for FILE in "${SQL_FILES[@]}"; do
    if [[ -f $FILE ]]; then
        echo "Importing $FILE into $DB_NAME..."
        mysql -u "$USER" -p"$PASSWORD" "$DB_NAME" < "$FILE"
    else
        echo "File $FILE not found in the current directory. Skipping."
    fi
done

echo "Database setup complete."
