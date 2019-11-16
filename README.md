# Bayesian Networks

Implementation for bayesian network with 

  - Enumeration
  - Rejection Sampling
  - Likelihood Weighting

```python
{
    'netid': "burglary",
    'query': ('B', 'j,m'),
    'result': {True: 0.28, False: 0.72},
    'samples': 10000,
}
RejectionSampling().run(testcase)
LikelihoodWeighting().run(testcase)
Enumeration().run(testcase)
```
