import pandas as pd

def build_knowledge_dict(sheet_url: str) -> dict:
    # CSV 형식 링크로 변환
    if "edit" in sheet_url:
        sheet_url = sheet_url.replace("/edit?", "/export?format=csv&")

    df = pd.read_csv(sheet_url)
    knowledge = {}

    for _, row in df.iterrows():
        name = row['Name']
        knowledge[name] = f"""
Profile:
[Demographics]
{row['Demo']}

[Personality]
{row['Big5']}

Below is a transcript of an interview where the chatbot asked the user about their preferences and experiences. 
Use this to understand what the character likes, dislikes, how their week went, and how they naturally express themselves in tone and style.
Only the user's responses (marked as "user") should be used as knowledge. 
The chatbot's questions (marked as "chatbot" or "assistant") are only provided to give context and should not be treated as part of the user’s knowledge.

[Interview: Top 5 Things This Character Loves]
{row['top5_love']}

[Interview: Top 5 Things This Character Hates]
{row['top5_hate']}

[Interview: Weekly Activities Overview]
{row['weekly_activities']}
"""
    return knowledge
