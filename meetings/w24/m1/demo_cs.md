commands starting in the demo directory:

    git init
    *add file
    git status
    git add work
    git commit -m "first commit"
    *change file
    git status
    git add .
    git commit -m "adding more work"
    git log --graph --all

https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things

switch to ssh:

    ssh uniqname@oncampus-course.engin.umich.edu
    ssh uniqname@greatlakes.arc-ts.umich.edu
    test out ssh
    ctrl+D

typing out passwords is hard

    cd
    cd .ssh
    ls
    ssh-keygen
    ssh-keygen -t ed25519
    * just typing a name puts the key in your current directory
    ssh uniqname@oncampus-course.engin.umich.edu
    cd .ssh
    vim authorized_keys
    *paste and save
    exit
    ssh uniqname@oncampus-course.engin.umich.edu

    * show how it works on most ssh servers

Even more speeed

    cd .ssh
    * make a config file
    show example config

Remote Repository

    ssh school
    mkdir demo_repo
    cd demo_repo
    git init
    exit
    cd demo
    git remote add origin school:demo_repo
    git remote add remote_name user@ip:demo_repo
    git fetch

    * branches intro
    git checkout -b new_branch
    git log --graph --all
    git push origin new_branch:new_branch

    
    ssh school
    cd demo_repo
    git branch
    git checkout new_branch
    ls
    exit
    cd 
    git clone school:demo_repo
    cd demo_repository
    git branch
    git remote

remote craziness

    git remote add test2 C:\Users\jacob\organizations\demo
    git merge test2/new_branch
    git log --graph --all
    git checkout -b best_branch
    * make changes to work
    git add .
    git commit -m "peak work"
    git log --graph --all
    git push test2 best_branch:best_branch
    cd demo
    git branch
    git log --graph --all
    git merge best_branch
    git log --graph --all


