#!/bin/bash

# Check message
if [ -z "$1" ]
then
  echo "❌ Commit message kiriting!"
  echo "Usage: ./auto_git.sh 'your message'"
  exit 1
fi

echo "📦 Adding files..."
git add .

echo "🧾 Committing..."
git commit -m "$1"

echo "🌐 Pushing to GitHub..."
git push origin main

echo "✅ Done!"

