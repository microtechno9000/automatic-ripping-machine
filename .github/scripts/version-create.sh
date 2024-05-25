#! /bin/bash

PR_TITLE=$(jq -r '.pull_request.title' "$GITHUB_EVENT_PATH")
if [[ "$PR_TITLE" == *"[FEATURE]"* ]]; then
  VERSION_TYPE="minor"
  echo "PR set to FEATURE updating minor version"
elif [[ "$PR_TITLE" == *"[BUGFIX]"* ]]; then
  VERSION_TYPE="patch"
  echo "PR set to BUGFIX updating patch version"
else
  echo "No version bump flag found in PR title. Exiting."
  echo "Edit your PR title to include either FEATURE or BUGFIX"
  exit 1
fi
CURRENT_VERSION=$(cat VERSION)
IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
if [ "$VERSION_TYPE" == "minor" ]; then
  VERSION_PARTS[1]=$((VERSION_PARTS[1]+1))
  VERSION_PARTS[2]=0
elif [ "$VERSION_TYPE" == "patch" ]; then
  VERSION_PARTS[2]=$((VERSION_PARTS[2]+1))
fi
NEW_VERSION="${VERSION_PARTS[0]}.${VERSION_PARTS[1]}.${VERSION_PARTS[2]}"
echo "NEW_VERSION=$NEW_VERSION" >> $GITHUB_ENV
echo "CURRENT_VERSION=$CURRENT_VERSION" >> $GITHUB_ENV
echo "New Version: " $NEW_VERSION