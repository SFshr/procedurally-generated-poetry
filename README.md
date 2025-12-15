# procedurally-generated-poetry

Possibly the most overengineered way to generate lines of nonsense. 

This project uses Markov chains and constraints derived from the Gutenberg Poetry corpus to try to approximate its contents.

## Example Outputs

wide the love not thus half rounding

his to boast to my dreamd us

destruction doom of the still good for in at night

queen to our worth in show thee low

## How It Works

This model uses a version of the model synthesis constraint solving algorithm to create lines of text that satisfy a set of adjacency constraints derived from the corpus. Probabilities for the next word to be chosen are given by the stationary distribution of a Markov chain in which each word selection is a state. The transition probability to a new selection state is calculated by its word's frequency in the corpus and the probability of its word class occupying its sentence position if the current selection state were realised. Hypothetically this should allow for interesting non chronological generation patterns but word selections tend to propagate out from the point in the sentence where the initial selection was made.