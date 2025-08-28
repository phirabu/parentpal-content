# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the ParentPal content repository containing parenting education materials in multiple languages (English, Spanish, German). The repository serves as the content backend for a parenting app, storing JSON-formatted educational content, audio files, and images.

## Key Content Types

- **Emergency Coach Scripts**: Situation-specific parenting guidance with strategies and mantras
- **Library Content**: Educational articles, videos, and comprehensive parenting resources
- **Meditations**: Audio meditation files and associated metadata
- **Daily Affirmations**: Positive messages for parents
- **Categories**: Organization structure for library content

## Working with Content

### Updating Content Files

When modifying any content file, always follow the Update Guide (docs/UPDATE_GUIDE.md):

1. Edit the content file (e.g., `content/en/emergencycoachscripts.json`)
2. Update `content/manifest.json`:
   - Increment the `version` number
   - Update the global `lastUpdated` timestamp
   - Update the specific file's entry in `contentFiles`
3. Commit both the content file and manifest.json together

### Content Converters

Use the Python converters in the `converter/` directory to transform content between JSON and Markdown formats for easier editing:

```bash
# Emergency Coach Scripts
python3 converter/coach-json-markdown-converter.py content/en/emergencycoachscripts.json scripts.md
# Edit scripts.md, then convert back
python3 converter/coach-json-markdown-converter.py scripts.md emergencycoachscripts_new.json

# Library Categories
python3 converter/library_categories_converter.py content/en/library_categories.json categories.md

# Library Content
python3 converter/library_content_converter.py content/en/library_content.json content.md
```

## Content Structure

### Multi-language Support
- Content is organized by language: `content/en/`, `content/es/`, `content/de/`
- Each language has identical file structures
- Audio files follow the same pattern: `audio/[type]/[language]/`

### Content File Formats

**Emergency Coach Scripts** (`emergencycoachscripts.json`):
- Contains scenarios with prevention tips, strategies, scripts, and mantras
- Each strategy includes difficulty level, time required, and why it works

**Library Categories** (`library_categories.json`):
- Defines content categories with colors, images, and descriptions
- Uses GitHub raw URLs for category images

**Library Content** (`library_content.json`):
- Contains topics with articles, videos, and related scripts
- Articles support full Markdown formatting
- Videos include YouTube URLs and descriptions

**Meditation Content** (`meditation_content.json`):
- Links to audio files with metadata and descriptions
- Associated category images

## Important Notes

- **Version Management**: Always use manifest.json for version tracking, not individual content files
- **Image URLs**: All images use GitHub raw URLs pointing to this repository
- **Content Archives**: Old versions are preserved in `content/archive/`
- **No Build Process**: This is a pure content repository with no build or test commands
- **Git Workflow**: Direct commits to main branch for content updates