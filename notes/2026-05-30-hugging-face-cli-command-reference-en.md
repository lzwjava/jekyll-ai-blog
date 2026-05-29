---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hugging Face CLI Command Reference
translated: false
type: note
---

Here's the complete `hf` CLI map, organized by group. Everything lives under the `hf` entry point.

## Top-level commands (no subgroup)

```
hf download <repo_id> [filenames...]    # download files from a repo
hf upload <repo_id> <local_path>        # upload files/folder to a repo
hf upload-large-folder <repo_id> <dir>  # chunked upload for huge folders
hf sync <bucket_id> <local_dir>         # sync with a storage bucket
hf env                                  # print environment info
hf update                               # check for huggingface_hub updates
hf version                              # print version
```

## `hf auth` — Authentication

```
hf auth login              # interactive login (prompt for token)
hf auth login --token $HF_TOKEN --add-to-git-credential
hf auth logout             # remove token from machine
hf auth whoami             # show current user/org
hf auth token              # print raw token (for piping to curl etc.)
hf auth list | ls          # list all stored tokens
hf auth switch <name>      # switch active token
```

## `hf repos` (alias `hf repo`) — Repository CRUD

```
hf repos list | ls         # list your repos (or --namespace)
hf repos create            # create a new repo
hf repos delete            # delete a repo
hf repos duplicate         # fork/duplicate a repo
hf repos move              # rename/move a repo
hf repos settings          # update repo settings
hf repos delete-files      # delete specific files from a repo

hf repos branch create     # create a branch
hf repos branch delete     # delete a branch

hf repos tag create        # create a tag
hf repos tag list | ls     # list tags
hf repos tag delete        # delete a tag
```

## `hf models` — Browse Models

```
hf models list | ls        # search/list models
hf models info             # model metadata
hf models card             # show model card (README)
```

## `hf datasets` — Browse Datasets

```
hf datasets list | ls      # search/list datasets
hf datasets info           # dataset metadata
hf datasets card           # show dataset card
hf datasets leaderboard    # dataset leaderboard
hf datasets parquet        # show parquet info
hf datasets sql            # query dataset with SQL
```

## `hf spaces` — Spaces (hosted Gradio/Streamlit apps)

```
hf spaces list | ls        # list spaces
hf spaces info             # space metadata/status
hf spaces card             # show space card
hf spaces search           # search spaces
hf spaces ssh              # SSH into a running space
hf spaces pause            # pause a space
hf spaces restart          # restart a space
hf spaces hardware         # get/set hardware (CPU/GPU/TPU)
hf spaces settings         # update space settings
hf spaces logs             # tail space logs
hf spaces hot-reload       # live-reload during dev

hf spaces volumes list | ls    # list persistent volumes
hf spaces volumes set          # attach a volume
hf spaces volumes delete       # detach a volume

hf spaces secrets list | ls    # list space secrets
hf spaces secrets add          # add a secret
hf spaces secrets delete       # delete a secret

hf spaces variables list | ls  # list space variables
hf spaces variables add        # add a variable
hf spaces variables delete     # delete a variable
```

## `hf jobs` — Training Jobs (HF Inference/Training)

```
hf jobs run                # launch a training job
hf jobs uv run             # launch via uv (auto-build from pyproject.toml)
hf jobs logs               # tail job logs
hf jobs stats              # job resource stats
hf jobs ps                 # list running jobs
hf jobs hardware           # list available hardware
hf jobs inspect            # inspect a job
hf jobs cancel             # cancel a job
hf jobs labels             # manage job labels

hf jobs scheduled ...      # scheduled/recurring jobs
  ps | inspect | delete | suspend | resume
hf jobs scheduled uv ...   # scheduled uv jobs
```

## `hf endpoints` — Inference Endpoints

```
hf endpoints list | ls         # list endpoints
hf endpoints deploy            # deploy a new endpoint
hf endpoints describe          # endpoint details
hf endpoints update            # scale/configure
hf endpoints delete            # delete
hf endpoints pause             # pause
hf endpoints resume            # resume
hf endpoints scale-to-zero     # scale to zero (save cost)
hf endpoints catalog           # list available instance types
```

## `hf buckets` — Storage Buckets (S3-like)

```
hf buckets create          # create a storage bucket
hf buckets list | ls       # list buckets
hf buckets info            # bucket details
hf buckets delete          # delete a bucket
hf buckets sync            # sync local dir ↔ bucket
```

## `hf cache` — Local Cache Management

```
hf cache list | ls         # scan & list cached repos
hf cache delete            # delete specific cached repos
hf cache prune             # remove old/orphaned cache entries
```

## `hf collections` — Curated Collections

```
hf collections list | ls       # list collections
hf collections info            # collection details
hf collections create          # create a collection
hf collections update          # update metadata
hf collections delete          # delete
hf collections add-item        # add a repo to collection
hf collections update-item     # update an item
hf collections delete-item     # remove an item
```

## `hf discussions` — PRs & Discussions

```
hf discussions list | ls       # list discussions/PRs for a repo
hf discussions info            # discussion details
hf discussions create          # open a discussion
hf discussions comment         # add a comment
hf discussions close           # close
hf discussions rename          # rename
hf discussions merge           # merge a PR
```

## `hf webhooks` — Webhook Management

```
hf webhooks list | ls      # list webhooks
hf webhooks info           # webhook details
hf webhooks create         # create a webhook
hf webhooks update         # update
hf webhooks enable         # enable
hf webhooks disable        # disable
hf webhooks delete         # delete
```

## `hf papers` — Academic Papers

```
hf papers list | ls        # list trending papers
hf papers search           # search papers
hf papers info             # paper details
hf papers read             # read paper content
```

## `hf skills` — AI Agent Skills Marketplace

```
hf skills list | ls        # list installed skills
hf skills preview          # preview a skill
hf skills add              # install a skill
hf skills update           # update installed skills
```

## `hf extensions` (alias `hf ext`) — CLI Extensions

```
hf ext ...                 # user-installed CLI extensions
```

## Python API (HfApi class)

The CLI is a thin wrapper around `HfApi` in `hf_api.py` (~11k lines). The main methods you'd use programmatically:

```python
from huggingface_hub import HfApi
api = HfApi()

# Auth
api.whoami()                           # current user info
api.get_token_permission()             # token role

# Repos
api.list_repos()                       # list repos
api.create_repo()                      # create
api.delete_repo()                      # delete
api.duplicate_repo()                   # fork
api.rename_repo()                      # move

# Files
api.upload_file()                      # upload single file
api.upload_folder()                    # upload folder
api.upload_large_folder()              # chunked upload for huge dirs
api.hf_hub_download()                  # download single file
api.snapshot_download()                # download entire repo
api.list_repo_files()                  # list files in repo
api.delete_files()                     # delete files
api.repo_info()                        # repo metadata

# Branches/Tags
api.create_branch() / api.delete_branch()
api.create_tag() / api.delete_tag() / api.list_repo_refs()

# Models
api.list_models()                      # search models
api.model_info()                       # model metadata

# Datasets
api.list_datasets()                    # search datasets
api.dataset_info()                     # dataset metadata

# Spaces
api.list_spaces()                      # search spaces
api.space_info()                       # space metadata
api.restart_space() / api.pause_space()
api.set_space_hardware()
api.add_space_secret() / api.delete_space_secret()

# Discussions/PRs
api.get_repo_discussions()
api.create_discussion()

# Inference
api.list_inference_endpoints()
api.create_inference_endpoint()
api.get_inference_endpoint()

# Collections
api.list_collections() / api.get_collection()
api.create_collection() / api.delete_collection()

# Jobs
api.list_jobs() / api.create_job()
```

The pattern is always: **CLI command → `hf_api.py` method → HF REST API**. The CLI adds output formatting (tables/JSON), interactive prompts, and error handling on top.