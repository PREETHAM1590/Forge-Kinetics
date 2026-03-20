# Stitch export helper

This workspace session could not directly download Stitch pages due terminal/network policy restrictions (`curl` and `Invoke-WebRequest` are blocked here), and the embedded browser tools cannot access page DOM content without enabling `workbench.browser.enableChatTools`.

## Included files
- `screens.csv`: mapping of screen names, ids, and URLs
- `download-with-curl.ps1`: bulk downloader script using `curl -L`

## Run locally (outside restricted session)
From `d:\FORGE\stitch-downloads`:

```powershell
powershell -ExecutionPolicy Bypass -File .\download-with-curl.ps1
```

## Notes
- If Stitch requires auth, run while logged in to Stitch in the same environment where `curl` has access to cookies/session or use Stitch's export/share links.
- After pages are downloaded, provide those files and I can parse/extract code blocks and image links automatically.
