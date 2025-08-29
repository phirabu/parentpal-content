#!/usr/bin/env python3
"""
Script to split library_content.json into individual topic files.
This creates a more maintainable structure with smaller, topic-focused files.
"""

import json
import os
from pathlib import Path
import shutil
from datetime import datetime

def load_json_file(filepath):
    """Load and parse a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath, data):
    """Save data as formatted JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Created: {filepath}")

def split_library_content(language_code):
    """Split library_content.json for a specific language into topic files."""
    print(f"\n📚 Processing {language_code.upper()} content...")
    
    # Paths
    base_dir = Path(__file__).parent / 'content' / language_code
    source_file = base_dir / 'library_content.json'
    topics_dir = base_dir / 'library_topics'
    
    # Check if source file exists
    if not source_file.exists():
        print(f"  ⚠️  Skipping {language_code}: {source_file} not found")
        return []
    
    # Load the monolithic library content
    library_data = load_json_file(source_file)
    topics = library_data.get('topics', [])
    
    print(f"  📊 Found {len(topics)} topics to split")
    
    # Create topics directory
    topics_dir.mkdir(exist_ok=True)
    
    # Split each topic into its own file
    topic_files = []
    for topic in topics:
        topic_id = topic.get('id', 'unknown')
        topic_file = f"library_topics/{topic_id}.json"
        topic_path = base_dir / 'library_topics' / f"{topic_id}.json"
        
        # Create individual topic file with just this topic's data
        topic_data = {
            "topic": topic
        }
        
        save_json_file(topic_path, topic_data)
        topic_files.append(topic_file)
        
        # Print statistics
        articles_count = len(topic.get('articles', []))
        media_count = len(topic.get('media', []))
        scripts_count = len(topic.get('scripts', []))
        print(f"    - {topic_id}: {articles_count} articles, {media_count} media, {scripts_count} scripts")
    
    return topic_files

def update_manifest(topic_files_by_language):
    """Update manifest.json with new topic-based structure."""
    print("\n📝 Updating manifest.json...")
    
    manifest_path = Path(__file__).parent / 'content' / 'manifest.json'
    
    # Load existing manifest
    manifest = load_json_file(manifest_path)
    
    # Update version
    old_version = manifest.get('version', '0.0.0')
    version_parts = old_version.split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_version = '.'.join(version_parts)
    manifest['version'] = new_version
    
    print(f"  📌 Version: {old_version} → {new_version}")
    
    # Add new topic-based entries to contentFiles
    for lang_code, topic_files in topic_files_by_language.items():
        # Keep the old monolithic entry for now (can remove later)
        old_key = f"libraryContent_{lang_code}"
        
        # Add new topic-based entry
        new_key = f"libraryTopics_{lang_code}"
        manifest['contentFiles'][new_key] = {
            "type": "multifile",
            "files": [f"content/{lang_code}/{f}" for f in topic_files],
            "required": True,
            "description": f"Library topic files for {lang_code.upper()}"
        }
        
        print(f"  ✓ Added {new_key} with {len(topic_files)} topic files")
    
    # Save updated manifest
    save_json_file(manifest_path, manifest)
    
    return new_version

def create_backup():
    """Create backup of original files before splitting."""
    print("\n💾 Creating backup...")
    
    backup_dir = Path(__file__).parent / 'backups' / datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Backup manifest and library content files
    files_to_backup = [
        'content/manifest.json',
        'content/en/library_content.json',
        'content/es/library_content.json',
        'content/de/library_content.json'
    ]
    
    for file_path in files_to_backup:
        source = Path(__file__).parent / file_path
        if source.exists():
            dest = backup_dir / file_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            print(f"  ✓ Backed up: {file_path}")
    
    print(f"  📁 Backup location: {backup_dir}")
    return backup_dir

def validate_split(language_code):
    """Validate that split topics match original content."""
    print(f"\n✅ Validating {language_code.upper()} split...")
    
    base_dir = Path(__file__).parent / 'content' / language_code
    source_file = base_dir / 'library_content.json'
    topics_dir = base_dir / 'library_topics'
    
    if not source_file.exists():
        return True  # Skip validation if no source file
    
    # Load original
    original_data = load_json_file(source_file)
    original_topics = original_data.get('topics', [])
    
    # Load all split files
    reconstructed_topics = []
    for topic_file in sorted(topics_dir.glob('*.json')):
        topic_data = load_json_file(topic_file)
        reconstructed_topics.append(topic_data['topic'])
    
    # Compare counts
    if len(original_topics) != len(reconstructed_topics):
        print(f"  ❌ Topic count mismatch: {len(original_topics)} original vs {len(reconstructed_topics)} split")
        return False
    
    # Compare article counts
    original_articles = sum(len(t.get('articles', [])) for t in original_topics)
    split_articles = sum(len(t.get('articles', [])) for t in reconstructed_topics)
    
    if original_articles != split_articles:
        print(f"  ❌ Article count mismatch: {original_articles} original vs {split_articles} split")
        return False
    
    print(f"  ✅ Validation passed: {len(reconstructed_topics)} topics, {split_articles} articles")
    return True

def main():
    """Main execution function."""
    print("🚀 Library Content Splitter")
    print("=" * 50)
    
    # Create backup first
    backup_dir = create_backup()
    
    # Process each language
    languages = ['en', 'es', 'de']
    topic_files_by_language = {}
    
    for lang_code in languages:
        topic_files = split_library_content(lang_code)
        if topic_files:
            topic_files_by_language[lang_code] = topic_files
    
    # Update manifest with new structure
    if topic_files_by_language:
        new_version = update_manifest(topic_files_by_language)
        
        # Validate all splits
        print("\n🔍 Running validation...")
        all_valid = True
        for lang_code in languages:
            if not validate_split(lang_code):
                all_valid = False
        
        if all_valid:
            print("\n✨ Success! Library content has been split into topic files.")
            print(f"📦 New manifest version: {new_version}")
            print(f"💾 Backup saved to: {backup_dir}")
            print("\n📋 Next steps:")
            print("  1. Review the new file structure in library_topics/ folders")
            print("  2. Test loading in the app with updated ContentService")
            print("  3. Commit changes to git")
            print("  4. Optionally remove old library_content.json files after app update")
        else:
            print("\n❌ Validation failed! Check the output above for details.")
            print(f"💾 Original files backed up at: {backup_dir}")
    else:
        print("\n⚠️  No content files found to split.")

if __name__ == "__main__":
    main()