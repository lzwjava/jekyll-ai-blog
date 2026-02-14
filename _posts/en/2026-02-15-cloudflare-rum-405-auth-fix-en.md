---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Cloudflare RUM 405 Authentication Error
translated: false
type: note
---

**Question:** What does this error mean and how to fix it when trying to fetch RUM sites: Exit code 1, Error fetching RUM sites: 405 {"success":false,"errors":[{"code":10405,"message":"Method not allowed for this authentication scheme"}],"messages":[],"result":null}, No Web Analytics sites found?

**Answer:**

This error occurs when making an API request to a Cloudflare endpoint (in this case, likely one of the RUM/Web Analytics management endpoints like `/accounts/{account_id}/rum/site_info`) using an **API Token** with authentication headers that are incompatible with the HTTP method used.

The key part is:  
**"Method not allowed for this authentication scheme" (code 10405)**  
This is a Cloudflare-specific error indicating that the authentication method (how you're sending the credentials) does not support the HTTP method of your request (e.g., GET, POST, DELETE, PATCH).

### Common Causes
1. Using **API Token** authentication (via `Authorization: Bearer <token>`) but the endpoint or method does not fully support it for certain operations.  
   Older or specific endpoints (including some RUM/Web Analytics ones) historically had better/more consistent support with the **Global API Key** (via `X-Auth-Email` + `X-Auth-Key` headers) rather than scoped API Tokens.

2. Using the wrong HTTP method for the endpoint.  
   - List sites: Must be **GET**  
   - Create site: **POST**  
   - Delete/Update: **DELETE** / **PATCH** / **PUT**  
   If you accidentally used POST for listing, or GET for creation, you'd get 405.

3. The token lacks the necessary **Edit** permission (though this usually gives 403 Forbidden or 10000 auth error, not specifically 10405).

4. In rare cases: The endpoint itself has restrictions on token auth for non-GET methods (seen in community reports for PATCH/PUT/DELETE on various APIs).

### How to Fix It (Step-by-Step)
1. **Verify you're using the correct HTTP method**  
   For listing Web Analytics sites (most common starting point):  
   - Endpoint: `GET https://api.cloudflare.com/client/v4/accounts/{account_id}/rum/site_info`  
   - Do **not** use POST/PATCH/etc. for listing.

2. **Switch to Global API Key authentication** (most reliable fix for this exact error on RUM-related endpoints)  
   - Go to Cloudflare Dashboard → **My Profile** → **API Tokens** tab → Scroll to **Global API Key** section → View / Generate if needed.  
   - Use these headers in your request (instead of Bearer token):  
     ```
     X-Auth-Email: your@email.com
     X-Auth-Key: YOUR_GLOBAL_API_KEY_HERE
     ```
   - Example curl to list sites:  
     ```bash
     curl -X GET "https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/rum/site_info" \
     -H "X-Auth-Email: your@email.com" \
     -H "X-Auth-Key: YOUR_GLOBAL_API_KEY_HERE" \
     -H "Content-Type: application/json"
     ```
   - This often resolves the "authentication scheme" mismatch for older/legacy-style endpoints.

3. **If you must use an API Token (Bearer auth)**  
   - Ensure the token has **Account → Web Analytics: Edit** permission.  
   - Double-check you're using **GET** for listing.  
   - Test a simple GET first. Some users report that non-GET methods (POST/DELETE/PATCH) on RUM endpoints still throw this 10405 error even with correct permissions when using Bearer — fallback to Global Key in those cases.  
   - Regenerate the token and re-test.

4. **Other Checks**  
   - Confirm your **Account ID** is correct (find it in dashboard → Overview sidebar).  
   - If no sites exist yet → the result will be empty array, but success:true (not this error).  
   - Use tools like Postman or curl with `-v` to see full response headers (look for `Allow:` header which lists permitted methods).

In summary: The quickest fix is usually **switching to Global API Key + X-Auth-* headers** instead of Bearer token, especially for RUM/Web Analytics management calls. This avoids the authentication scheme restriction seen with some methods/endpoints.

**References:**

- [Cloudflare Community - PATCH method not allowed for the api_token authentication scheme](https://community.cloudflare.com/t/patch-method-not-allowed-for-the-api-token-authentication-scheme/505411)
- [Cloudflare Community - PUT method not allowed for the api_token authentication scheme](https://community.cloudflare.com/t/put-method-not-allowed-for-the-api-token-authentication-scheme/381292)
- [Cloudflare API Authentication - Headers reference](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
- [Cloudflare Community - 405 response in RUM Rules API (similar auth scheme issue)](https://community.cloudflare.com/t/405-response-in-rum-rules-api/876646)