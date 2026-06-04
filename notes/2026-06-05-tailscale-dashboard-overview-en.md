---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tailscale Dashboard Overview
translated: false
type: note
---

**Question:** What do each of the Tailscale admin panel sections do?

**Answer:**

Tailscale's admin dashboard is organized around three layers: **network visibility** (Machines, Users, Services), **access policy** (ACLs, Apps), **operational management** (Logs, DNS, Settings), and **billing**.

## Main Navigation

**Machines**
Lists all connected devices (your MacBook Air, workstation at 192.168.1.36, etc.). Shows IP addresses in the Tailnet, connection status, OS, last seen. You can authorize/deauthorize devices, tag them for access control, and force key rotation here.

**Apps**
Tailscale Apps (beta/early access feature). Allows you to expose HTTP applications through your Tailnet without manual port forwarding. You define which apps on which machines should be accessible, and Tailscale handles DNS routing through `app.tailnet-name.ts.net` domains.

**Services**
Services like SSH, HTTPS, or custom services you expose through your Tailnet. Complements Apps for non-HTTP protocols. Useful for advertising services that multiple machines need to discover.

**Users**
Team members with access to your Tailnet. Shows email, last login, MFA status. You manage invites, remove users, and control who can add devices here.

**Access controls (ACLs)**
The firewall rules of your Tailnet. Written in HCL (HashiCorp Configuration Language), these define **who can connect to what**. Examples:

```hcl
{
  "acls": [
    {
      "action": "accept",
      "src": ["tag:engineers"],
      "dst": ["tag:servers:*"]
    },
    {
      "action": "accept",
      "src": ["user:you@example.com"],
      "dst": ["tag:personal:*"]
    }
  ]
}
```

Uses tags (assigned to machines) and users for policy. Critical for zero-trust networking.

**Logs**
Audit trail of Tailnet activity — who accessed what, auth events, device registrations, ACL changes. Invaluable for debugging connectivity issues or security audits.

**DNS**
Custom DNS records for your Tailnet. You can define `internal-service.tailnet-name.ts.net` → machine IP mappings, or use Tailscale's MagicDNS (auto-resolves machine names). Also shows global nameservers.

**Settings → Tailnet Settings**
Cluster-wide configuration:

- **General**: Tailnet name (auto-generated), sharing settings, device approval policy (auto-approve or manual), OIDC/OAuth provider setup
- **User management**: SSO/SAML configuration, role-based access control (RBAC), who can add devices
- **Device management**: Auto-update policy, device expiration, subnet routing rules, exit nodes (which machines act as gateways out of the Tailnet)
- **Policy file management**: Git integration for ACLs — version-control your access rules
- **Trust credentials**: Certificate-based device auth, API keys for Tailscale API calls
- **Webhooks**: Trigger external systems on Tailnet events (device added, user removed, etc.)
- **Contact preferences**: Email notifications
- **Billing**: Plan, seat limits, usage

**Settings → Personal Settings**
Your account level:

- **Keys**: Generate **Auth keys** (for CI/CD, headless device provisioning) and **API keys** (for scripting Tailscale API). Critical for automation.

## Practical Use Cases

**Your setup (MacBook Air + workstation):**

- Machines: Both should appear here
- ACLs: Tag workstation as `tag:gpu`, restrict GPU tasks to your user
- DNS: Add `gpu.local` → workstation IP
- Keys: Generate auth key for headless AMD Dev Cloud instance to auto-join Tailnet

**Example ACL for your workflow:**

```hcl
{
  "acls": [
    {
      "action": "accept",
      "src": ["autogroup:self"],
      "dst": ["autogroup:self:*"]
    },
    {
      "action": "accept",
      "src": ["tag:dev"],
      "dst": ["tag:gpu:*"]
    }
  ]
}
```

**For CLI automation (ww, iclaw, zz):**
Generate an Auth key in **Settings → Personal Settings → Keys**, then:

```bash
tailscale up --authkey=<KEY> --hostname=automation-box
```

Your free plan: 6 users, 50 tagged resources, unlimited devices. Plenty for a solo engineer + compute cluster.
