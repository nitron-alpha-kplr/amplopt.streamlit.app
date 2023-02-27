import streamlit as st

title = "Tip #4: If-Then"


def run():
    st.markdown(
        """
    Assume that production of a specific item $i$ costs $u_i$ per unit, but there is an additional fixed charge of $w_i$ if we produce item $i$ at all.
    """
    )

    st.image("static/images/SetupCosts.png")

    st.markdown(
        r"""
    For instance, $w_i$ could be the cost of setting up a production plant, initial cost of equipment etc.

    Then the cost of producing $x_i$ units of product $i$ is given by the discontinuous function:
    $$
    \begin{split}c_i(x_i) = \left \{ \begin{array}{ll}w_i + u_i x_i, & x_i > 0\\0, & x_i=0.\end{array}\right .\end{split}
    $$

    Using AMPL MP-based or Constraint Programing drivers, we can minimize the total production cost of $n$ products with the following objective function:

    ```
    minimize TotalCost:
        sum {i in 1..n} (u[i]*x[i] + if x[i]>0 then w[i]);
    ```

    For older MIP drivers, a linearized model is needed. It can be constructed using auxiliary binary variables and connecting constraints as follows:

    ```
    var z{1..n} binary;

    minimize TotalCost:
        sum {i in 1..n} (w[i]*z[i] + u[u]*x[i]);

    s.t. ConnectBinaries {i in 1..n}:
        x[i] <= M*z[i];     ## Use a big-M constraint to enforce z[i]=0 ==> x[i]=0
    ```

    Full example of a facility location model with setup costs:
    ```
    # Set up the sets
    set I := 1..10;  # potential facility locations
    set J := 1..50;  # customers

    # Set up the parameters
    param w {i in I} = Normal(60, 20);  # fixed costs for each facility
    param u {i in I, j in J} = Uniform(10, 30);  # transportation costs from each facility to each customer
    param d {j in J} = Uniform(5, 10);  # demand for each customer

    # Set up the decision variables
    var x {i in I, j in J} >= 0 <= d[j];  # amount of demand for customer j satisfied by facility i

    # Set up the objective function
    minimize total_cost:
        sum {i in I, j in J} u[i,j]*x[i,j] +
            sum {i in I} if sum {j in J} x[i,j] > 0 then w[i];

    # Set up the constraints
    subject to demand_constraint {j in J}:
        sum {i in I} x[i,j] = d[j];
    ```

    Linearized model:
    ```
    # Set up the sets
    set I := 1..10;  # potential facility locations
    set J := 1..50;  # customers

    # Set up the parameters
    param w {i in I} = Normal(60, 20);  # fixed costs for each facility
    param u {i in I, j in J} = Uniform(10, 30);  # transportation costs from each facility to each customer
    param d {j in J} = Uniform(5, 10);  # demand for each customer

    # Set up the decision variables
    var z {i in I} binary;  # whether or not to build a facility at location i
    var x {i in I, j in J} >= 0;  # amount of demand for customer j satisfied by facility i

    # Set up the objective function
    minimize total_cost:
        sum {i in I} w[i]*z[i] + sum {i in I, j in J} u[i,j]*x[i,j];

    # Set up the constraints
    subject to demand_constraint {j in J}:
        sum {i in I} x[i,j] = d[j];
    subject to capacity_constraint {i in I}:
        sum {j in J} x[i,j] <= z[i] * sum {j in J} d[j];
    ```

    Running both models with HiGHS:
    ```
    ampl: option solver highs;
    ampl: solve;
    HiGHS 1.4.0: optimal solution; objective 4796.760641
    0 simplex iterations
    1 branching nodes
    ```

    Running both models with Gurobi:
    ```
    ampl: option solver gurobi;
    ampl: solve;
    Gurobi 10.0.0: optimal solution; objective 4796.760641
    44 simplex iterations
    1 branching nodes
    ```

    Documentation on the expression-valued `if-then-else` operator can be found in the [MP Modeling Guide](https://amplmp.readthedocs.io/en/latest/rst/model-guide.html).
        """
    )