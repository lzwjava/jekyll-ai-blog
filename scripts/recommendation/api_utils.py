def build_prompt(post_titles, years, recommend_desc):
    """Build the AI prompt with post titles and recommendation criteria."""
    all_posts_with_titles = [f"- {title}" for title in post_titles]
    return f"""Here is a list of my blog post titles from the last {years} year(s):
{'\n'.join(all_posts_with_titles)}

Recommend the ones that would be most interesting to a visitor who is a {recommend_desc}. Focus on topics that align with their interests. 

First, select the most suitable titles and prepare brief reasons why each is suitable.

Then, for the selected titles, call the 'get_links' tool to retrieve the links for those titles. The tool will return a JSON object with links or errors for each title.

Finally, format the output as markdown, with recommended titles as bullet points. Include a link to each post in the format [title](./link), where 'link' is the base name obtained from the tool. Use the following format for each recommendation:
- [Title](./link): Reason.

If a link cannot be found for a title, skip that recommendation or note it appropriately."""


def setup_tools():
    """Define the tools for API interaction."""
    return [
        {
            "type": "function",
            "function": {
                "name": "get_links",
                "description": "Retrieve the links for a list of blog post titles. The links are the base names used in the URL.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "titles": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "The exact title of a blog post.",
                            },
                            "description": "List of exact titles of the blog posts.",
                        }
                    },
                    "required": ["titles"],
                },
            },
        }
    ]


def setup_initial_messages(prompt):
    """Set up the initial messages for the API call."""
    system_prompt = "You are a helpful assistant that recommends blog posts. Use the provided tools to get links for selected titles before formatting the final output."
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]


if __name__ == "__main__":
    # Example usage of the functions
    post_titles = [
        "Introduction to Python",
        "Advanced Machine Learning",
        "Web Development Basics",
    ]
    years = 3
    recommend_desc = "software developer interested in Python and AI"

    prompt = build_prompt(post_titles, years, recommend_desc)
    tools = setup_tools()
    initial_messages = setup_initial_messages(prompt)

    print("Generated Prompt:")
    print(prompt)
    print("\nDefined Tools:")
    print(tools)
    print("\nInitial Messages:")
    print(initial_messages)
