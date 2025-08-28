#!/usr/bin/env python3
"""
Update library_content.json with German translations from individual MD files
Preserves JSON structure and media items while replacing text content
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

class JsonMdUpdater:
    def __init__(self):
        self.topics_dir = Path("content/de/topics")
        self.json_path = Path("content/de/library_content.json")
        self.errors = []
        
    def extract_field(self, text: str, field_name: str) -> Optional[str]:
        """Extract a field value from markdown text"""
        match = re.search(rf'\*\*{field_name}:\*\* (.+?)(?:\n|$)', text)
        return match.group(1).strip() if match else None
    
    def extract_code_field(self, text: str, field_name: str) -> Optional[str]:
        """Extract a code field value from markdown text"""
        match = re.search(rf'\*\*{field_name}:\*\* `(.+?)`', text)
        return match.group(1) if match else None
    
    def parse_article_from_md(self, block: str, title: str = None) -> Dict[str, Any]:
        """Parse an article from markdown block"""
        article = {}
        
        # Use provided title or extract from block
        if title:
            article['title'] = title
        else:
            title_match = re.search(r'^(.+?)$', block, re.MULTILINE)
            if title_match:
                article['title'] = title_match.group(1).strip()
        
        # Extract metadata
        article['id'] = self.extract_code_field(block, "ID")
        article['category'] = self.extract_field(block, "Category") or self.extract_field(block, "Kategorie")
        
        # Extract read time
        read_time = self.extract_field(block, "Read Time") or self.extract_field(block, "Lesezeit")
        if read_time:
            match = re.search(r'(\d+)', read_time)
            if match:
                article['readTime'] = int(match.group(1))
        
        article['publishedAt'] = self.extract_field(block, "Published") or self.extract_field(block, "Veröffentlicht")
        article['description'] = self.extract_field(block, "Description") or self.extract_field(block, "Beschreibung")
        
        # Extract tags
        tags_match = re.search(r'\*\*(?:Tags|Schlagwörter):\*\* (.+?)(?:\n|$)', block)
        if tags_match:
            tag_text = tags_match.group(1)
            article['tags'] = [tag.strip('`').strip() for tag in tag_text.split(', ')]
        
        # Extract content
        content_match = re.search(r'```markdown\n(.*?)\n```', block, re.DOTALL)
        if content_match:
            article['content'] = content_match.group(1)
        
        # Extract image URL if present
        article['imageUrl'] = self.extract_field(block, "Image URL") or self.extract_field(block, "Bild-URL")
        
        return article
    
    def parse_script_from_md(self, block: str, title: str = None) -> Dict[str, Any]:
        """Parse a script from markdown block"""
        script = {}
        
        # Use provided title or extract from block
        if title:
            script['title'] = title
        else:
            title_match = re.search(r'^(.+?)$', block, re.MULTILINE)
            if title_match:
                script['title'] = title_match.group(1).strip()
        
        # Extract metadata
        script['id'] = self.extract_code_field(block, "ID")
        script['scenario'] = self.extract_field(block, "Scenario") or self.extract_field(block, "Szenario")
        
        # Extract steps
        steps = []
        step_pattern = r'(\d+)\. \*\*(.+?)\*\*\n\s+> (.+?)(?=\n\d+\.|$)'
        step_matches = re.findall(step_pattern, block, re.DOTALL)
        
        for _, title, content in step_matches:
            steps.append({
                'title': title.strip(),
                'content': content.strip()
            })
        
        if steps:
            script['steps'] = steps
        
        return script
    
    def parse_topic_md(self, md_path: Path) -> Dict[str, Any]:
        """Parse a topic markdown file and extract articles and scripts"""
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            'articles': [],
            'scripts': []
        }
        
        # Extract topic metadata
        result['title'] = self.extract_field(content, "Title") or ""
        if not result['title']:
            # Try to extract from header
            title_match = re.search(r'^## 📂 (.+?)$', content, re.MULTILINE)
            if title_match:
                result['title'] = title_match.group(1)
        
        result['description'] = self.extract_field(content, "Description") or self.extract_field(content, "Beschreibung") or ""
        
        # Split content into articles and scripts sections
        sections = re.split(r'^### ', content, flags=re.MULTILINE)
        
        for section in sections:
            if section.startswith("📄 Artikel") or section.startswith("📄 Articles"):
                # Process articles
                article_blocks = re.split(r'^---+$', section, flags=re.MULTILINE)
                for block in article_blocks:
                    if "#### 📖 " in block:
                        # Extract title first
                        title_match = re.search(r'^#### 📖 (.+?)$', block, re.MULTILINE)
                        title = title_match.group(1) if title_match else None
                        # Remove the header line completely
                        block_clean = re.sub(r'^#### 📖 .+?\n', '', block, flags=re.MULTILINE)
                        article = self.parse_article_from_md(block_clean, title)
                        if article.get('id'):
                            result['articles'].append(article)
            
            elif section.startswith("📋 Scripts") or section.startswith("📋 Skripte"):
                # Process scripts
                script_blocks = re.split(r'^---+$', section, flags=re.MULTILINE)
                for block in script_blocks:
                    if "#### 📝 " in block:
                        # Extract title first
                        title_match = re.search(r'^#### 📝 (.+?)$', block, re.MULTILINE)
                        title = title_match.group(1) if title_match else None
                        # Remove the header line completely
                        block_clean = re.sub(r'^#### 📝 .+?\n', '', block, flags=re.MULTILINE)
                        script = self.parse_script_from_md(block_clean, title)
                        if script.get('id'):
                            result['scripts'].append(script)
        
        return result
    
    def update_topic_in_json(self, json_data: Dict, topic_id: str, md_data: Dict) -> bool:
        """Update a specific topic in the JSON with data from MD file"""
        # Find the topic in JSON
        topic_found = False
        for topic in json_data['topics']:
            if topic['id'] == topic_id:
                topic_found = True
                
                # Update title and description if available
                if md_data.get('title'):
                    topic['title'] = md_data['title']
                if md_data.get('description'):
                    topic['description'] = md_data['description']
                
                # Update articles
                for md_article in md_data['articles']:
                    article_id = md_article['id']
                    # Find matching article in JSON
                    for json_article in topic.get('articles', []):
                        if json_article['id'] == article_id:
                            # Update text fields only
                            if md_article.get('title'):
                                json_article['title'] = md_article['title']
                            if md_article.get('description'):
                                json_article['description'] = md_article['description']
                            if md_article.get('content'):
                                json_article['content'] = md_article['content']
                            # Keep other fields from JSON (URLs, dates, etc.)
                            break
                
                # Update scripts
                for md_script in md_data['scripts']:
                    script_id = md_script['id']
                    # Find matching script in JSON
                    for json_script in topic.get('scripts', []):
                        if json_script['id'] == script_id:
                            # Update text fields only
                            if md_script.get('title'):
                                json_script['title'] = md_script['title']
                            if md_script.get('scenario'):
                                json_script['scenario'] = md_script['scenario']
                            if md_script.get('steps'):
                                json_script['steps'] = md_script['steps']
                            break
                
                print(f"✅ Updated topic: {topic_id}")
                print(f"   - Updated {len(md_data['articles'])} articles")
                print(f"   - Updated {len(md_data['scripts'])} scripts")
                break
        
        if not topic_found:
            self.errors.append(f"Topic {topic_id} not found in JSON")
            print(f"❌ Topic not found in JSON: {topic_id}")
            return False
        
        return True
    
    def run(self):
        """Main execution function"""
        print("=== Starting JSON Update from MD Files ===\n")
        
        # Load JSON
        with open(self.json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        print(f"Loaded JSON with {len(json_data['topics'])} topics\n")
        
        # Process each MD file
        md_files = sorted(self.topics_dir.glob("*.md"))
        print(f"Found {len(md_files)} MD files to process\n")
        
        success_count = 0
        for md_file in md_files:
            topic_id = md_file.stem  # filename without extension
            print(f"\nProcessing: {topic_id}")
            
            try:
                # Parse MD file
                md_data = self.parse_topic_md(md_file)
                
                # Update JSON
                if self.update_topic_in_json(json_data, topic_id, md_data):
                    success_count += 1
            except Exception as e:
                self.errors.append(f"Error processing {topic_id}: {str(e)}")
                print(f"❌ Error processing {topic_id}: {e}")
        
        # Save updated JSON
        output_path = Path("content/de/library_content.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n=== Update Complete ===")
        print(f"✅ Successfully updated {success_count}/{len(md_files)} topics")
        print(f"📁 Saved to: {output_path}")
        
        if self.errors:
            print(f"\n⚠️  Errors encountered:")
            for error in self.errors:
                print(f"  - {error}")
        
        return success_count == len(md_files)

if __name__ == "__main__":
    updater = JsonMdUpdater()
    success = updater.run()
    exit(0 if success else 1)