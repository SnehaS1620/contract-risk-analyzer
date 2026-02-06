from openai import OpenAI

# hardcoded key for hackathon simplicity
client = OpenAI(api_key="PASTE_YOUR_REAL_KEY_HERE")


def explain_clause(text, risks, lang="English"):
    try:
        if lang == "Hindi":
            instruction = "Explain this contract clause in simple Hindi."
        else:
            instruction = "Explain this contract clause in simple business English."

        prompt = f"""
{instruction}

Clause:
{text}

Risks detected: {", ".join(risks)}

Explain meaning, why risky, and safer wording.
"""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return resp.choices[0].message.content

    except:
        return "⚠️ AI explanation unavailable."

def summarize_contract(text, lang="English"):
    try:
        if lang == "Hindi":
            instruction = "Summarize this contract in simple Hindi bullet points."
        else:
            instruction = "Summarize this contract in simple English bullet points."

        prompt = f"""
{instruction}

{text[:2000]}
"""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return resp.choices[0].message.content

    except:
        if lang == "Hindi":
            return "⚠️ एआई स्पष्टीकरण अस्थायी रूप से उपलब्ध नहीं है।"
        else:
            return "⚠️ AI explanation temporarily unavailable."


