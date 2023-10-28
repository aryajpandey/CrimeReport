# Git Cheat Sheet

## Setup & Initialization
- Install Git: [Download here](https://git-scm.com/downloads)
- Configure user information:
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "you@example.com"
  ```

## Cloning a Repository
- Clone an existing repository:
  ```bash
  git clone https://github.com/user/repo.git
  ```

## Working with Branches
- Create a new branch:
  ```bash
  git branch new-branch
  ```

- Switch to a specific branch:
  ```bash
  git checkout new-branch
  ```

- Create and switch to a new branch in one command:
  ```bash
  git checkout -b new-branch
  ```

- List all branches:
  ```bash
  git branch
  ```

- List all remote branches:
  ```bash
  git branch -r
  ```

## Making Changes
- Stage changes for commit:
  ```bash
  git add .
  ```

- Commit staged changes:
  ```bash
  git commit -m "Commit message"
  ```

## Pushing and Pulling Changes
- Push changes to remote repository:
  ```bash
  git push origin branch-name
  ```

- Pull changes from remote repository:
  ```bash
  git pull origin branch-name
  ```

- Set up tracking for a branch with the remote:
  ```bash
  git push -u origin branch-name
  ```

## Merging Branches
- Merge a branch into the current branch:
  ```bash
  git merge branch-name
  ```

## Viewing History
- View commit history:
  ```bash
  git log
  ```

## Getting Help
- Get help with a Git command:
  ```bash
  git help command
  ```

- Show the Git manual:
  ```bash
  git help
  ```
