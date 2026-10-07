/**
 * WhatConverts webhook -> GitHub Actions relay.
 *
 * WhatConverts fires this when a phone-call lead is modified, which is what a
 * rep marking a call quotable looks like. The relay's only job is to start the
 * sync workflow; GitHub's schedule delivers roughly 15% of its slots, so waiting
 * for the next one costs about three hours.
 *
 * It deliberately ignores the request body. WhatConverts cannot sign or
 * authenticate its webhooks, so nothing in the payload can be trusted -- the
 * POST is treated purely as "something changed, go look". The sync then reads
 * the WhatConverts API itself and applies the same checks it always has. The
 * worst a forged request can do is start a run that finds nothing, because the
 * sync is idempotent.
 *
 * Deploy: see README.md in this directory.
 */

const OWNER = "mpocockch";
const REPO = "ch-content";
const WORKFLOW = "whatconverts-hubspot-sync.yml";
const REF = "claude/blog-automation-process-flbewl";  // the repo's default branch

export default {
  async fetch(request, env) {
    // The secret lives in the path because WhatConverts cannot send headers.
    // This is a bearer token in a URL, not real authentication: it keeps random
    // internet traffic out, and the idempotent sync covers the rest.
    const url = new URL(request.url);
    if (url.pathname !== `/${env.RELAY_PATH}`) {
      return new Response("Not found", { status: 404 });
    }
    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }

    const response = await fetch(
      `https://api.github.com/repos/${OWNER}/${REPO}/actions/workflows/${WORKFLOW}/dispatches`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${env.GITHUB_TOKEN}`,
          Accept: "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28",
          "User-Agent": "whatconverts-hubspot-relay",
          "Content-Type": "application/json",
        },
        // dry_run must be explicit: the workflow input defaults to true, so
        // omitting it would start a rehearsal that writes nothing.
        body: JSON.stringify({ ref: REF, inputs: { dry_run: "false" } }),
      },
    );

    if (response.status === 204) {
      return new Response("dispatched", { status: 200 });
    }

    // Return 200 regardless. WhatConverts may retry or disable a webhook that
    // keeps erroring, and a failed dispatch is not worth losing the hook over --
    // the scheduled sweep still catches the lead. The body records what happened
    // for whoever reads the Cloudflare log.
    const detail = await response.text();
    console.log(`dispatch failed: ${response.status} ${detail.slice(0, 300)}`);
    return new Response(`dispatch failed: ${response.status}`, { status: 200 });
  },
};
