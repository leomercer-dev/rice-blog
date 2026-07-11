#!/bin/bash
set -e

echo "=== Building rice.blog ==="
cd /home/leo/Desktop/rice-blog
python3 build.py

echo "=== Switching to gh-pages branch ==="
# Create a temp dir for the gh-pages branch files  
tmpdir=$(mktemp -d)
cp -r /home/leo/Desktop/rice-blog/.git "$tmpdir/"
cd "$tmpdir"
git checkout --orphan gh-pages-deploy 2>/dev/null || git checkout -b gh-pages-deploy
git rm -rf . 2>/dev/null || true

echo "=== Copying _site contents to root ==="
cp -r /home/leo/Desktop/rice-blog/_site/* $tmpdir/
# Clean up the source dir copy
rm -rf /home/leo/Desktop/rice-blog/_site

cd "$tmpdir"
git add -A
git commit --allow-empty-message -m "" 2>/dev/null || git commit -m "Deploy $(date +%Y-%m-%d)" 
git push origin gh-pages-deploy:gh-pages --force
git checkout main 2>/dev/null || true

rm -rf "$tmpdir"
echo "Done! Site deployed to gh-pages branch."
