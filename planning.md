# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
The domain i chose was Campus Dining! Im a big foodie and Im always curious on finding the best places to eat on campus during my time at NYU.
I love to explore different cafeterias and since NYU is in the middle of the city, they also have a couple of different offers and selections that we can take advantage of. Its harder to find thorugh official channels on which dining halls serve what, which food is better, which ones are worth the cost and if people have dietary restrictions and some dining halls say officially they cater to it, but the food is never available that would be a very useful use-case with this RAG. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Official NYU dining page| | nyu.edu/students/student-information-and-resources/housing-and-dining/dining.html|
| 2 | NYUEats| | dineoncampus.com/NYUeats|
| 3 | Allergen Guide| | https://www.nyu.edu/content/dam/nyu/campusServices/misc/24-25-dining/NYU%20Eats%20Allergen%20Guide.pdf|
| 4 | Dietary options| | https://www.nyu.edu/students/student-information-and-resources/housing-and-dining/dining/dietary-options.html?challenge=d06e90d7-4d8f-4b88-9d8c-10b73beb60f1|
| 5 | Brooklyn Meal Plans| | https://www.nyu.edu/students/student-information-and-resources/housing-and-dining/dining/nyu-meal-plan/brooklyn-meal-plans.html?challenge=d06e90d7-4d8f-4b88-9d8c-10b73beb60f1|
| 6 | Dining Cheat Sheet Article| | https://meet.nyu.edu/academics/student-voices/dining-hall-nyu-eats/|
| 7 | NYU news - dining| | https://nyunews.com/?s=dining|
| 8 | Reddit|Dining Hall for NYU r/nyu thread | https://www.reddit.com/r/nyu/search/?q=dining+hall&cId=d77d3b17-3c32-4607-b1a2-fc94aa52835b&iId=96148a0b-0dc0-463c-9059-e11315c37441|
| 9 | Reddit| |https://www.reddit.com/r/nyu/search/?q=meal+plan&cId=274bb81d-565d-4edb-96f3-5138efc3ebc9&iId=9221ea28-9e0e-4a60-a41c-d355a972d965 |
| 10 | Yelp| | https://www.yelp.com/biz/weinstein-passport-dining-hall-new-york|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
