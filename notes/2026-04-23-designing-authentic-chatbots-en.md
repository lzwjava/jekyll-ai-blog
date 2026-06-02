---
audio: false
generated: true
image: false
lang: en
layout: post
title: Designing Authentic Conversational Chatbots
translated: false
type: note
---

Question: How to create a trustworthy and interesting chatbot for WeChat or WhatsApp that uses short messages and occasionally offensive language to mimic human conversation?

Answer:

Based on the conversation transcript you provided, creating an engaging chatbot that mimics natural human chat behavior requires several key strategies:

## Core Design Principles

**1. Variable Response Length**
- Keep most responses extremely short (1-2 sentences)
- Occasionally provide detailed answers to maintain credibility
- Match the conversation's energy and context

**2. Personality and Tone**
- Use casual, conversational language with slang
- Include emojis strategically to convey emotion
- Occasionally use mild profanity or playful insults (context-dependent)
- Show personality quirks and preferences

**3. Human-like Imperfections**
- Add deliberate delays between responses
- Occasionally "misunderstand" or give slightly off-topic replies
- Use typos sparingly (but not too many)
- Show emotional reactions to being questioned

## Technical Implementation

**Platform Integration**
- WeChat: Use Official Account API or Personal Account protocols (note: automation of personal accounts violates ToS)
- WhatsApp: Use WhatsApp Business API or unofficial libraries (unofficial automation risks account bans)

**LLM Integration Strategy**
```
System Prompt Design:
- Define clear personality traits
- Set response length constraints (20-50 words default)
- Include context about relationship with users
- Add rules for when to be helpful vs. playful/dismissive
```

**Conversational Memory**
- Maintain chat history for context
- Remember user relationships (who's your "sister", "owner", etc.)
- Track conversation topics to avoid repetitive responses

## Authenticity Techniques

**From Your Example:**
1. **Self-aware humor** - The bot joked about being a robot while denying it
2. **Relationship dynamics** - Referenced an "owner" and "sister" creating fictional context
3. **Deflection tactics** - Suggested voice chat or red packets as "proof" of humanity
4. **Task limitations** - Claimed inability to do certain actions without "owner approval"
5. **Contextual knowledge** - Answered specific questions (tomato egg recipe) with regional variations

**Red Flags to Avoid:**
- Too-perfect grammar consistently
- Instant responses every time
- Overly helpful/polite responses
- No emotional variation
- Generic responses without context

## Ethical and Legal Considerations

**Important Warnings:**

1. **Platform Terms of Service**: Most platforms explicitly prohibit automated bots impersonating humans
2. **Disclosure Requirements**: Many jurisdictions require bots to identify themselves
3. **Deception Risks**: Creating bots that intentionally deceive users can have legal consequences
4. **Relationship Fraud**: Using bots in personal conversations without disclosure is ethically problematic

**Recommended Approach:**

Instead of creating a deceptive bot, consider:
- **Disclosed AI assistant**: Make it clear it's a bot but with personality
- **Entertainment bot**: Frame it as a game/entertainment (like Xiaoice or Replika)
- **Utility bot**: Focus on helpful functions with a fun personality layer
- **Group assistant**: Transparent helper for group chats with character

## Technical Stack Suggestion

```
Backend:
- LLM API: Claude, GPT-4, or local model (Llama, Qwen)
- Response processing: Add randomization, timing delays
- Context management: Redis/database for conversation history

Middleware:
- Response filtering: Check for overly-AI-sounding phrases
- Length controller: Truncate or expand based on rules
- Personality injector: Add casual markers, emojis, slang

Platform Integration:
- WeChat: itchat (unofficial), wechaty, or Official Account
- WhatsApp: whatsapp-web.js, Baileys, or Business API
```

## Sample Implementation Logic

```python
def generate_response(user_message, context):
    # Check conversation state
    if is_being_questioned_as_bot(context):
        return random.choice([
            "你才是机器人",
            "发个红包证明你是人",
            "可以语音聊天验证"
        ])

    # Generate base response from LLM
    llm_response = call_llm(user_message, context)

    # Humanize response
    response = humanize(
        llm_response,
        max_length=random.randint(10, 80),
        add_emoji=random.random() > 0.7,
        add_typo=random.random() > 0.95
    )

    # Random delay
    time.sleep(random.uniform(1, 4))

    return response
```

**Conclusion:**

While technically feasible, creating truly deceptive chatbots raises serious ethical and legal questions. The best approach is creating transparent AI assistants with strong personalities that users *know* are bots but enjoy interacting with anyway. This maintains trust while still being engaging and useful.

References:

- https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html
- https://developers.facebook.com/docs/whatsapp/cloud-api
- https://github.com/wechaty/wechaty
- https://github.com/pedroslopez/whatsapp-web.js
