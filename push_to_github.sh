#!/bin/bash

# GitHub Push Script
# Run this script to push your code to GitHub

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║              🚀 GITHUB PUSH SCRIPT                                   ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

echo "📊 Current Status:"
git status --short | head -10
echo ""

echo "🔐 Authentication Required:"
echo "   You need to authenticate with GitHub"
echo ""
echo "   Option 1: Use Personal Access Token (PAT)"
echo "   ----------------------------------------"
echo "   1. Go to: https://github.com/settings/tokens"
echo "   2. Generate new token (classic)"
echo "   3. Select scopes: repo (all)"
echo "   4. Copy the token"
echo "   5. Run: git push -u origin main"
echo "   6. Username: srivigneshr07-IT"
echo "   7. Password: <paste your token>"
echo ""
echo "   Option 2: Use SSH Key"
echo "   ---------------------"
echo "   1. Generate SSH key: ssh-keygen -t ed25519 -C 'srivigneshr07@gmail.com'"
echo "   2. Add to GitHub: https://github.com/settings/keys"
echo "   3. Change remote: git remote set-url origin git@github.com:srivigneshr07-IT/internship-project-final.git"
echo "   4. Push: git push -u origin main"
echo ""
echo "   Option 3: Use GitHub CLI"
echo "   ------------------------"
echo "   1. Install: https://cli.github.com/"
echo "   2. Login: gh auth login"
echo "   3. Push: git push -u origin main"
echo ""

read -p "Press Enter to attempt push (you'll be prompted for credentials)..."

echo ""
echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║              ✅ PUSH SUCCESSFUL                                      ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 Your code is now on GitHub!"
    echo "📍 Repository: https://github.com/srivigneshr07-IT/internship-project-final"
    echo ""
else
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║              ❌ PUSH FAILED                                          ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "⚠️  Authentication failed. Please use one of the options above."
    echo ""
fi
