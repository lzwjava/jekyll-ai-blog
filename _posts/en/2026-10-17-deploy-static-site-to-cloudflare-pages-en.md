---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deploy Static Site to Cloudflare Pages
translated: false
type: note
---

Question: How do you deploy a static website to Cloudflare?

Answer: Use Cloudflare Pages. For a static website, such as HTML/CSS/JS, a Jekyll blog, or a prebuilt React/Vite app, you have two main options:

- GitHub → Cloudflare Pages: Best for continuous deployment. Every push to your production branch triggers a build and deployment.
- CLI → Cloudflare Pages: Best for deploying directly from your terminal without connecting a Git repository.

Both provide a `*.pages.dev` URL, and you can connect your own domain.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages docs

+1



## Option 1: Deploy from your terminal

If you already have a static site, this is the quickest way to deploy it.

For example, suppose your built website is in `dist/`:

```
cd my-site

# Authenticate with Cloudflare
npx wrangler login

# Create the Pages project (first deployment only)
npx wrangler pages project create my-site

# Deploy your static files
npx wrangler pages deploy dist --project-name=my-site
```

Replace `dist` with your actual output directory. For a plain HTML website, it might be `.` or `public/`; for Vite, it is commonly `dist/`.

Your website will be available at:

`https://my-site.pages.dev`

Official guide: [Cloudflare Pages Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/?utm_source=chatgpt.com).&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub

+1



## Option 2: Automatic deployment from GitHub

Recommended if you actively maintain the website or blog.

1. Push your website to a GitHub repository.
2. Open the [Cloudflare Dashboard](https://dash.cloudflare.com/?utm_source=chatgpt.com).
3. Go to Workers & Pages → Create application → Pages → Import an existing Git repository.
4. Select your repository and configure the build.

Typical settings:

| Setting                | Plain HTML      | Vite            |
| ---------------------- | --------------- | --------------- |
| Production branch      | `main`          | `main`          |
| Build command          | `exit 0`        | `npm run build` |
| Build output directory | `.` or `public` | `dist`          |

For a Jekyll site, use the appropriate Ruby/Jekyll build command and the generated output directory, often `_site`.

After deployment, every push to `main` automatically publishes the updated site.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages docs

+1



## Option 3: Connect your own domain

After deployment:

1. Open your Pages project in Cloudflare.
2. Go to Custom domains.
3. Select Set up a custom domain.
4. Enter your domain and follow the DNS instructions.

For example, you could serve your site at `example.com` instead of `my-site.pages.dev`.

See [Custom domains in Cloudflare Pages](https://developers.cloudflare.com/pages/configuration/custom-domains/?utm_source=chatgpt.com).

## Which should you choose?

For your workflow, I'd use GitHub + Cloudflare Pages for production websites, because it gives you reproducible builds, version history, and automatic deployments. Use the Wrangler CLI when you want to publish generated sites from scripts or AI agents.

One important detail: choose Git integration or Direct Upload when creating the project. Cloudflare doesn't let you convert an existing Direct Upload project into a Git-integrated project; switching requires creating a new project.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages docs

+1



One question: What kind of static site are you deploying?

Plain HTML/CSS/JS

Jekyll blog

Vite / React

Next.js static export

Other

Deployment method

Terminal / CLI

GitHub automatic deployment

Dashboard upload

Show exact deployment steps
