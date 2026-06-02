---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Maximizing Zoom AI Companion Outputs
translated: false
type: note
---

Question: In Zoom AI Companion, how can I extract as much detailed information as possible from the chat box, such as a comprehensive 10-minute summary without word limits like 500 words, a structured transcript for a one-hour meeting (e.g., by time segments or individual speakers like "what one speaker said" vs. "what David said"), and an organized or refined transcript overall?

Answer:

### Enabling and Accessing Zoom AI Companion for Detailed Outputs

Zoom AI Companion is an AI-powered assistant integrated into Zoom meetings that generates real-time transcripts, summaries, and answers based on the conversation. To get the most out of it—especially for long meetings like one hour—start by enabling it in your Zoom settings (under **Settings > AI Companion** in the web portal). As the host, you can toggle features like **Meeting Summary** and **Ask AI Companion** before or during the meeting. This uses a temporary transcript (no full recording needed unless you want one). For guests, request the host to enable sharing.

Key limitation: AI responses in the chat box (accessed via the sparkle icon during/after meetings) often cap at ~500 words due to design for brevity. To bypass this for comprehensive details, use iterative prompting, post-meeting access, or download the full transcript.

### Getting Comprehensive 10-Minute Summaries Without Strict Word Limits

- **During the Meeting (Real-Time Chat Box):**
  - Open the AI Companion panel (sparkle icon in the toolbar).
  - Use built-in prompts like "Summarize the meeting" for an initial bullet-point overview of topics, speakers, and action items. For more depth in 10 minutes of discussion:
    - Prompt: "Provide a detailed summary of the last 10 minutes, including timestamps, key quotes from each speaker, and decisions made."
    - Follow up iteratively: If it hits a limit, ask "Expand on [specific topic/speaker] from the last summary" or "Continue the summary from where you left off."
  - Tip: Ask for structured formats like numbered lists: "Create a numbered list of topics from the last 10 minutes, with the speaker's name and a 2-3 sentence recap for each." This encourages longer, organized outputs without exceeding limits in one go.

- **Post-Meeting (for Deeper Analysis):**
  - After the meeting ends, access the summary via email, Zoom Team Chat, or your account's **Recordings & Transcripts** section (under **My Summaries** tab).
  - Re-open the AI Companion chat in the meeting recap to query the full context: "Generate a comprehensive 10-minute breakdown of [time segment, e.g., 15:30-15:40], ignoring brevity—include full quotes and speaker attributions."
  - To avoid limits: Break it into parts (e.g., "Summarize minutes 1-5 in detail" then "Minutes 6-10") and compile manually.

This approach can yield 1,000+ words total by chaining responses, as the AI draws from the entire transcript.

### Handling One-Hour Meetings: Using Time Segments or Per-Speaker Breakdowns

For a full hour, divide the analysis to build a refined, organized transcript. AI Companion doesn't auto-generate a full verbatim transcript in chat (it's summary-focused), but you can prompt for speaker-specific or timed details.

- **By Time Segments (e.g., Quarterly Breakdowns):**
  - Prompt: "Break down the one-hour meeting into four 15-minute segments. For each, list: timestamp range, main topics, speakers involved, key quotes, and action items."
  - For refinement: "Refine the transcript for [segment]: Remove filler words, attribute every statement to a speaker (e.g., 'David said: [quote]'), and highlight decisions."
  - Post-meeting: Download the raw transcript (if enabled via **Settings > Recording > Cloud Recording > Audio Transcript**) and feed sections back into the chat: "Analyze this transcript excerpt [paste text] for speaker David—what did he say about [topic]?"

- **Per-Speaker Analysis (e.g., "What Does One Say" vs. "What Does David Say"):**
  - During/after: "Provide a speaker-specific recap: What did [Speaker Name, e.g., David] contribute? Include quotes, timestamps, and how it related to others' input."
  - For all speakers: "Create an organized transcript by speaker: Group statements chronologically for each person, starting with 'David's contributions:' followed by bulleted quotes and context."
  - Advanced: "Compare speakers: What did the group say on [topic] vs. what David said? Use a table format with columns for Speaker, Quote, Timestamp, and Impact."
  - To organize: Request "Refined transcript: Chronological order, speaker-labeled (e.g., David: [text]), with headings for topics and bolded action items."

For a one-hour meeting, this might take 5-10 iterative prompts (2-3 minutes each) to cover everything comprehensively. Enable **Retain Transcripts** in admin settings (Account/Group level) to access raw data longer (up to 180 days).

### Building an Organized, Refined Transcript Overall

- **Steps for a Full Refined Transcript:**
  1. **Enable Transcription:** Turn on **Live Transcript** or **Cloud Recording** pre-meeting for a downloadable VTT/TXT file with timestamps and speaker IDs.
  2. **Generate Base Summary:** Use "Full meeting summary" prompt post-meeting for topics, highlights, and actions.
  3. **Refine in Chat:** Paste transcript chunks into AI Companion: "Refine this full transcript: Organize by topic sections, attribute speakers accurately, remove redundancies, and add summaries per section."
  4. **Export and Share:** Save outputs to a doc; share via email/Team Chat. For visuals, prompt "Format as a Markdown table: Rows for timestamps, columns for Speaker, Content, Actions."

- **Best Practices:**
  - **Prompt Engineering:** Be specific (e.g., "Ignore word limits—provide exhaustive detail") and iterative to expand outputs.
  - **Templates:** Use Zoom's built-in ones (e.g., "Project Update" for structured recaps) or custom: "Lecture-style transcript with Q&A sections."
  - **Limitations & Workarounds:** Accuracy drops with accents/noise—review manually. For unlimited depth, download the transcript and use external tools like ChatGPT, but stay in Zoom for seamless integration.
  - **Privacy Note:** Transcripts are temporary (30 days) unless retained; Zoom doesn't train on your data.

This method turns AI Companion into a powerful tool for detailed, speaker-aware transcripts without needing third-party apps.

References:

- [Accessing Full Transcript of AI Companion](https://community.zoom.com/t5/Zoom-AI-Companion/Accessing-full-transcript-of-AI-Companion/m-p/207315)
- [Using Meeting Summary with AI Companion](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058013)
- [Zoom AI Companion FAQ](https://uis.georgetown.edu/zoom/zoom-ai/zoom-ai-faq/)
- [How to Use Zoom AI Transcription Tool](https://tactiq.io/learn/zoom-ai-transcription-tool)
- [Use Zoom’s AI Companion to Take Notes and Summarize Meetings](https://www.wired.com/story/zoom-ai-companion-take-notes-summarize-meetings/)
- [The Ultimate Guide To Zoom AI Companion](https://getvoip.com/blog/zoom-ai-companion/)
- [Favorite AI Companion Tips and Tricks](https://www.zoom.com/en/blog/ai-companion-tips-and-tricks/)
- [Zoom AI Companion Explained](https://tactiq.io/learn/zoom-ai-companion-explained)
