#this one can grab from net
import re
import requests
import openai
from bs4 import BeautifulSoup

def get_scores(statement):
    openai.api_key = "something"
    prompt = f"This is a tool to determine the political stance of a certain statement.\n\nThe statement is: {statement}\n\nThe tool responds with three numbers between -10 and 10, which represent the following:\n\nEconomic Score: Negative numbers indicate left-wing economic views, positive numbers indicate right-wing economic views.\nSocial Score: Negative numbers indicate socially left-wing views, positive numbers indicate socially right-wing views.\nAuthoritarian Score: Negative numbers indicate libertarian views, positive numbers indicate authoritarian views.\n\nJustification: Please provide a brief justification of your scores for this statement.\n\nThe user's words are: {statement}.\n\nAnswer should be in the format:\nEconomic Score: N\nSocial Score: N\nAuthoritarian Score: N\nJustification: ..."
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
    except openai.error.InvalidRequestError as e:
        return 0, 0, 0
    print(f"\n\n\nStatement {total_lines}\n{statement}\n")
    print(response.choices[0].text)
    scores_match = re.search(r'Economic Score: (-?\d+)\s*Social Score: (-?\d+)\s*Authoritarian Score: (-?\d+)\s*Justification:', response.choices[0].text)
    if scores_match:
        return int(scores_match.group(1)), int(scores_match.group(2)), int(scores_match.group(3))
    else:
        return 0, 0, 0

url = input("URL plz as a wassie: ")
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

lines = [p.text.strip() for p in soup.find_all('p') if len(p.text.strip()) >= 20]

total_lines = 0
total_economic_scores = 0
total_social_scores = 0
total_authoritarian_scores = 0

for line in lines:
    if not line:
        continue

    total_lines += 1
    economic_score, social_score, authoritarian_score = get_scores(line)
    total_economic_scores += economic_score
    total_social_scores += social_score
    total_authoritarian_scores += authoritarian_score

print(f"\nTotal Lines: {total_lines}")
print(f"Total Economic Scores: {total_economic_scores}")
print(f"Total Social Scores: {total_social_scores}")
print(f"Total Authoritarian Scores: {total_authoritarian_scores}")

print("\nAverage Scores:")
print(f"Economic: {total_economic_scores / total_lines:.2f}")
print(f"Social: {total_social_scores / total_lines:.2f}")
print(f"Authoritarian: {total_authoritarian_scores / total_lines:.2f}")
