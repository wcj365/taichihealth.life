#!/usr/bin/bash

# Step 1 - Start from scratch
# Jupyter creates _build folder to store the genreated contents
# We only need to retain the html subfolder for website
# We use docs folder as the document root for setting up GitHub Pages

source ../taiji74/.venv/bin/activate

git pull

if [ -d "_build" ] 
then
    rm -r _build
fi

if [ -d "docs/cn" ] 
then
    rm -r docs/cn
fi

mkdir ./docs/cn

# Step 2 - Generate table of contents

jupyter-book toc from-project src_cn -f jb-book -s "_*.*" > src_cn/_toc.yml


# Step 3 - Build the static website for the book
# The interim results are in _build folder

jupyter-book build --path-output . src_cn > jupyterbook_cn.log


# Step 4 - Copy the genreated website to docs folder 

cp -r _build/html/* ./docs/cn/   # This is the contents of the generated website
touch ./docs/cn/.nojekyll        # ask GitHub Pages not to render the static website using Jekyll

# Step 5 - Push the changes to GitHub

git add .
git commit -m "Built the static website of the books."
git push
