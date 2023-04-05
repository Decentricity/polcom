import openai
import re

def opinionate(text):
    text_op = re.search(r'"text": "(.*?)Economic Score', text, re.DOTALL)
    if text_op:
        return text_op.group(1)
    else:
        return None

# Set up the OpenAI API key

openai.api_key = "something"


# Main loop that prompts the user to enter social media posts and
# uses the OpenAI API to determine the political leanings of each post
economic_scores = []
social_scores = []
libertarian_scores = []
while True:
    post = input("Enter a social media post (type 'end' to finish): ")
    if post.lower() == "end":
        break

    # Call the OpenAI API to analyze the post
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"This is a tool to determine the political stance of a certain social media post.\n\nThe user provides the social media post, and the tool responds with three scores from -10 to 10.\n\nThe first score, score A, represents economic stance, where the lower the score, the more left-wing the post is, and the higher, the more right-wing.\nThe second score, score B, represents social stance, where the lower the score, the more socially left-wing the post is, and the higher, the more socially right-wing.\nThe third score, score C, represents libertarian/authoritarian stance, where the lower the score, the more libertarian the post is, and the higher, the more authoritarian.\nThe user's words are: "+post+".\nAnswer should be in the format:\n<opinion of the tool>\nEconomic Score: A\nSocial Score: B\nLibertarian Score: C",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the political slant scores from the OpenAI API response
#    scores_match = re.search(r'Economic Score:\s*(-?\d+)\s+Social Score:\s*(-?\d+)\s+Libertarian Score:\s*(-?\d+)', str(response))
    scores_match = re.search(r'Economic Score: (-?\d+)\nSocial Score: (-?\d+)\nLibertarian Score: (-?\d+)', response.choices[0].text)
    if scores_match:
        economic_scores.append(int(scores_match.group(1)))
        social_scores.append(int(scores_match.group(2)))
        libertarian_scores.append(int(scores_match.group(3)))

        # Print the scores for the post
        print(opinionate(repr(response)))
        print(f"Economic Score: {scores_match.group(1)}")
        print(f"Social Score: {scores_match.group(2)}")
        print(f"Authoritarian Score: {scores_match.group(3)}")
    else:
        print(response) 

# Compute the average scores for all of the posts
if len(economic_scores) > 0:
    avg_economic_score = sum(economic_scores) / len(economic_scores)
    avg_social_score = sum(social_scores) / len(social_scores)
    avg_libertarian_score = sum(libertarian_scores) / len(libertarian_scores)

# Print the average scores across all posts
    print(f"\nYour average scores across all posts, in a range between -10 and 10, are:")
    print(f"Economic Score: {avg_economic_score:.2f} (Negative numbers indicate left-wing economic views, positive numbers indicate right-wing economic views)")
    print(f"Social Score: {avg_social_score:.2f} (Negative numbers indicate socially left-wing views, positive numbers indicate socially right-wing views)")
    print(f"Authoritarian Score: {avg_libertarian_score:.2f} (Negative numbers indicate libertarian views, positive numbers indicate authoritarian views)")

else:
    print("No posts were entered. Please run the program again.")
