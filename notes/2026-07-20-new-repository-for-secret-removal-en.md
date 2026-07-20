---
audio: false
generated: true
image: false
lang: en
layout: post
title: New Repository for Secret Removal
translated: false
type: note
---

Question: For GitHub Enterprise, is creating a new repository, deleting the old one, and renaming the new one a good way to remove leaked secret files, since orphan commits are hard to delete even with history rewriting?

Answer:

Yes, **creating a fresh repository and migrating only clean history is often the most reliable operational solution**, especially for enterprise environments where you need high confidence that leaked secrets are gone. But there are some important nuances.

The key point:

> Deleting a file in Git does not delete the secret. Rewriting history may remove it from normal refs, but old objects can survive in clones, caches, forks, mirrors, backups, and GitHub internal storage.

### Option 1: Rewrite history (preferred when you need to preserve repo identity)

Typical tools:

* `git filter-repo` (recommended)
* BFG Repo-Cleaner

Example:

```bash
git clone --mirror git@github.com:company/repo.git
cd repo.git

git filter-repo --path secrets.env --invert-paths

git push --force --mirror
```

Then:

1. Rotate/revoke the leaked keys immediately.
2. Ask all developers to reclone.
3. Trigger GitHub secret scanning.
4. Contact GitHub Enterprise support if you need backend object removal.

Problem:

Even after:

```bash
git gc --prune=now
```

you cannot guarantee every copy disappears.

Why?

Git objects can exist in:

* developer machines
* CI caches
* forks
* pull request refs
* GitHub backups
* package caches
* artifact storage

`git gc` only cleans **your local object database**.

---

### Option 2: New repository migration (your approach)

This is often the cleanest enterprise approach.

Flow:

```
old-repo
    |
    | export clean source
    v
new-repo
    |
    | rename
    v
production-repo-name
```

Example:

```bash
# create clean repository
mkdir new-repo
cd new-repo

git init

cp -r ../clean-source/* .

git add .
git commit -m "Initial clean import"

git remote add origin git@github.com:company/new-repo.git
git push -u origin main
```

Then:

```
old-repo
    -> archive
    -> delete
new-repo
    -> rename to old name
```

Advantages:

* guaranteed clean Git object graph
* no old commits
* no hidden dangling blobs
* simpler audit story

For highly sensitive leaks (AWS keys, production passwords, private certificates), this is often the safest path.

---

### But don't forget: the secret is already compromised

Repository deletion does **not** fix:

```
secret leaked
        |
        +--> GitHub
        +--> developer clones
        +--> CI logs
        +--> Docker images
        +--> backups
        +--> screenshots
```

The correct incident response order:

```
1. Revoke secret
       |
       v
2. Rotate credentials
       |
       v
3. Remove from repository
       |
       v
4. Audit access logs
       |
       v
5. Clean history / migrate repo
```

For example:

AWS:

```bash
aws iam delete-access-key
aws iam create-access-key
```

GitHub PAT:

```
Settings
 -> Developer settings
 -> Personal access tokens
 -> Revoke
```

---

### Enterprise recommendation

For a company repository:

| Situation                                 | Best choice                     |
| ----------------------------------------- | ------------------------------- |
| Accidentally committed normal config file | `git filter-repo`               |
| API key/password leaked                   | rotate + filter history         |
| Private key/certificate leaked            | rotate + new repo               |
| Compliance/security audit                 | new repo migration              |
| Huge repo with many users                 | filter history + GitHub support |

For a serious enterprise incident, I would usually do:

```
1. Freeze old repo
2. Revoke all secrets
3. Create clean repo
4. Import clean source
5. Preserve old repo as private archive
6. Rename repositories
7. Update CI/CD references
8. Force everyone to reclone
```

The new repository approach is not just "easier"; it creates a **new cryptographic object graph**, which is the closest thing to a guaranteed clean state.
