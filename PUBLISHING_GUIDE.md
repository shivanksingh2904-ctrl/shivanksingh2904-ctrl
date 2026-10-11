# Fixing and publishing your GitHub profile visuals

## Why images may not show
GitHub READMEs render best when assets are committed to the same repository and linked by relative paths. This package uses:
- `assets/profile-banner.svg` — local animated banner
- `assets/tech-stack.svg` — local skills graphic
- `assets/activity-graph.svg` — local chart placeholder, replaced by the workflow

External cards such as GitHub stats and profile views still rely on third-party services. If they fail, the rest of the README remains styled and readable.

## Upload these exact paths
Repository: `shivanksingh2904-ctrl/shivanksingh2904-ctrl`

```text
README.md
assets/profile-banner.svg
assets/tech-stack.svg
assets/activity-graph.svg
scripts/generate_activity_graph.py
.github/workflows/refresh-profile-visuals.yml
```

Keep the folders and filenames exactly as shown. Do not upload the files into a nested folder.

## Enable the workflow
1. Open repository **Settings → Actions → General**.
2. Under **Workflow permissions**, choose **Read and write permissions** and save.
3. Open **Actions → Refresh profile visuals**.
4. Select **Run workflow** and inspect the logs.
5. The workflow updates the activity graph and creates/updates the `output` branch with contribution-snake SVGs.

## Verify
- Visit `https://github.com/shivanksingh2904-ctrl/shivanksingh2904-ctrl` and inspect the README.
- Test the local image directly: `https://raw.githubusercontent.com/shivanksingh2904-ctrl/shivanksingh2904-ctrl/main/assets/profile-banner.svg`
- If the local image URL is a 404, it is not in the expected path or the files have not been pushed.
- The snake won't appear until the workflow successfully creates the `output` branch.

## Important limitations
- The README cannot run custom JavaScript, custom CSS, hover-driven app controls, or live embedded dashboards.
- The graph counts recent **public GitHub events** from the public events API; it is not a full contribution-calendar count.
- External GitHub stat cards can occasionally fail due to third-party outages.
- Replace any generic project links with exact source repository URLs if you have separate repos for PantryPulse and DocuMind.
