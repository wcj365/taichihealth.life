#!/usr/bin/bash

# Step 1 - Start from scratch
# Jupyter creates _build folder to store the genreated contents
# We only need to retain the html subfolder for website
# We use docs folder as the document root for setting up GitHub Pages

git pull

if [ -d "_build" ] 
then
    rm -r _build
fi

if [ -d "docs/en" ] 
then
    rm -r docs/en
fi

mkdir ./docs/en

# Step 2 - Generate table of contents

python -m jupyter-book toc from-project src_en -f jb-book -s "_*.*" > src_en/_toc.yml


# Step 3 - Build the static website for the book
# The interim results are in _build folder

jupyter-book build --path-output . src_en > jupyterbook_en.log


# Step 4 - Copy the genreated website to docs folder 

cp -r _build/html/* ./docs/en/   # This is the contents of the generated website
touch ./docs/en/.nojekyll        # ask GitHub Pages not to render the static website using Jekyll

# Step 5 - Push the changes to GitHub

git add .
git commit -m "Built the static website of the books."
git push
