import streamlit as st

title = "Tip #3: Alldifferent"


def run():
    st.markdown(
        """
    Consider the N-Queens problem: **How can N queens be placed on an NxN chessboard so that no two of them attack each other?** [ Solve it on [Google Colab](https://colab.research.google.com/github/ampl/amplcolab/blob/master/authors/glebbelov/miscellaneous/nqueens.ipynb)! ]
    """
    )

    st.image("static/images/nqueens.png")

    st.markdown(
        """
    - Constraint `alldiff` enforces a set of integer variables to take distinct values.
    ```
    s.t. OneJobPerMachine: 
    alldiff {j in JOBS} MachineForJob[j];
    ```

    - `alldiff` can be used conditionally:
    ```
    s.t. VisitOnce {j in GUESTS}:
    IsHost[j] = 0 ==> alldiff {t in TIMES} Visit[j,t];
    ```

    - Older MIP drivers need a manual reformulation of `alldiff` with binary variables:
    ```
    s.t. OneMachinePerJob {j in JOBS}:
    sum {k in MACHINES} Assign[j,k] = 1;

    s.t. OneJobPerMachine {k in MACHINES}:
    sum {j in JOBS} Assign[j,k] = 1;
    ```


    ## Back to the N-Queens problem

    New MP Library-based, as well as Constraint Programming drivers, accept `alldiff` directly:
    ```
    param n integer > 0;             # N queens
    var Row {1..n} integer >= 1 <= n;
    s.t. row_attacks: alldiff ({j in 1..n} Row[j]);
    s.t. diag_attacks: alldiff ({j in 1..n} Row[j]+j);
    s.t. rdiag_attacks: alldiff ({j in 1..n} Row[j]-j);
    ```

    A reformulated model for older MIP drivers:
    ```
    param n integer > 0;
    var X{1..n, 1..n} binary; 
    # X[i,j] is one if there is a queen at (i,j); else zero

    s.t. column_attacks {j in 1..n}:
        sum {i in 1..n} X[i,j] = 1;

    s.t. row_attacks {i in 1..n}:
        sum {j in 1..n} X[i,j] = 1;

    s.t. diagonal1_attacks {k in 2..2*n}:
        sum {i in 1..n, j in 1..n: i+j=k} X[i,j] <= 1;

    s.t. diagonal2_attacks {k in -(n-1)..(n-1)}:
        sum {i in 1..n, j in 1..n: i-j=k} X[i,j] <= 1;
    ```

    Running both models with HiGHS:
    ```
    ampl: include nqueens.mod;
    ampl: let n := 8;
    ampl: option solver highs;
    ampl: solve;
    HiGHS 1.4.0: optimal solution
    0 simplex iterations
    1 branching nodes
    Objective = find a feasible point.
    ```

    Another problem can be modeled with `alldiff`: [Sudoku. A GUI-based Colab Notebook](https://colab.research.google.com/github/ampl/amplcolab/blob/master/authors/mapgccv/miscellaneous/sudoku.ipynb).

    MP Documentation on the `alldiff` operator can be found at [https://amplmp.readthedocs.io/](https://amplmp.readthedocs.io/).
        """
    )