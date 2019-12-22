Here are all entities necessary for running simple election.
 
1. Parameters naming  
Usually we characterize an election with:
    * _n - number of voters_
    * _m - number of candidates_
    * _k - size of committee_ 

    ```python
    n = 5
    m = 3
    k = 2
    ```
2. Preferences Profile 
Depending on given rule, preferences are defined in an ordinal or approval model.
Single preference always represents single voter.
    * Ordinal preferences
    ```python
    from pmp.preferences import Ordinal
    orders = [
        [1, 2, 0],
        [2, 1, 0],
        [2, 0, 1],
        [1, 2, 0],
        [1, 0, 2]
    ]
    
    preferences = [Ordinal(o) for o in orders]

    ```
    * Approval preferences
     ```python
    from pmp.preferences import Approval
    approves = [
        [0, 1, 2],
        [0, 1],
        [1],
        [1, 2],
        [0, 2]
    ]
    
    preferences = [Approval(a) for a in approves]

    ```
    * Profile  
    With defined preferences next step is to create preferences profile. It consists of candidates and preferences lists.
     ```python
    from pmp.preferences import Profile
    candidates = [0, 1, 2]
    
    profile = Profile(candidates, preferences)
    ```
3. Finding committee  
You always compute winning committee with an instance of a rule. It has method `find_committee`
with two obligatory parameters - _k_ and _profile_, both which we have defined earlier.
With one instance you can compute results for different values of _k_ or for different profiles.

```python
from pmp.rules import SNTV

sntv = SNTV()
committee = sntv.find_committee(k, profile)
```

   
