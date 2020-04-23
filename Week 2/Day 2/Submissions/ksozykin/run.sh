#!/bin/bash
for clf in SVC KNN LOGREG DUMMY
do
    echo
    echo $clf
    python3 antipatterns_task_ksozykin.py  --test_size=0.33 --seed 42 --clf $clf
done
