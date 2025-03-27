# Explanation of the Implementation

This project involves modeling the inheritance of a gene and its effect on a trait (such as hearing impairment) using a Bayesian network. The goal was to determine the probability distributions for each person’s gene copies (0, 1, or 2) and whether they exhibit the trait. In this task, we only had to implement three functions: **joint_probability**, **update**, and **normalize**.

## joint_probability
The joint_probability function calculates the probability of a particular configuration in which each person in the family has a specified number of gene copies and either does or does not exhibit the trait. For every individual, the function first determines how many copies of the gene they are assumed to have by checking membership in the one_gene and two_genes sets. If a person is not in either set, then they have zero copies. The function then checks whether the individual’s parents are listed. For persons without parental data, it simply uses the unconditional probability from PROBS["gene"]:
````python
if mother is None and father is None:
    gene_prob = PROBS["gene"][gene_count]
````
For individuals with parents, the probability is computed based on the chance that each parent passes on a gene copy. This involves considering the mutation probability – if a parent has two copies, the gene is passed on with probability 1 - PROBS["mutation"]; if they have one copy, the chance is 0.5; and if they have none, only a mutation could result in a pass. After computing the probability for the gene inheritance, the function also factors in the probability of showing (or not showing) the trait, given the gene count:
````python
trait_prob = PROBS["trait"][gene_count][has_trait]
p *= gene_prob * trait_prob
````

## update
The update function’s role is to take the joint probability computed for a specific configuration and add it to the cumulative probability distributions for each person. The function iterates over every person and first determines the gene count (0, 1, or 2) based on whether the person is in one_gene or two_genes. It then checks whether the person is assumed to exhibit the trait. The following lines show how the respective probabilities are updated:
````python
probabilities[person]["gene"][gene_count] += p
probabilities[person]["trait"][has_trait] += p
````

This ensures that after considering all possible configurations, the probabilities dictionary accumulates the total probability for each gene and trait outcome for every individual.

## normalize
The normalize function ensures that the probability distributions for each person sum to 1 by scaling the probabilities appropriately. For each person, the function first calculates the total sum of the probabilities in the gene distribution and then divides each gene probability by this total. For example, normalization of the gene probabilities is performed with:
````python
gene_total = sum(probabilities[person]["gene"].values())
for gene_count in probabilities[person]["gene"]:
    probabilities[person]["gene"][gene_count] /= gene_total
````
A similar approach is applied to the trait probabilities. This step is crucial because, after the update phase, the values are raw totals accumulated over many configurations. Normalization converts these totals into valid probability distributions while preserving their relative proportions.

## Summary
These functions work together to iterate through every possible scenario of gene inheritance and trait exhibition, combine the probabilities for each individual event into an overall joint probability, update cumulative distributions accordingly, and finally normalize these distributions so that they represent proper probabilities.