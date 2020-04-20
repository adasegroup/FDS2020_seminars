# Try to make a branch with cabin approved backpack contents
#  * use cherry-pick, checkout -b, rebase et c.
#  * if you feel adventurous, see what `git bisect` does and try to find the first bad commit with it
mkdir gd2
cd gd2

git init

touch backpack
git add backpack && git commit -m'empty'

>> backpack echo wallet
git add backpack && git commit -m'wallet'

git checkout -b conference master
>> backpack echo sweater
git add backpack && git commit -m'sweater'

>> backpack echo pass
git add backpack && git commit -m'pass'

>> backpack echo shampoo
git add backpack && git commit -m'shampoo'

>> backpack echo laptop
git add backpack && git commit -m'laptop'

>> backpack echo booze
git add backpack && git commit -m'booze'

>> backpack echo power bank
git add backpack && git commit -m'power bank'

>> backpack echo poster
git add backpack && git commit -m'poster'


