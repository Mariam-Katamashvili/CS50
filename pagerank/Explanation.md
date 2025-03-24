# Explanation of Implementation

We have to implement two ways of showing pages' popularity: one by sampling and the other by iterating. The first approach simulates a random surfer using the sampling method (via the sample_pagerank function), while the second approach computes PageRank by repeatedly applying the PageRank formula until convergence (via the iterate_pagerank function). The transition_model function is used by sample_pagerank to determine the probability distribution over the next page to visit.

## transition_model
The transition_model function calculates the probability distribution for the next page a random surfer might visit. It starts by giving each page a base probability of 
(1 - damping_factor) / n is the total number of pages. If the current page has outgoing links, the damping factor is divided evenly among those links and added to the base probability. If there are no links from the current page, the damping factor is spread evenly among all pages. 

```` python
probability = {p: (1 - damping_factor) / n for p in corpus}
links = corpus[page]
if len(links) == 0:
    for p in corpus:
         probability[p] += damping_factor / n
else:
    for linked_page in links:
         probability[linked_page] += damping_factor / len(links)
````

## sample_pagerank

The sample_pagerank function uses the transition model to simulate a random surfer. It begins at a random page and then repeatedly uses the transition model to decide the next page to visit. Each time a page is visited, we count that visit. After n samples, the fraction of visits a page gets is taken as its estimated PageRank. After completing all the samples, we calculate the PageRank for each page by dividing its count by the total number of samples.
```` python
 counter = {page: 0 for page in corpus}
    page = random.choice(list(corpus.keys()))
    counter[page] += 1

    for _ in range(n - 1):
        probability = transition_model(corpus, page, damping_factor)
        page_names = list(probability.keys())
        pageranks = list(probability.values())

        page = random.choices(page_names, weights=pageranks, k=1)[0]
        counter[page] += 1
````

## iterate_pagerank
The iterate_pagerank function calculates PageRank by updating the values repeatedly until they stop changing by more than a small threshold. Initially, every page is given an equal rank of 1 / n. Then for each page, a new rank is computed by starting with a base value of (1 - damping_factor) / n and then adding contributions from every other page that links to it. If a page has no outgoing links, we treat it as if it links to every page.This loop sums the contributions from all pages that could potentially link to the page we're evaluating. The process is repeated until every page's rank changes by less than 0.001. The final stable PageRank values are then returned.

```` python
rank = (1 - damping_factor) / n
for linking_pages in corpus:
    links = corpus[linking_pages]
    if len(links) == 0:
        rank += damping_factor * (pagerank[linking_pages] / n)
    elif page in links:
        rank += damping_factor * (pagerank[linking_pages] / len(links))
````
## Output and Conclusions
### output
````
PageRank Results from Sampling (n = 1000000)
  1.html: 0.2192
  2.html: 0.4288
  3.html: 0.2205
  4.html: 0.1314
PageRank Results from Iteration
  1.html: 0.2202
  2.html: 0.4289
  3.html: 0.2202
  4.html: 0.1307
````
The output shows two sets of PageRank values for the same set of pages. The first set, “PageRank Results from Sampling,” was computed by simulating a random web surfer who visited 1,000,000 pages. In this simulation, the chance of landing on a page was counted over all the visits, so for example, page 2.html was visited about 42.88% of the time. The second set, “PageRank Results from Iteration,” was obtained by repeatedly applying the PageRank formula until the rank values stopped changing significantly. Both methods produced very similar numbers.

This similarity tells us that both the random sampling method and the iterative calculation are converging on the same idea of page importance. In this case, page 2.html is clearly the most popular, with a rank around 0.4289. Pages 1.html and 3.html are almost equally important, each with a rank of roughly 0.220, while page 4.html has a lower rank of about 0.130. These values mean that if you were randomly surfing this set of pages, you would land on page 2.html nearly 43% of the time, on pages 1.html and 3.html about 22% of the time each, and on page 4.html about 13% of the time.

Both methods — sampling and iteration — provide us with ways to estimate how important or popular a page is within the corpus. The sampling method mimics the behavior of a random web surfer, while the iterative method solves for a fixed point in the PageRank equations until the values settle down.