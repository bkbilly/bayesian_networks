# Bayesian Networks

Implementation for bayesian network with 

  - Enumeration
  - Rejection Sampling
  - Likelihood Weighting

```python
import bayesian_networks

testcase = {
    'netid': "burglary",
    'query': ('B', 'j,m'),
    'result': {True: 0.28, False: 0.72},
    'samples': 10000,
}

bayesian_networks.Enumeration().run(testcase)
bayesian_networks.RejectionSampling().run(testcase)
bayesian_networks.LikelihoodWeighting().run(testcase)
```
