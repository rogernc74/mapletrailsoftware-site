# Acadie+ Firebase browser configuration

GitHub secret-scanning alert [#1](https://github.com/rogernc74/mapletrailsoftware-site/security/secret-scanning/1) identifies the Firebase browser API key checked into the Acadie+ checkout configuration. Render will supply the key at build time. The published module must retain the same route and configuration contract so both checkout locales, Firebase sign-in and App Check keep working.

This fix covers the website repository and its build step. The browser will continue receiving the client key as part of Firebase configuration. Credential restrictions, rotation, historical Git cleanup and alert closure are separate changes.

## Verify and deploy

1. Set `ACADIE_FIREBASE_WEB_API_KEY` in the existing Render static site's build environment using **Save only**.
2. Before merging, add the following to the Render build command and preserve the publish directory. If the site already has a build command, chain this step with `&&` so any earlier failure still fails the build. The temporary check lets Render rebuild the current revision, which already includes its configuration.

   ```sh
   if [ -f scripts/configure-acadie-billing.py ]; then python3 scripts/configure-acadie-billing.py --output acadie/billing-config.js; fi
   ```

3. Merge the fix after Render is ready. Verify its deployment, both checkout pages, the generated module and a signed-in access refresh without initiating a purchase. Then use the generator directly as the build step so a missing script fails a future build.

Run `python3 scripts/check-site.py` from the repository root. Use a temporary output path outside the checkout for local generator tests. Check that missing or invalid input fails before writing and that the current browser value produces a module identical to the published configuration.

## Ownership

The Codex chat for GitHub alert #1 owns this change. The isolated managed worktree `acadie-billing-config-fix` starts from website `main` at `b152c0b519f33bfad1ec4eb2ec732b16ce08af4c`. Validation uses Python, Node and small temporary fixtures. No native build or new dependency is needed.

## Verification

The site validator passed for all 21 pages and 571 local references. The generator rejects missing and invalid values before writing, and a rerun accepts a replacement value. The module generated with the current key matches the bytes served by the live checkout. The source scan found zero Google API key literals in the candidate files.

Render build settings, GitHub merge and live checkout verification are pending Render sign-in. Keep the managed worktree for that rollout.
