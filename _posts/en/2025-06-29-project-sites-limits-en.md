---
audio: false
generated: true
lang: en
layout: post
title: GitHub Pages Project Site URL Rules
translated: false
type: note
---

With GitHub Pages, you can create **Project Sites** under your personal account in addition to your User Site (`username.github.io`). However, the format of the URL for Project Sites is limited to specific patterns, and not all subdomain or subpath configurations are natively supported. Let’s address your question about whether you can use `username.github.io/project1` or `project1.username.github.io` for Project Sites.

### Key Points

- **User Site**: A single repository named `username.github.io` serves content at `https://username.github.io`.
- **Project Sites**: Any other repository in your personal account can be configured as a Project Site, served at `https://username.github.io/repository-name` (a subpath, not a subdomain).
- **Subdomain Limitation**: GitHub Pages does not natively support subdomains like `project1.username.github.io` under the `github.io` domain. The `github.io` domain is managed by GitHub, and only `username.github.io` (for users) or `organization.github.io` (for organizations) are supported as top-level subdomains. Custom subdomains like `project1.username.github.io` require a custom domain and DNS configuration.

### Can You Use `username.github.io/project1`?

**Yes**, you can use `username.github.io/project1` for a Project Site. This is the standard way GitHub Pages handles Project Sites:

- Create a repository in your personal account (e.g., `username/project1`).
- Enable GitHub Pages for that repository:
  - Go to the repository’s **Settings** tab.
  - Scroll to the **Pages** section.
  - Under **Source**, select the branch to publish (e.g., `main` or `gh-pages`) and save.
- Once configured, the site will be accessible at `https://username.github.io/project1`.
- You can create multiple Project Sites (e.g., `username.github.io/project2`, `username.github.io/project3`) by enabling GitHub Pages on additional repositories (`username/project2`, `username/project3`, etc.).
- **Content**: Add an `index.html` or use a static site generator like Jekyll in the publishing branch of each repository.

### Can You Use `project1.username.github.io`?

**No**, GitHub Pages does not support subdomains like `project1.username.github.io` natively under the `github.io` domain. The `github.io` domain only allows:

- `username.github.io` for User Sites.
- `organization.github.io` for Organization Sites.
- Subpaths like `username.github.io/repository-name` for Project Sites.

To achieve a URL like `project1.username.github.io`, you would need:

1. **A Custom Domain**: Purchase a domain (e.g., `example.com`) from a registrar like Namecheap or GoDaddy.
2. **DNS Configuration**: Set up a CNAME record to point a subdomain (e.g., `project1.example.com`) to your GitHub Pages site (e.g., `username.github.io` or `username.github.io/project1`).
3. **GitHub Pages Settings**:
   - In the repository’s **Pages** settings, configure the custom domain (e.g., `project1.example.com`).
   - Optionally, enable “Enforce HTTPS” for security.
4. **Outcome**: You can map `project1.example.com` to the content of the `project1` repository, but not `project1.username.github.io`, as GitHub controls the `github.io` domain and doesn’t allow custom subdomains under it.

### Example Setup for `username.github.io/project1`

1. Create a repository named `project1` under your account (`username/project1`).
2. Add content (e.g., `index.html`):

   ```bash
   git clone https://github.com/username/project1
   cd project1
   echo "Hello from Project 1" > index.html
   git add --all
   git commit -m "Initial commit"
   git push origin main
   ```

3. Enable GitHub Pages:
   - Go to `username/project1` → **Settings** → **Pages**.
   - Set the source to `main` (or another branch) and save.
4. Visit `https://username.github.io/project1` to see the site live (may take a few minutes to propagate).

### Example for Custom Subdomain with a Custom Domain

If you want `project1.example.com`:

1. Own a domain (e.g., `example.com`).
2. In your DNS provider’s settings, add a CNAME record:
   - Name: `project1`
   - Value: `username.github.io`
3. In the `project1` repository’s **Pages** settings, set the custom domain to `project1.example.com`.
4. Push content to the `project1` repository, and it will be served at `project1.example.com`.

### Limitations

- **Subpaths Only for `github.io`**: Without a custom domain, Project Sites are always served as subpaths (`username.github.io/project1`), not subdomains (`project1.username.github.io`).
- **One User Site**: Your `username.github.io` repository is reserved for your User Site. Project Sites use other repositories and appear as subpaths.
- **Custom Subdomains Require Custom Domain**: To get `project1.something`, you need to own `something` (e.g., `example.com`) and configure DNS.
- **Private Repositories**: Project Sites in private repositories require GitHub Pro, Team, or Enterprise. For free accounts, repositories must be public.

### Summary

- **Use `username.github.io/project1`**: Yes, this is supported natively by creating a repository (`username/project1`) and enabling GitHub Pages. You can create multiple Project Sites this way (e.g., `username.github.io/project2`, etc.).
- **Use `project1.username.github.io`**: No, this is not supported under `github.io`. You’d need a custom domain (e.g., `project1.example.com`) and DNS setup to achieve a similar effect.
- **Multiple Subdomains**: To get multiple `*.github.io` subdomains, create GitHub organizations (as discussed previously) for `org1.github.io`, `org2.github.io`, etc., or use a custom domain for subdomains like `project1.example.com`.

If you need help setting up a specific Project Site, configuring a custom domain, or managing multiple sites, let me know!
