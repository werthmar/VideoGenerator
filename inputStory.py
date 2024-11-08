import re

def read_multiline_input(prompt="Enter story (type 'END' on a new line to finish):\n"):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    return lines  # Returns a list of strings

def manualStoryInput():
    stories = []  # List to hold story dictionaries

    while True:
        story_lines = read_multiline_input()
        story = "\n".join(story_lines)
        print("\nStory entry complete.")

        if story.strip().lower() == 'go':
            print("Starting generator...")
            break

        else:
            # Clean the story
            title, tags, cleaned_story = extract_title_and_tags(story)

            # Add the story and title to the list as a dictionary
            stories.append({'story': cleaned_story, 'title': title, 'tags': tags})
            print(f"Story '{title}' has been added. Tags: {tags}\n")

            # Ask if user wants to add another story
            x = input("Add another story? (y/n)").strip().lower()
            if x == 'n':
                break


    # Optionally print all stories collected
    print("\nAll Stories:")
    for item in stories:
        print(f"Title: {item['title']}\nTags: {item['tags']}\nStory: {item['story']}\n")

    return stories

def extract_title_and_tags(text):
    # Improved patterns to handle any whitespace between tags and text,
    # and to make it case insensitive if needed.
    title_pattern = r'<title\s*>(.*?)<\/title\s*>'
    tags_pattern = r'<tags\s*>(.*?)<\/tags\s*>'

    # Extract title and tags
    title_match = re.search(title_pattern, text, re.IGNORECASE)
    tags_match = re.search(tags_pattern, text, re.IGNORECASE)

    # Extract and strip the title and tags
    title = title_match.group(1).strip() if title_match else None
    tags = tags_match.group(1).strip() if tags_match else None

    # Remove the title and tags, and line breaks from the text
    text_without_title = re.sub(title_pattern, '', text, flags=re.IGNORECASE)
    text_without_title_and_tags = re.sub(tags_pattern, '', text_without_title, flags=re.IGNORECASE)
    #text_without_title_and_tags_and_line_breaks = text_without_title_and_tags.replace("\n", "").strip()

    return title, tags, text_without_title_and_tags


if __name__ == "__main__":
    manualStoryInput()