---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cached Authentication Accelerates HTTPS
translated: false
type: note
---

OK here's the deep answer from the source code.

The claim "HTTPS + GCM is faster than SSH" isn't about protocol speed at the wire level. It's about the **credential caching architecture** that GCM implements. Let me trace through the actual code path.

HTTPS + GCM credential flow (from the code):

  1. Git needs credentials → spawns `git-credential-manager get`
  2. GCM reads stdin key=value pairs (protocol=https, host=github.com, ...)
  3. HostProviderRegistry selects provider by priority:
       GitHub → GitLab → Bitbucket → AzureDevOps (Normal)
       Generic (Low — fallback)
  4. Provider calls GetCredentialAsync(input)
  5. THE FAST PATH — look at GitHubHostProvider.cs line 175-176:

       credential = _context.CredentialStore.Get(service, userName);

     And GenericHostProvider.cs line 73:

       ICredential credential = _context.CredentialStore.Get(service, input.UserName);

     This is a LOCAL OS call — macOS Keychain, Windows Credential Manager, or
     Linux libsecret. Zero network. Returns in microseconds.

  6. Credential found → write username/password to stdout → Git uses it.
     GCM process exits.

The critical insight: **GCM only does the expensive OAuth/browser/device-code flow ONCE** (in GenerateCredentialAsync). After that, the token/PAT is cached in the OS credential store and every subsequent `git push`/`pull`/`fetch` hits the fast path (step 5).

Compare the network paths:

  SSH:  git → ssh → ssh-agent → TCP → ncat → SOCKS5 → mihomo → internet
        (Every single operation: key exchange, agent signing, connection setup)

  HTTPS + GCM (cached):
        git → spawns git-credential-manager → Keychain.Get() → stdout
        → git uses token over HTTPS → mihomo → internet

  HTTPS + GCM (cold/first time):
        git → GCM → browser OAuth → token → Keychain.Store()
        (Slower than SSH first time, but only happens once)

Where GCM saves time:

  1. Credential retrieval: OS keychain lookup is ~0.1ms vs SSH agent
     socket round-trip + key signing (~1-5ms) on every operation.

  2. No SSH handshake overhead: SSH needs key exchange (DH), signature
     verification, and channel setup per connection. HTTPS reuses tokens
     as bearer auth headers — just an HTTP header, no crypto negotiation.

  3. Connection reuse: HTTPS connections can be HTTP/2 multiplexed.
     Each SSH session is a separate TCP connection with full handshake.

  4. Process count: GCM spawns once, reads stdin, writes stdout, exits.
     SSH requires persistent ssh-agent + ssh process + ncat tunnel.

But the real speed difference in your setup (China → GitHub through mihomo):

  The bottleneck isn't protocol overhead — it's your proxy path.
  Both SSH and HTTPS go through mihomo at 127.0.0.1:7890.

  The GCM advantage is that it caches tokens aggressively. After first
  auth, Git never needs to re-authenticate — it just sends the cached
  token as an Authorization header. SSH re-authenticates (key exchange)
  on every new connection.

  Token lifetime (from GenericHostProvider line 291-314):
  OAuth tokens have refresh tokens cached at:
    "refresh_token.{host}" service name in credential store
  So even token refresh is a local store lookup + one HTTP call,
  not a full interactive auth flow.

TL;DR: GCM makes HTTPS fast by turning authentication into a local cache
lookup after the first login. SSH has no equivalent caching — it does
cryptographic auth on every connection. The difference compounds when
your network path has high latency (like going through a Los Angeles proxy).

One caveat: if your SSH keys are in ssh-agent and you're using SSH
connection multiplexing (ControlMaster), the per-connection overhead
drops significantly. But that requires explicit configuration — GCM's
caching works out of the box.