import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 1000000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # n is total number of pages in the corpus
    n = len(corpus)

    # Surfer choosing one of all pages with equal probability
    probability = {p: (1 - damping_factor) / n for p in corpus}

    # Links is set of pages that current page links to
    links = corpus[page]
    num_links = len(links)

    if num_links == 0:
        for p in corpus:
            probability[p] += damping_factor / n
    else:
        for linked_page in links:
            probability[linked_page] += damping_factor / num_links

    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize counter so that we keep track of each page occurrence. By default, all pages will be assigned 0
    counter = {page: 0 for page in corpus}
    page = random.choice(list(corpus.keys()))
    counter[page] += 1

    for _ in range(n - 1):
        probability = transition_model(corpus, page, damping_factor)
        page_names = list(probability.keys())
        pageranks = list(probability.values())

        # Next page is randomly chosen based on weight
        page = random.choices(page_names, weights=pageranks, k=1)[0]
        counter[page] += 1

    pagerank = {page: count / n for page, count in counter.items()}
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    pagerank = {page: 1 / n for page in corpus}

    while True:
        ranks = {}
        for page in corpus:
            rank = (1 - damping_factor) / n
            for linking_pages in corpus:
                links = corpus[linking_pages]
                if len(links) == 0:
                    rank += damping_factor * (pagerank[linking_pages] / n)
                elif page in links:
                    rank += damping_factor * (pagerank[linking_pages] / len(links))
            ranks[page] = rank

        if all(abs(ranks[page] - pagerank[page]) <= 0.001 for page in pagerank):
            break

        pagerank = ranks.copy()

    return pagerank


if __name__ == "__main__":
    main()