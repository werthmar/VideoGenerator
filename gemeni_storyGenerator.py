import random
import re
import vertexai
from vertexai.generative_models import GenerativeModel

def generateStory():
    available_stories = [
        'Topic 1: how your family tried to steal something from you like a house/car/valuable/job/...,'
        'Topic 2: a am i the asshole story,'
        'Topic 3: a how i got fired story,'
        'Topic 4: a what was your wierdes customer interaction or wierdest request you got working a certain job,'
        'Topic 5: an encounter with a crazy karen,'
        'Topic 6: annoying influencers demanding things for free or being a public nuissance,'
        'Topic 7: how you took revenge on a bully in a very pityful and mean way,'
        'Topic 8: how you got arrested and or jailed for doing something stupid,'
        'Topic 9: lovestory about heartbreak, cheating, getting back together or finding each other'
    ]
    selected_story = random.choice(available_stories)

    prompt=f'I Want you to write a story. Read to the end of the prompt before starting to generate the story. Write out of your perspective. Make these stories exciting, like a really angry customer interaction that spirals out of control and then a big payoff at the end like the customer beeing arrested. Alternativly the story can end with a bad Ending like the family being torn appart or a bittersweet ending which contains good aswell as bad aspects. Exaggerate the Characters and Story but keep them believable, like a story that could have actually happend. Get angry at the karen or the asshole or the boss, flip out or do something over the top. Do not talk about how you learned a lesson or how there is something positive in the story at the end. Instead end the story quickly with a highlight. Do not use words that arent English. Write in multiple parts without specifying the parts. A Story segment can cross over multiple parts. Try to be around {random.randint(750, 800)} words. Do not use Abbreviations like HR, write the full word instead. Use normal, everyday language and avoid fancy words, wordplay or metaphors. Write like a real human talking about their experience. Write the text so that it is easy to read for a text to speech model. Also avoid special characters or special formatting, because it is meant to be read out loud by a program. Do not use cursive. Now write the story like the stories from reddit talking about {selected_story} Begin the story with a realy short TL;DR(Too Long Didnt read) In which you outline the events in a catchy way without spoiling the ending. Dont spell out TL;DR just wirte the TL;DR WITHOUT writing TL;DR at the start of it. For example in the case of an Am I the Asshole story begin with: "am i the asshole for doing x? and than beginn the real story. Or in the case of a Karen story something like: "Crazy caren demands me being fired for not allowing her to steal" adapt this approach to the topic appropriatly. Do not generate tags for the TL;DR. After the story generate a compelling title for this story in 2-3 short (max 7 letters per word) words with an emoji at the end and exclamationmarks. Write <title></title> and put the title within these brackets Then write <tags></tags> and put multiple Tags within these brackets. All tags start with a #. you always must include the tags #foru #foryoupage, #tts #funny, #fyp, #redditstories, #redditreadings, #reddit. Add at least 100 other tags fitting the story like #karen when its a "karen" story or #aita when its a "am i the asshole" story. You can also add tags that help the video to get more traction on tiktok like #POV or #comedy.'


    PROJECT_ID = "videogenerator-438710"
    vertexai.init(project=PROJECT_ID, location="europe-west3") #us-central1

    model = GenerativeModel("gemini-1.5-pro-002")

    response = model.generate_content(prompt)
    story = response.text

    # Clean the story
    title, tags, cleaned_story = extract_title_and_tags(story)

    # Add the story and title to the list as a dictionary
    print(f"Story '{title}' has been generated. Tags: {tags}\nStory: {cleaned_story}")
    return title, tags, cleaned_story

    #print(response.text)

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
    generateStory()