# connect.openab.dev

Landing page for **OpenAB Connect**, the closed-source macOS client for
[`openabdev/openab-pty`](https://github.com/openabdev/openab-pty).

Static HTML, no build step. GitHub Pages serves `main`.

It lives in its own repository rather than in `openab-pty` on purpose: that
repository is MIT-licensed and states it contains no client, and putting a
closed-source product's marketing page inside it would blur what the licence
covers for anyone reading it.

`privacy.html` and `support.html` are not optional decoration — the App Store
requires a reachable privacy policy URL, and the support URL is what a reviewer
and a user are sent to.
