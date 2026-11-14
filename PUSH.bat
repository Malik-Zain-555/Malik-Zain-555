@echo off
cd /d "%~dp0"
git init -b main
git config user.name >nul 2>&1 || git config user.name "Malik Zain"
git config user.email >nul 2>&1 || git config user.email "malik-zain-555@users.noreply.github.com"
git add -A
git commit -m "Profile: README + interactive site + auto-update"
git remote remove origin >nul 2>&1
git remote add origin https://github.com/Malik-Zain-555/Malik-Zain-555.git
git push -u origin main --force
echo.
echo Done. If it asked you to sign in, sign in and run this file again.
pause
