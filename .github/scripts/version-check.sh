#! /bin/bash

if ! git diff origin/main --name-only | grep -q 'VERSION'; then
  echo "VERSION_UPDATED=false" >> "$GITHUB_ENV"
  echo "No Version update found in commit"
else
  echo "VERSION_UPDATED=true" >> "$GITHUB_ENV"
  echo "Version update found in commit"
fi