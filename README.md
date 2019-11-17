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

enum = bayesian_networks.Enumeration()
results = enum.run(testcase)
bayesian_networks.print_result(results, showcolors=True)

rejection = bayesian_networks.RejectionSampling()
results = rejection.run(testcase)
bayesian_networks.print_result(results, showcolors=True)

weighting = bayesian_networks.LikelihoodWeighting()
results = weighting.run(testcase)
bayesian_networks.print_result(results, showcolors=True)
```
