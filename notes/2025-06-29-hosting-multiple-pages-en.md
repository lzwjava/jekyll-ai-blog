---
audio: false
generated: true
lang: en
layout: post
title: Host Multiple GitHub Pages with Organizations
translated: false
type: note
---

Yes, creating a GitHub organization is a viable way to host additional GitHub Pages sites with unique `*.github.io` subdomains, as each organization can have its own `organization.github.io` site, separate from your personal `username.github.io` site. Here's how you can do it and what you need to know:

### Key Points

- **Personal Account Limitation**: Each GitHub user account can have only one User Site, hosted at `username.github.io`, which is tied to a repository named `username.github.io`. If you've already used this for your personal account, you can't create another `*.github.io` subdomain under the same account.
- **Organization Sites**: Each GitHub organization can also have its own Organization Site, hosted at `organization.github.io`, by creating a repository named `organization.github.io`. This allows you to create additional `*.github.io` subdomains by setting up multiple organizations.
- **Project Sites**: Both user and organization accounts can host multiple Project Sites (e.g., `username.github.io/project` or `organization.github.io/project`) from other repositories, but these are subpaths, not subdomains. If you specifically want distinct subdomains (e.g., `sub.example.github.io`), you cannot achieve this directly with GitHub Pages without a custom domain, as GitHub does not support custom subdomains like `sub.example.github.io` under the `github.io` domain.[](https://github.com/orgs/community/discussions/54144)

### Steps to Create a GitHub Organization for Additional `*.github.io` Subdomains

1. **Create a GitHub Organization**:
   - Go to GitHub and sign in with your account.
   - Click the "+" icon in the top-right corner and select **New organization**.
   - Follow the prompts to set up the organization, choosing a unique name (e.g., `myorg`). This name will determine the subdomain (e.g., `myorg.github.io`).
   - Note: Organizations can be created for free, but some features (like private repositories) may require a paid plan, depending on your needs. GitHub Pages for public repositories is available with GitHub Free.[](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

2. **Create the Organization's GitHub Pages Repository**:
   - In the new organization, create a repository named exactly `myorg.github.io` (replace `myorg` with your organization’s name).
   - This repository will host the Organization Site, accessible at `https://myorg.github.io`.

3. **Set Up GitHub Pages**:
   - Go to the `myorg.github.io` repository’s **Settings** tab.
   - Scroll to the **Pages** section.
   - Under **Source**, select the branch you want to publish (e.g., `main` or `gh-pages`) and save.
   - Once configured, the site will be live at `https://myorg.github.io` after a few minutes.[](https://dev.to/mohammedasker/how-to-get-github-subdomain-with-github-pages-4g0p)

4. **Add Content**:
   - Add an `index.html` file or use a static site generator like Jekyll to the repository’s publishing branch.
   - Commit and push your changes. For example:

     ```bash
     git clone https://github.com/myorg/myorg.github.io
     cd myorg.github.io
     echo "Hello World" > index.html
     git add --all
     git commit -m "Initial commit"
     git push origin main
     ```

   - Visit `https://myorg.github.io` to verify the site is live.[](https://dev.to/mohammedasker/how-to-get-github-subdomain-with-github-pages-4g0p)

5. **Repeat for Additional Subdomains**:
   - Create additional organizations (e.g., `myorg2`, `myorg3`) and repeat the process to get `myorg2.github.io`, `myorg3.github.io`, etc.
   - Each organization can have one `*.github.io` subdomain, allowing you to create as many subdomains as you have organizations.

### Limitations and Considerations

- **Custom Subdomains on `github.io`**: You cannot create subdomains like `sub.myorg.github.io` directly with GitHub Pages. The `github.io` domain is managed by GitHub, and only `username.github.io` or `organization.github.io` are supported. To use custom subdomains (e.g., `blog.example.com`), you must own a custom domain and configure DNS settings (CNAME records) to point to `myorg.github.io`.[](https://github.com/orgs/community/discussions/54144)[](https://github.com/orgs/community/discussions/64133)
- **Single Repository per Subdomain**: Each `*.github.io` subdomain is tied to a single repository (`username.github.io` or `organization.github.io`). You cannot serve multiple subdomains from a single repository without a custom domain and additional hosting or proxying services.[](https://webmasters.stackexchange.com/questions/144484/separate-subdomains-on-one-github-page)
- **Management Overhead**: Each organization requires separate management (e.g., members, permissions, billing). Ensure you’re comfortable managing multiple organizations.
- **DNS and Custom Domains**: If you want to use a custom domain (e.g., `example.com` or `sub.example.com`) instead of `*.github.io`, you can configure it in the repository’s **Pages** settings and add a CNAME record with your DNS provider. For example, point `sub.example.com` to `myorg.github.io`. Be sure to verify the domain to prevent takeover risks.[](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)[](https://dev.to/scc33/how-to-host-a-site-with-a-subdomain-on-github-pages-5a1j)
- **Private Repositories**: GitHub Pages for private repositories requires GitHub Pro, Team, or Enterprise plans. If you’re using free plans, ensure your `myorg.github.io` repository is public.[](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

### Alternative for Multiple Subdomains

If your goal is to have multiple subdomains (e.g., `blog.example.com`, `shop.example.com`) under a single custom domain, you can:

1. Purchase a custom domain (e.g., `example.com`) from a registrar like Namecheap or GoDaddy.
2. Create multiple repositories in your organization (e.g., `myorg/blog`, `myorg/shop`).
3. Enable GitHub Pages for each repository, setting custom domains like `blog.example.com` and `shop.example.com` in their respective **Pages** settings.
4. Configure CNAME records with your DNS provider to point `blog.example.com` to `myorg.github.io` and `shop.example.com` to `myorg.github.io`. Note that all repositories without their own custom domain will appear under the organization’s custom domain as subpaths (e.g., `example.com/blog`).[](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)[](https://stackoverflow.com/questions/68505452/github-pages-with-single-custom-subdomain-for-multiple-repositories-using-paths)
5. Be aware that serving multiple subdomains from a single repository is not natively supported by GitHub Pages and may require external services like a CDN or reverse proxy.[](https://webmasters.stackexchange.com/questions/144484/separate-subdomains-on-one-github-page)

### Example Scenario

- You’ve used `username.github.io` for your personal site.
- Create an organization named `myorg` and a repository `myorg.github.io` to get `myorg.github.io`.
- Create another organization named `myorg2` and a repository `myorg2.github.io` to get `myorg2.github.io`.
- For custom subdomains, own `example.com`, and set up `blog.example.com` (pointing to `myorg.github.io`) and `shop.example.com` (pointing to `myorg2.github.io`) via CNAME records.

### Final Notes

- Creating multiple organizations is a straightforward way to get additional `*.github.io` subdomains without needing a custom domain.
- If you want true subdomains (e.g., `sub.myorg.github.io`), you’ll need a custom domain and DNS configuration, as GitHub’s `github.io` doesn’t support this natively.
- Always verify custom domains to avoid security risks like domain takeovers.[](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- DNS changes can take up to 24 hours to propagate.[](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)

If you have further questions or need help with specific configurations, let me know!
