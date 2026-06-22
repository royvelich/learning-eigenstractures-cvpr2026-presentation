# Using shape descriptors (HKS) to find the functional map $C$

How descriptors such as the Heat Kernel Signature determine the functional map
$C$ between two shapes — the standard functional-maps pipeline
(Ovsjanikov et al., 2012).

---

## The core idea: descriptors must be preserved by the map

HKS is **intrinsic**, so corresponding points have (nearly) the same signature.
A descriptor *function* on shape $A$ should therefore be carried by $C$ onto the
matching descriptor function on shape $B$ — **without ever knowing the point
correspondence**. Descriptors give us functions we know should line up; that is
exactly the data needed to solve for $C$.

---

## Turning preservation into linear constraints on $C$

**1. Compute descriptors on both shapes.**
HKS evaluated at several time scales gives a *family* of functions:

$$
f_1^A,\dots,f_m^A \ \text{on } A,
\qquad
f_1^B,\dots,f_m^B \ \text{on } B,
$$

one per scale (in practice one also adds WKS, and landmark / region indicator
functions).

**2. Express each descriptor in its shape's eigenbasis.**
Take the coefficient vectors — the "coordinates" of each function in the LBO
eigenbasis:

$$
\mathbf{a}_i = \Phi_A^\top M_A\, f_i^A,
\qquad
\mathbf{b}_i = \Phi_B^\top M_B\, f_i^B .
$$

**3. Preservation becomes a linear relation.**
Corresponding descriptors must map to one another:

$$
C\,\mathbf{a}_i \approx \mathbf{b}_i \qquad \text{for every } i .
$$

Stack the coefficient vectors as columns of two matrices,
$\hat A = [\,\mathbf a_1 \cdots \mathbf a_m\,]$ and
$\hat B = [\,\mathbf b_1 \cdots \mathbf b_m\,]$:

$$
\boxed{\,C\,\hat A \approx \hat B\,}
$$

---

## Solve a tiny least-squares problem

We solve for the $K \times K$ entries of $C$ (with $K \approx 30$):

$$
C^\star = \arg\min_{C}\;
\underbrace{\big\lVert C\hat A - \hat B \big\rVert_F^2}_{\text{descriptors preserved}}
\;+\;
\alpha\,\underbrace{\big\lVert C\Lambda_A - \Lambda_B C \big\rVert_F^2}_{\text{commute with the Laplacian}} .
$$

- **First term — the data.** Comes directly from the descriptors
  (HKS, WKS, landmarks).
- **Second term — the structural prior.** $C$ should commute with the Laplacian
  eigenvalues. Since this penalizes entry $(i,j)$ by $\big(\lambda_i^B - \lambda_j^A\big)^2$,
  it drives off-diagonal entries to zero — this is **why $C$ comes out
  near-diagonal**, and it keeps the problem well-posed even with few descriptors.
- Often one also enforces **orthogonality** $C^\top C \approx I$ (for
  area-preserving, near-isometric maps).

Here $\Lambda_A = \operatorname{diag}(\lambda_1^A,\dots,\lambda_K^A)$ and
$\Lambda_B = \operatorname{diag}(\lambda_1^B,\dots,\lambda_K^B)$ are the diagonal
matrices of LBO eigenvalues of the two shapes.

---

## Where the commutativity term comes from

The term $\lVert C\Lambda_A - \Lambda_B C\rVert_F^2$ encodes the fact that an
isometry preserves the Laplacian, so its functional map must **commute** with it.

### 1. The Laplacian, in the eigenbasis, is diagonal

By definition the eigenfunctions diagonalize the operator,
$\Delta_A\varphi_k^A=\lambda_k^A\varphi_k^A$. So if $f=\sum_k a_k\varphi_k^A$ has
coefficients $\mathbf a$, then

$$
\Delta_A f=\sum_k a_k\,\Delta_A\varphi_k^A=\sum_k \lambda_k^A a_k\,\varphi_k^A .
$$

In coordinates, "apply $\Delta_A$" simply scales each coefficient by its
eigenvalue:

$$
\mathbf a \;\longmapsto\; \Lambda_A\,\mathbf a .
$$

So the matrix of $\Delta_A$ **in its own eigenbasis is the diagonal $\Lambda_A$**
(and likewise $\Delta_B \leftrightarrow \Lambda_B$ on $B$). The next subsection
derives this carefully.

#### Why $\Delta$ becomes the diagonal matrix $\Lambda$

This "multiply by $\Lambda$" is just the statement that **the Laplacian, written
in its own eigenbasis, is diagonal**, with the eigenvalues on the diagonal.

**Intuition.** The eigenfunctions are the Laplacian's *pure modes*: the equation
$\Delta\varphi_k=\lambda_k\varphi_k$ says $\Delta$ does not mix modes, it only
**stretches each mode by its own factor $\lambda_k$**. A general function is a
blend of modes with weights $a_k$; since $\Delta$ scales each mode independently,
every weight is rescaled $a_k\mapsto\lambda_k a_k$. No mixing $\Rightarrow$ the
action is diagonal — exactly like diagonalizing a matrix, where in the eigenbasis
the map becomes "scale each coordinate by its eigenvalue."

**Function-space derivation.** Apply $\Delta$ term by term, using linearity and
the eigenvalue equation:

$$
\Delta f=\Delta\!\Big(\sum_k a_k\varphi_k\Big)
=\sum_k a_k\,\Delta\varphi_k
=\sum_k a_k\,\lambda_k\,\varphi_k
=\sum_k (\lambda_k a_k)\,\varphi_k .
$$

The $k$-th coefficient of $\Delta f$ is therefore $\lambda_k a_k$, i.e.
$\mathbf a \xrightarrow{\ \Delta\ } \Lambda\,\mathbf a$.

**Discrete (mesh) derivation.** With mass matrix $M$ and stiffness matrix $L$,
the discrete Laplacian operator is $\Delta=M^{-1}L$, and the eigenproblem is

$$
L\,\varphi_k=\lambda_k\,M\,\varphi_k
\quad\Longleftrightarrow\quad
M^{-1}L\,\varphi_k=\lambda_k\,\varphi_k .
$$

Stacking eigenvectors as columns of $\Phi$ gives two facts:

$$
\Phi^\top M\,\Phi=I \quad(\text{$M$-orthonormal}),
\qquad
L\,\Phi=M\,\Phi\,\Lambda \quad(\text{eigenproblem}).
$$

A function has coefficients $\mathbf a=\Phi^\top M f$ and (in the span)
$f=\Phi\,\mathbf a$. The coefficients of $\Delta f$ are then

$$
\mathbf c
=\Phi^\top M\,(\Delta f)
=\Phi^\top M\,(M^{-1}L f)
=\Phi^\top L f
=\Phi^\top L\,\Phi\,\mathbf a
=\Phi^\top(M\Phi\Lambda)\,\mathbf a
=(\Phi^\top M\Phi)\,\Lambda\,\mathbf a
=\Lambda\,\mathbf a .
$$

The $M$ and $L$ collapse precisely because $\Phi$ is $M$-orthonormal and solves
the eigenproblem. So, in the eigenbasis, applying $\Delta$ is exactly
multiplication by $\Lambda$.

### 2. The map commutes with the Laplacian

The Laplacian is intrinsic: "diffuse on $A$, then transfer to $B$" equals
"transfer to $B$, then diffuse on $B$." As a commuting diagram on coefficient
vectors, for any $\mathbf a$:

$$
\underbrace{C\,(\Lambda_A\,\mathbf a)}_{\text{apply }\Delta_A\text{ on }A,\ \text{then map}}
\;=\;
\underbrace{\Lambda_B\,(C\,\mathbf a)}_{\text{map, then apply }\Delta_B\text{ on }B}.
$$

This must hold for **every** $\mathbf a$, so the vector drops out and leaves a
matrix identity:

$$
C\,\Lambda_A = \Lambda_B\,C
\qquad\Longleftrightarrow\qquad
C\Lambda_A - \Lambda_B C = 0 .
$$

That zero residual is what sits inside the norm — imposed as a *soft* penalty
$\lVert C\Lambda_A - \Lambda_B C\rVert_F^2$, since real shapes are only
near-isometric.

### 3. Why it forces $C$ near-diagonal (entrywise)

Both $\Lambda_A$ and $\Lambda_B$ are diagonal, so $C\Lambda_A$ scales **column**
$j$ by $\lambda_j^A$ while $\Lambda_B C$ scales **row** $i$ by $\lambda_i^B$.
Hence each entry of the residual is

$$
\big(C\Lambda_A - \Lambda_B C\big)_{ij} = C_{ij}\,\big(\lambda_j^A - \lambda_i^B\big),
$$

and the whole term is a **weighted penalty on the entries of $C$**:

$$
\lVert C\Lambda_A - \Lambda_B C\rVert_F^2
= \sum_{i,j} C_{ij}^{\,2}\,\big(\lambda_j^A - \lambda_i^B\big)^2 .
$$

- Where eigenvalues match ($\lambda_i^B \approx \lambda_j^A$, i.e. near the
  diagonal for near-isometric shapes) the weight is $\approx 0$, so $C_{ij}$ is
  **free**.
- Off the diagonal the eigenvalues differ, the weight is large, and $C_{ij}$ is
  **driven to zero**.

The weights grow as the eigenvalues spread apart, producing the characteristic
**funnel-shaped mask** — exactly the near-diagonal $C$ — and regularizing the
otherwise under-determined least-squares.

---

## Then refine (spectral ICP)

1. Recover a point map from $C$ — nearest neighbour in the $\Phi$ embeddings
   (the **delta-transport** step: push $\delta_p$ through $C$, read off the peak).
2. Re-estimate $C$ from the updated correspondence by **orthogonal Procrustes**.
3. Repeat until convergence.

---

## One-line summary

> Descriptors give the **data** $\big(C\hat A \approx \hat B\big)$, and
> Laplacian commutativity gives the **prior** (diagonal) — so solving for $C$ is
> a small linear least-squares problem, with **no combinatorial search** over
> point matchings.

The HKS fingerprints used to *describe* points are exactly the inputs that
*determine* the map $C$.

---

### Symbol reference

| Symbol | Meaning |
|---|---|
| $\Phi_A,\ \Phi_B$ | matrices of LBO eigenfunctions (columns) of shapes $A$, $B$ |
| $M_A,\ M_B$ | mass (area) matrices |
| $\Lambda_A,\ \Lambda_B$ | diagonal matrices of LBO eigenvalues |
| $f_i^A,\ f_i^B$ | the $i$-th descriptor function on each shape |
| $\mathbf a_i,\ \mathbf b_i$ | its coefficients in the eigenbasis |
| $\hat A,\ \hat B$ | descriptor coefficients stacked as columns |
| $C$ | the functional map ($K\times K$) |
