# Content Update Guide

## How to Update Content

When you make changes to any content file:

1. **Edit your content file** (e.g., `content/emergencycoachscripts.json`)

2. **Update the manifest.json**:
   - Increment the `version` number (e.g., "1.0.1" → "1.0.2")
   - Update the global `lastUpdated` timestamp
   - Update the specific file's `lastUpdated` in `contentFiles`
   - Update the checksum (or use a unique value like "sha256:v1.0.2")

Example:
```json
{
  "version": "1.0.2",
  "lastUpdated": "2025-05-26T10:00:00Z",
  "contentFiles": {
    "emergencyCoachScripts": {
      "lastUpdated": "2025-05-26T10:00:00Z",
      "checksum": "sha256:v1.0.2"
    }
  }
}
```

3. **Commit and push** both files to GitHub

4. **Test the update** in the app:
   - Go to Settings → Force Content Update Check
   - The app should detect and download the changes

## Timestamp Management

- **Only maintain timestamps in manifest.json**
- Remove `version`, `lastUpdated`, `publishedAt`, `updatedAt` from content files
- The app will use manifest timestamps for update detection

## Troubleshooting

If updates aren't detected:
1. Check that manifest.json was updated and pushed
2. Ensure timestamps are newer than the cached version
3. Use "Force Content Update Check" to clear cache
4. Check browser console for error messages