import os
from openai import OpenAI
from dotenv import load_dotenv

test_story = 'It all started when I switched jobs six months ago. The new place was great at first—good pay, short commute, and a decent team. But it didn’t take long for me to notice something was…off. My coworkers, especially my boss Rachel. had this weird energy. They were overly friendly, almost suspiciously so. I’m not one to complain about people being nice, but it was like they were all playing a role. Small things started to feel strange: people kept offering me food. Like, all the time. I’d be at my desk, and Cheryl from HR would just drop off a random slice of cake or a burrito she “couldn’t finish.” Then Steve from marketing did the same. Every. Single. Day. Rachel was the worst. She kept asking if I “felt at home” and mentioned how important it was to build a sense of family at work. At first, I thought it was just team bonding stuff. But then, they started asking really personal questions about my home life. How many bedrooms I had, if I lived alone, what my mortgage was like. At the same time, things were going sideways with my family. My parents had always been weirdly fixated on my house. I bought it after years of saving, and ever since then, they’d drop hints about how “it’s such a big place for one person.” A few weeks after starting this new job, my brother Matt—who I’d barely heard from in years—suddenly started showing up. At first, it was casual. He said he was “just in the area” and wanted to hang out. But then he started making comments like, “Man, if I had a place like this, I’d definitely throw some killer parties. Too bad your neighborhood’s so quiet.” He wasn’t even wrong; I love the peace and quiet. But then my mom jumped on board with this narrative too, telling me I should sell the house and move closer to them so we could “all be a family again.” I started feeling paranoid. Why was everyone so interested in my house all of a sudden?'

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

def generateStory():

    # Example usage of the OpenAI API
    #response = client.chat.completions.create(
    #    messages=[
    #        {
    #           "role": "user",
    #            "content": "Say this is a test",
    #        }
    #    ],
    #    model="gpt-3.5-turbo",
    #)
    #return response

    return test_story

    # Print the generated story
    #story = response.choices[0].message['content']
    #print(story)

if __name__ == "__main__":
    story = generateStory()
    print(story)