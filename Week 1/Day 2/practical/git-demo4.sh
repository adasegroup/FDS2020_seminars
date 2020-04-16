mkdir gd4
cd gd4

# make a remote repo
mkdir _remote
cd _remote

git init
touch C0 && git add C0 && git commit -m'C0'
touch C1 && git add C1 && git commit -m'C1'

cd ..

# make a bare relay repo
git clone _remote remote.git --bare

# make a local repo
git clone remote.git local

# add local work
cd local
git checkout -b side1
touch C2 && git add C2 && git commit -m'C2'

git checkout -b side2
touch C3 && git add C3 && git commit -m'C3'
touch C4 && git add C4 && git commit -m'C4'

git checkout -b side3
touch C5 && git add C5 && git commit -m'C5'
touch C6 && git add C6 && git commit -m'C6'
touch C7 && git add C7 && git commit -m'C7'

# add remote work
cd ../_remote
git remote add origin ../remote.git
touch C8 && git add C8 && git commit -m'C8'
git push -u origin master

# on local
cd ../local
