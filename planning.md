# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Domain for this Unofficial Guide - NYU Campus Dining — covering dining hall quality, dietary accommodations, meal plan value, and student experiences across NYU's Manhattan and Brooklyn locations.

Im a big foodie and Im always curious on finding the best places to eat on campus during my time at NYU.
I love to explore different cafeterias and since NYU is in the middle of the city, they also have a couple of different offers and selections that we can take advantage of. Its harder to find through official channels on which dining halls serve what, which food is better, which ones are worth the cost and if people have dietary restrictions and some dining halls say officially they cater to it, but the food is never available - that would be a very useful use-case with this RAG. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Official NYU dining page | | https://nyu.edu/students/student-information-and-resources/housing-and-dining/dining.html |
| 2 | NYUEats | | https://dineoncampus.com/NYUeats |
| 3 | Allergen Guide | | https://www.nyu.edu/content/dam/nyu/campusServices/misc/24-25-dining/NYU%20Eats%20Allergen%20Guide.pdf |
| 4 | Dietary options | | https://www.nyu.edu/students/student-information-and-resources/housing-and-dining/dining/dietary-options.html |
| 5 | Brooklyn Meal Plans | | https://www.nyu.edu/students/student-information-and-resources/housing-and-dining/dining/nyu-meal-plan/brooklyn-meal-plans.html |
| 6 | Dining Cheat Sheet Article | | https://meet.nyu.edu/academics/student-voices/dining-hall-nyu-eats/ |
| 7 | Washington Square News | Ranked: What is the best NYU dining hall? — senior student's full ranking with specific food commentary per hall | https://nyunews.com/culture/dining/2022/09/18/ranked-dining-halls/ |
| 8 | Washington Square News | Opinion: First-years need freedom from meal plans — student data on wasted swipes and inflexible plan structures | https://nyunews.com/ops/2023/12/23/freshman-waste-too-many-meal-swipes/ |
| 9 | Her Campus NYU | A Definitive Ranking of NYU's Dining Halls — hall-by-hall breakdown including vegan/vegetarian options | https://www.hercampus.com/school/nyu/definitive-ranking-nyu-s-dining-halls/ |
| 10 | RateMyDorm | Student Guide to NYU Dining — covers Lipton, Downstein, Upstein, Third North with honest student reviews | https://www.ratemydorm.com/blog/student-guide-to-nyu-dining |
| 11 | USWIB | Dining Hall Superlatives — covers 18 Below, Upstein, Kimmel, Lipton from a student perspective | https://www.uswib.com/lifestyle/dining-hall-superlatives |
| 12 | Yelp – Third North Residence Hall | Student reviews touching on dining and dorm experience | https://www.yelp.com/biz/third-north-residence-hall-new-york |
| 13 | Yelp – Weinstein Passport Dining Hall | Student and visitor reviews of Weinstein dining | https://www.yelp.com/biz/weinstein-passport-dining-hall-new-york |
| 14 | Reddit r/nyu |  | https://www.reddit.com/r/nyu/comments/1s5snid/dining_hall_vs_offcampus_food/ |
| 15 | Reddit r/nyu |  | https://www.reddit.com/r/nyu/comments/pl7q2x/dining_hall_rant/ |
| 16 | Reddit r/nyu |  | https://www.reddit.com/r/nyu/comments/1hgwvzf/what_should_i_know_about_the_dining_halls/ |
| 16 | Reddit r/nyu |  | https://www.reddit.com/r/nyu/comments/mpbcl/dining_halls/ |
| 16 | Reddit r/nyu |  | https://www.reddit.com/r/nyu/comments/1flj4de/best_dining_halls_go/ |
| 16 | Reddit r/nyu |  | https://www.reddit.com/r/nyu/comments/8iwih0/is_it_worth_keeping_the_meal_plan_after_freshman/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 300

**Overlap:** 75

**Reasoning:** The documents I have gathered have a mix of long opinion articles (WSN, Her Campus) sit alongside structured PDFs (allergen guide) and short reviews (Yelp, Reddit).  A lot of your most useful content is actually pretty atomic, if your chunks are 400 tokens, that fact gets buried in a wall of surrounding text, and retrieval might miss it or return a lot of noise around it. The WSN articles are long enough that 300-token chunks still capture full thoughts.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5 - seems like a good spot since 3 may not get enough tokens and 7+ might get in too much noise

**Production tradeoff reflection:** In production, the main tradeoff is between MiniLM's speed and zero cost versus the accuracy and context-length gains of a hosted model like OpenAI's text-embedding-3-large.

MiniLM maxes out at 256 tokens per chunk, which works fine for short student reviews but would silently truncate longer documents in a larger corpus. It's also trained on general text, so it has no special understanding of dining-specific vocabulary — a fine-tuned or larger model would retrieve more precisely on niche queries. 

NYU's international student body is also worth considering: a multilingual model like paraphrase-multilingual-MiniLM-L12-v2 would capture non-English reviews that MiniLM might embed poorly. 

Finally, latency — MiniLM runs on CPU for free, while a hosted API like OpenAI embeddings adds cost and external dependency but offers better reliability at scale. 

For this project, MiniLM is the right call; in production the choice would depend on query volume, user language diversity, and budget.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about vegan and vegetarian options at Lipton Hall? | Lipton has the best variety of vegan/vegetarian options, a dedicated vegan station, and is 100% Halal certified |
| 2 | Is the NYU meal plan worth it for first-year students? | Students report wasting swipes end-of-semester; the plan is inflexible, minimum 200 swipes/semester for most dorms |
| 3 | Which dining hall do students recommend for someone with gluten allergies? | Official allergen guide and student sources point to specific options; Lipton and the Kosher Eatery flagged most often |
| 4 | What do students say about wait times and crowding at Kimmel during lunch? | Kimmel lines during lunch are notoriously long but food quality is considered worth the wait |
| 5 | How does Downstein compare to Upstein for food quality? | Upstein generally ranked higher; Downstein known for soft serve and community feel but less variety |
---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. There is a lot of cross-referencing happening. Where different documents can have different info - for exmaple, official documents could state something else but the reddit threads or Yelp reviews could point in a completely different direction. So that should be stated explicitly to the user - retrieval might surface contradictory chunks (official page says dietary options are available; student review says they're never stocked), and the LLM may confidently blend them into a misleading answer rather than flagging the disagreement.

2. Since its a lot of scraping social media threads, it could have noisy data - wrong information or a side-thread talking about something irrelevant or ads. eg - Reddit threads drift into tangents about dorms, NYC restaurants, or campus life generally, and those off-topic chunks will still get embedded and retrieved on food queries.

3. Data that is too old (many years ago and things might have changed now), dining hall menus, hours, and meal plan prices change every semester, so a 2019 Her Campus article or old Reddit thread could be confidently wrong about something that has since changed.

4. Chunks splitting key information across boundaries - a review that says "the chicken is great..." in one chunk and "...but only on Tuesdays, every other day it's awful" in the next chunk. Retrieved alone, the first chunk gives a misleading answer. 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
 
┌──────────────────────────────┐
│        Document Ingestion    │
│   Web Scraper + PDF Parser   │
└───────────────┬──────────────┘
                │
┌───────────────▼──────────────┐
│           Chunking           │  
│   300 tokens / 75 overlap    │
└───────────────┬──────────────┘
                │
┌───────────────▼──────────────┐
│      Embedding + Vector Store│
│        all-MiniLM-L6-v2      │
│           (ChromaDB)         │
└───────────────┬──────────────┘
                │
┌───────────────▼──────────────┐
│           Retrieval          │
│  ChromaDB cosine similarity  │
│           top-k = 5          │
└───────────────┬──────────────┘
                │
┌───────────────▼──────────────┐
│          Generation          │
│           Llama LLM          │
└──────────────────────────────┘ 
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

Tool: Claude

Input: Domain section, Documents section (including all source URLs), Chunking Strategy section, and Architecture diagram to give full pipeline context.

Expected output: ingest.py containing:

A document loading function that scrapes each source URL and loads the allergen PDF
chunk_documents() that takes chunk size (300) and overlap (75) as inputs and returns chunked documents
chunk_documents() should save chunks to a file (e.g. chunks.json)

Verification:

Print the total number of documents successfully loaded and spot-check each source by printing the first 200 characters of its content to confirm scraping worked

For any sources that block scraping (Reddit, some NYU pages), note these will be handled manually

Print the total number of chunks produced, the token size of each chunk, and randomly sample 5 chunks to verify they are the right size and contain coherent text

```python
load_documents(urls: list[str]) -> list[str]
chunk_documents(docs: list[str], chunk_size: int = 300, overlap: int = 75) -> list[str]
```

**Milestone 4 — Embedding and retrieval:**

Tool: Claude

Input: Retrieval Approach section, Architecture diagram, Chunking Strategy section, and Evaluation Plan to guide testing.

Expected output: retriever.py containing:

embed_and_store() that takes chunked documents from ingest.py - it takes the output of chunk_documents() as input, embeds them using all-MiniLM-L6-v2 and stores them in ChromaDB

retrieve() that takes a query string and returns the top 5 most relevant chunks using cosine similarity

Verification:

Run 1-2 evaluation questions through retrieve() and print the returned chunks to manually check if the results are relevant and on-topic.
If results feel too broad or noisy, tune top-k down to 3; if results feel thin or incomplete, tune up to 7.

Confirm ChromaDB index was built correctly by checking the total number of stored embeddings matches the chunk count from Milestone 3

```python
embed_and_store(chunks: list[str]) -> chromadb.Collection
retrieve(query: str, k: int = 5) -> list[dict[str, any]]
# where each dict has keys: "text", "source", "similarity_score"
```

**Milestone 5 — Generation and interface:**

Tool: Claude

Input: Architecture diagram, Anticipated Challenges section, Evaluation Plan, and Chunking Strategy section to inform prompt construction.

Expected output:

generator.py containing:

Calls Groq API using API key stored in .env

Receives retrieved chunks and cosine similarity scores from retrieve.py

Constructs a prompt that includes the retrieved chunks as context, instructs the model on what to avoid (based on Anticipated Challenges — e.g. don't blend conflicting sources, flag stale information), and passes the user query

Returns the generated answer to app.py

app.py containing the frontend interface where users can type a query and see the generated answer - app.py would be a simple Streamlit front-end with a title for 'Unofficial Guide to NYU Dining' and have the chat option with 2-3 of the sample questions from the evaluation plan. 

Error handling - go through the challenges section, flag uncertainty rather than answer confidently when sources conflict

Verification:

Run all 5 evaluation questions end-to-end and compare outputs against expected answers in the Evaluation Plan

Check that the model is correctly grounding answers in retrieved chunks and not hallucinating beyond them

Verify .env API key is loading correctly and Groq API calls are succeeding

```python
construct_prompt(query: str, chunks: list[dict]) -> str
generate(query: str, chunks: list[dict]) -> str
```