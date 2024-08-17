# RL-MDP-TicTacToe

I trained a reinforcement learning agent to play Tic Tac Toe by modeling it as a Markov Decision Process and optimizing the policy through Value and Policy Iteration. 


<img src='/assets/example.png' width=400>

A state is a nonuplets with values of 0, 1 or 2. 0 represents an emtpy space on the board. 1 is the circle player and 2 is the x player. The computer agent will always be the circle player and the human player will be the x player. 

The reward function of the computer agent maps a state to either 1, -1 or 0. 1 for when there are three circles in a row and -1 when there are 3 x's in a row, and 0 for all other states. 

$$
 \begin{equation}
 R(s') =
   \left\lbrace\begin{array}{lr}
       1, & \text{3 x's in a row} \\
       -1, & \text{3 o's in a row} \\
       0, & \text{otherwise}
    \end{array}\right.
 \end{equation}
$$

Since the reward function is not stochastic, the MDP prob function is given by 

$$
P(s'|s,a) = 1/ \text{number of possible moves}
$$

And the value function is given by 

$$
V_\pi = E_\pi [\sum_k r_k] = \sum P(s'|s,a) \times [R(s') + \gamma V_\pi(s')]
$$

## Value Iteration
For Value Iteration we iteratively update the value function through this formula until it converges:

$$
V(s) = \max_a \sum_{s'} P(s'|s,a) \times (R(s') + \gamma V(s'))
$$

The algorithm can be described as following: 

* Initialize $\epsilon > 0$  to determine convergence condition
* Initialize $V(s)$, for all $s \in S^+$ to be 0
* Loop
    * $\Delta \leftarrow 0 $
    * Loop for each $s \in S^+$
      * $v \leftarrow V(s)$
      * $V(s) \leftarrow \max_a \sum_{s'} P(s'|s,a) \times (R(s') + \gamma V(s'))$
      * $\Delta \leftarrow max(\Delta, \lvert v - V(s) \rvert) $
* Until $\Delta < \epsilon$

After having an accurate estimate of the value function we can extract the optimal policy

$$
\pi(s,a) = \underset{a}{\text{argmax}} \sum_{s'} P(s'|s,a) \times (R(s') + \gamma V(s'))
$$


## Policy Iteration

Policy iteration is a two step process that involves first policy evalution and then policy improvement. The main difference is that in policy iteration we first initalize the policy to be arbitrary. And then in the evaluation step instead of using the action that maximizes the value function, we use our current policy. We then iteratively evaluate that policy and then improve it. 

* Initialize $V(s) \in \mathbb{R}$ and $\pi(s) \in A(s)$ arbitrarily for all $s \in S$
  
Policy Evaluation

* Loop
     * $\Delta \leftarrow 0 $
     * * Loop for each $s \in S^+$
       * $v \leftarrow V(s)$
       * $V(s) \leftarrow \sum_{s'} P(s'|s,\pi(s)) \times (R(s') + \gamma V(s'))$
       * $\Delta \leftarrow max(\Delta, \lvert v - V(s) \rvert) $
* Until $\Delta < \epsilon$

Policy Improvement

* $\text{policy-stable} \leftarrow true $
* For each $s \in S$
    * $\text{old-action} \leftarrow \pi(s)$
    * $V(s) \leftarrow \underset{a}{\text{argmax}} \sum_{s'} P(s'|s,a) \times (R(s') + \gamma V(s'))$
    * if $\text{old-action} \neq \pi(s)$, then $\text{policy-stable} \leftarrow false$
* If policy-stable then stop and return $V \approx v_*$, and $\pi \approx \pi_*$; else go to policy evaluation


