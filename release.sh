#!/bin/bash
# Auto-version GitHub release script for DesignTranslatorApp

APP_NAME="DesignTranslatorApp"
REPO="git@github.com:starfish-pengolin/DesignTranslatorApp.git"
RELEASE_TITLE="DesignTranslatorApp Release"
RELEASE_NOTES="Stable release of DesignTranslatorApp"

# --- Get latest tag ---
LATEST_TAG=$(git tag --sort=-v:refname | head -n1)
if [[ -z "$LATEST_TAG" ]]; then
  VERSION="v1.0.0"
else
  IFS='.' read -r MAJOR MINOR PATCH <<< "${LATEST_TAG//v/}"
  PATCH=$((PATCH+1))
  VERSION="v$MAJOR.$MINOR.$PATCH"
fi

ZIP_NAME="${APP_NAME}_${VERSION}.zip"

# --- Zip project excluding venv and git ---
echo "Zipping project as $ZIP_NAME..."
zip -r $ZIP_NAME . -x "*.git*" "venv/*" "*.pyc" "__pycache__/*"

# --- Commit changes ---
echo "Adding and committing changes..."
git add .
git commit -m "Prepare $VERSION release" || echo "Nothing to commit"

# --- Push to GitHub ---
echo "Pushing to GitHub..."
git branch -M main
git remote set-url origin $REPO
git push -u origin main

# --- Create GitHub release ---
echo "Creating GitHub release $VERSION..."
gh release create $VERSION $ZIP_NAME \
  --title "$RELEASE_TITLE $VERSION" \
  --notes "$RELEASE_NOTES"

# --- Print permanent download link ---
echo "Release created! Download link:"
echo "https://github.com/starfish-pengolin/$APP_NAME/releases/download/$VERSION/$ZIP_NAME"

