#!/bin/bash
echo "===================================================="
echo " Uploading Indian Road Accident Analytics to GitHub"
echo " Repository: https://github.com/123anildalai/indian-road-accident-analytics.git"
echo "===================================================="
git init
git add .
git commit -m "feat: complete b.tech major data analytics project codebase"
git branch -M main
git remote add origin https://github.com/123anildalai/indian-road-accident-analytics.git
git push -u origin main
echo "===================================================="
echo " Project successfully pushed to GitHub!"
echo "===================================================="
