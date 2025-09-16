#!/usr/bin/env python3
"""
Split the library_content.md file into separate topic files for easier translation
"""

import re
import os

def split_topics(input_file, output_dir):
    """Split the combined markdown file into separate topic files"""
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Split by the topic separator (80 equals signs)
    topic_separator = "=" * 80
    topics = content.split(topic_separator)
    
    # Process each topic
    topic_count = 0
    for topic_block in topics:
        if "## 📂 " in topic_block:
            # Extract topic ID
            id_match = re.search(r'\*\*ID:\*\* `(.+?)`', topic_block)
            if id_match:
                topic_id = id_match.group(1)
                
                # Clean up the topic block
                topic_content = topic_block.strip()
                
                # Save to file
                output_file = os.path.join(output_dir, f"{topic_id}.md")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(topic_content)
                
                print(f"Created: {output_file}")
                topic_count += 1
    
    print(f"\nSplit into {topic_count} topic files in {output_dir}/")
    return topic_count

if __name__ == "__main__":
    input_file = "content/en/library_content.md"
    output_dir = "content/en/topics"
    
    split_topics(input_file, output_dir)