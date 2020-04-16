mkdir gd5
cd gd5

git init
> text echo original-1
>> text echo original-2
>> text echo original-3
git add text && git commit -m'C0'

git checkout -b theirs
> text echo original-1
>> text echo theirs-2
>> text echo original-3
git add text && git commit -m'C1'

git checkout -b yours master
> text echo original-1
>> text echo yours-2
>> text echo original-3
git add text && git commit -m'C2'
