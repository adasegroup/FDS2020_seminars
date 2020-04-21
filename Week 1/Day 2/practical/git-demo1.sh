# Branches are work-in-progress, tags are milestones
#  * try makind new branches and commit in them checkout, branch
#  * try moving branch tips to other commits: branch, reset
#  * try tagging and using `git describe`

mkdir gd1
cd gd1

git init

touch backpack
git add backpack && git commit -m'C0'

>> backpack echo sweater
git add backpack && git commit -m'C1'

>> backpack echo wallet
git add backpack && git commit -m'C2'

>> backpack echo socks
>> backpack echo gloves
git add backpack && git commit -m'C3'

>> backpack echo canned beans
>> backpack echo chips
git add backpack && git commit -m'C4'
