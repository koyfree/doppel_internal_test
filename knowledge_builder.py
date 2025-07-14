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

[Top 5 Things this character loves and hates]
\t•\tWhat this character love: 
{row['top5_love']}
\t•\tWhat this character hate: 
{row['top5_hate']}

[Weekly Activities Overview]
\t•\t{row['weekly_activities']}
"""
    return knowledge
