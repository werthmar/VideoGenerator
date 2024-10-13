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
            title = input("Please enter a title for your story: ").strip()
            # Add the story and title to the list as a dictionary
            stories.append({'story': story, 'title': title})
            print(f"Story '{title}' has been added.\n")

            # Ask if user wants to add another story
            x = input("Add another story? (y/n)").strip().lower()
            if x == 'n':
                break


    # Optionally print all stories collected
    print("\nAll Stories:")
    for item in stories:
        print(f"Title: {item['title']}\nStory: {item['story']}\n")

    return stories


if __name__ == "__main__":
    manualStoryInput()