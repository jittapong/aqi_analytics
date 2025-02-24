#!/bin/bash

# Print a message to indicate the script is running
echo "Running test.sh script..."

# Create a test file
touch test_file.txt

# Write a message to the test file
echo "This is a test file created by test.sh" > test_file.txt

# List the contents of the current directory
ls -l

# Print a success message
echo "test.sh script completed successfully."