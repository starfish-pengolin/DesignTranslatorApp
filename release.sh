#!/bin/bash
# Auto-version GitHub release script for DesignTranslatorApp
# Clean zip excluding venv, .git, .ssh, caches, and temp files

APP_NAME="DesignTranslatorApp"
REPO="git@github.com:starfish-pengolin/DesignTranslatorApp.git"
RELEASE_TITLE="DesignTranslatorApp Release"
RELEASE_NOTES="Stable release of DesignTranslatorApp"

# --- 1) Get latest tag and increment patch version ---
LATEST_TAG=$(git tag --sort=-v:refname | head -n1)
if [[ -z "$LATEST_TAG" ]]; then
  VERSION="v1.0.0"
else
  IFS='.' read -r MAJOR MINOR PATCH <<< "${LATEST_TAG//v/}"
  PATCH=$((PATCH+1))
  VERSION="v$MAJOR.$MINOR.$PATCH"
fi

ZIP_NAME="${APP_NAME}_${VERSION}.zip"

# --- 2) Zip project cleanly ---
echo "Zipping project as $ZIP_NAME..."
zip -r $ZIP_NAME . \
  -x "*.git*" \
  -x "venv/*" \
  -x "*.pyc" \
  -x "__pycache__/*" \
  -x ".ssh/*" \
  -x "tmp/*" \
  -x "frontend_dist/*" \
  -x "node_modules/*" \
  -x "*.log" \
  -x "*.zip"

# --- 3) Commit changes ---
echo "Adding and committing changes..."
git add .
git commit -m "Prepare $VERSION release" || echo "Nothing to commit"

# --- 4) Push to GitHub ---
echo "Pushing to GitHub..."
git branch -M main
git remote set-url origin $REPO
git push -u origin main

# --- 5) Create GitHub release ---
echo "Creating GitHub release $VERSION..."
gh release create $VERSION $ZIP_NAME \
  --title "$RELEASE_TITLE $VERSION" \
  --notes "$RELEASE_NOTES"

# --- 6) Print permanent download link ---
echo "Release created! Direct download link:"
echo "https://github.com/starfish-pengolin/$APP_NAME/releases/download/$VERSION/$ZIP_NAME"

#!/bin/bash
# Auto-version GitHub release script for DesignTranslatorApp
# Includes hidden credit automatically

APP_NAME="DesignTranslatorApp"
REPO="git@github.com:starfish-pengolin/DesignTranslatorApp.git"
RELEASE_TITLE="DesignTranslatorApp Release"
RELEASE_NOTES="Stable release of DesignTranslatorApp"

# 1) Determine new version
LATEST_TAG=$(git tag --sort=-v:refname | head -n1)
if [[ -z "$LATEST_TAG" ]]; then
  VERSION="v1.0.0"
else
  IFS='.' read -r MAJOR MINOR PATCH <<< "${LATEST_TAG//v/}"
  PATCH=$((PATCH+1))
  VERSION="v$MAJOR.$MINOR.$PATCH"
fi

ZIP_NAME="${APP_NAME}_${VERSION}.zip"

# 2) Add hidden credit
echo "Powered by Mosh3L" > hidden_credit.txt

# 3) Zip project cleanly
zip -r $ZIP_NAME . \
  -x "*.git*" \
  -x "venv/*" \
  -x "*.pyc" \
  -x "__pycache__/*" \
  -x ".ssh/*" \
  -x "tmp/*" \
  -x "frontend_dist/*" \
  -x "node_modules/*" \
  -x "*.log" \
  -x "*.zip"

# 4) Commit changes
git add .
git commit -m "Prepare $VERSION release" || echo "Nothing to commit"

# 5) Push to GitHub
git branch -M main
git remote set-url origin $REPO
git push -u origin main

# 6) Create GitHub release
gh release create $VERSION $ZIP_NAME \
  --title "$RELEASE_TITLE $VERSION" \
  --notes "$RELEASE_NOTES"

# 7) Print permanent download link
echo "Release created! Direct download link:"
echo "https://github.com/starfish-pengolin/$APP_NAME/releases/download/$VERSION/$ZIP_NAME"

# 8) Clean up
rm hidden_credit.txt
