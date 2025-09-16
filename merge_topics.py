#!/usr/bin/env python3
"""
Merge separate topic markdown files back into a single library_content.md file
"""

import os
from pathlib import Path

def merge_topics(input_dir, output_file):
    """Merge separate topic files back into one file"""
    
    # Get all topic files in order
    topic_order = [
        'parenting_foundations',
        'child_development', 
        'understanding_tantrums',
        'lying_and_stealing',
        'understanding_whining',
        'understanding_winning_losing',
        'understanding_fears_anxiety',
        'understanding_repairing',
        'personality_social_skills',
        'understanding_sleep_bedtime',
        'understanding_screen_time',
        'understanding_transitions_change',
        'understanding_discipline_boundaries'
    ]
    
    # Start with header
    content_parts = [
        "# Library Content\n",
        "*Topics, articles, videos, and scripts for the parenting library*\n"
    ]
    
    # Process each topic in order
    separator = "\n\n" + "=" * 80 + "\n\n"
    
    for i, topic_id in enumerate(topic_order):
        topic_file = Path(input_dir) / f"{topic_id}.md"
        
        if topic_file.exists():
            with open(topic_file, 'r', encoding='utf-8') as f:
                topic_content = f.read()
                
                # Skip the header lines if present
                if topic_content.startswith("# Library Content"):
                    lines = topic_content.split('\n')
                    # Find where the actual topic content starts
                    for j, line in enumerate(lines):
                        if line.startswith("## 📂"):
                            topic_content = '\n'.join(lines[j:])
                            break
                
                content_parts.append(topic_content)
                
                # Add separator between topics (but not after the last one)
                if i < len(topic_order) - 1:
                    content_parts.append(separator)
                
                print(f"Added: {topic_id}")
        else:
            print(f"Warning: {topic_file} not found")
    
    # Write merged content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content_parts))
    
    print(f"\nMerged {len(topic_order)} topics into {output_file}")

if __name__ == "__main__":
    # Merge German topics
    input_dir = "content/de/topics"
    output_file = "content/de/library_content.md"
    
    merge_topics(input_dir, output_file)