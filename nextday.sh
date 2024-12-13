#!/usr/bin/env bash

YEAR=$(date +%Y);
DAY=${1:-$(date +%d)};
FOLDER="./$YEAR/$DAY";

# validate day
if ! [[ $DAY =~ ^[0-9]+$ ]]; then
    echo "Invalid day: $DAY";
    exit 1;
fi

echo "Creating folder for day $DAY in $FOLDER";
mkdir -p $FOLDER;
touch "$FOLDER/main.py";

echo "Adding folder to git...";
git add $FOLDER;

# https://github.com/wimglenn/advent-of-code-data
echo "Downloading day $DAY input to $FOLDER/input.txt...";
aocd $DAY $YEAR > "$FOLDER/input.txt";