---
audio: false
generated: true
image: false
lang: en
layout: post
title: Google Cloud CLI Update
translated: false
type: note
---

% gcloud components update
Beginning update. This process may take several minutes.


Your current Google Cloud CLI version is: 507.0.0
You will be upgraded to version: 532.0.0

┌─────────────────────────────────────────────────────────────────────────────┐
│                      These components will be updated.                      │
├─────────────────────────────────────────────────────┬────────────┬──────────┤
│                         Name                        │  Version   │   Size   │
├─────────────────────────────────────────────────────┼────────────┼──────────┤
│ BigQuery Command Line Tool                          │     2.1.21 │  1.8 MiB │
│ BigQuery Command Line Tool (Platform Specific)      │     2.1.17 │  < 1 MiB │
│ Cloud Storage Command Line Tool                     │       5.35 │ 12.4 MiB │
│ Cloud Storage Command Line Tool (Platform Specific) │       5.34 │  < 1 MiB │
│ Google Cloud CLI Core Libraries                     │ 2025.07.25 │ 22.1 MiB │
│ Google Cloud CLI Core Libraries (Platform Specific) │ 2025.05.23 │  < 1 MiB │
│ Google Cloud CRC32C Hash Tool (Platform Specific)   │      1.0.0 │  1.4 MiB │
│ gcloud cli dependencies                             │ 2025.04.18 │ 16.1 MiB │
└─────────────────────────────────────────────────────┴────────────┴──────────┘

A lot has changed since your last upgrade.  For the latest full release notes,
please visit:
  https://cloud.google.com/sdk/release_notes

Once started, canceling this operation may leave your SDK installation in an inconsistent state.

Do you want to continue (Y/n)?  Y

Performing in place update...

╔════════════════════════════════════════════════════════════╗
╠═ Downloading: BigQuery Command Line Tool                  ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Downloading: BigQuery Command Line Tool (Platform Spe... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Downloading: Cloud Storage Command Line Tool             ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Downloading: Cloud Storage Command Line Tool (Platfor... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Downloading: Google Cloud CLI Core Libraries             ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Downloading: Google Cloud CLI Core Libraries (Platfor... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Downloading: Google Cloud CRC32C Hash Tool (Platform ... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Downloading: gcloud cli dependencies                     ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Uninstalling: BigQuery Command Line Tool                 ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Uninstalling: BigQuery Command Line Tool (Platform Sp... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Uninstalling: Cloud Storage Command Line Tool            ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Uninstalling: Cloud Storage Command Line Tool (Platfo... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Uninstalling: Google Cloud CLI Core Libraries            ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Uninstalling: Google Cloud CLI Core Libraries (Platfo... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Uninstalling: Google Cloud CRC32C Hash Tool (Platform... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Uninstalling: gcloud cli dependencies                    ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Installing: BigQuery Command Line Tool                   ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Installing: BigQuery Command Line Tool (Platform Spec... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Installing: Cloud Storage Command Line Tool              ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Installing: Cloud Storage Command Line Tool (Platform... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Installing: Google Cloud CLI Core Libraries              ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Installing: Google Cloud CLI Core Libraries (Platform... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Installing: Google Cloud CRC32C Hash Tool (Platform S... ═╣
╠════════════════════════════════════════════════════════════╣
╠═ Installing: gcloud cli dependencies                      ═╣
╚════════════════════════════════════════════════════════════╝

Performing post processing steps...done.

Update done!

To revert your CLI to the previously installed version, you may run:
  $ gcloud components update --version 507.0.0
