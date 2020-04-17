# Sets up three git repos:
#  gd4/team -- a repository where other team members work
#  gd4/project.git -- a bare repository that doesn’t have a working directory
#    * shared repository containig git metadata, history and snapshots
#    * it is impossible to edit files and commit changes in it
#    * no working tree -- can only work as a remote
#  gd4/local -- user's own repository where only they work

mkdir gd4
cd gd4

# make a remote repo
mkdir team
cd team

git init
touch C0 && git add C0 && git commit -m'C0'
touch C1 && git add C1 && git commit -m'C1'

cd ..

# make a bare repo that we will use like a repo on github
git clone team project.git --bare

# make a local repo
git clone project.git local

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
cd ../team
git remote add origin ../project.git
touch C8 && git add C8 && git commit -m'C8'
git push -u origin master

# on local
cd ../local
