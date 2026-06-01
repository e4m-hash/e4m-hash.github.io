# LaTeX 수식 지원

MathJax를 사용해 LaTeX 수식을 렌더링합니다.

인라인 수식은 이렇게 표시됩니다: $f(x) = x^2$. 입력은 `$f(x) = x^2$` 처럼 `$...$`로 감쌉니다.

블록 수식은 별도 줄에 `$$...$$`를 사용합니다.

```
$$
F(x) = \int^a_b \frac{1}{2}x^4
$$
```

위 입력은 아래처럼 렌더링됩니다.

$$
F(x) = \int^a_b \frac{1}{2}x^4
$$
# 연산자 · 관계성 기호

|      $\leq$      |      $\geq$       |          $<$          |        $>$         |
| :--------------: | :---------------: | :-------------------: | :----------------: |
|       $=$        |      $\neq$       |        $\nleq$        |      $\ngeq$       |
|     $\cong$      |     $\equiv$      |        $\sim$         |     $\approx$      |
|   $\doteqdot$    |     $\times$      |          $+$          |        $-$         |
|      $\div$      |      $\cdot$      |        $\ast$         |       $\pm$        |
|      $\mp$       |      $\circ$      |       $\oplus$        |     $\otimes$      |
|     $\odot$      |    $\bigcirc$     |      $\bigoplus$      |    $\bigotimes$    |
|    $\bigodot$    |     $\propto$     |       $\cdots$        |      $\dots$       |
|    $\because$    |   $\therefore$    |       $\forall$       |     $\exists$      |
|      $\in$       |     $\subset$     |      $\subseteq$      |      $\notin$      |
|    $\supset$     |    $\supseteq$    |     $\subsetneq$      |    $\supsetneq$    |
|  $\not\subset$   |   $\not\supset$   |    $\not\subseteq$    |  $\not\supseteq$   |
|   $\emptyset$    |   $\varnothing$   |       $\oslash$       |       $\cap$       |
|      $\cup$      |      $\vert$      |      $\parallel$      |       $\bot$       |
|      $\top$      |     $\vdots$      |       $\ddots$        |      $\circ$       |
|    $\bullet$     |      $\neq$       |       $\wedge$        |       $\vee$       |
|   $\leftarrow$   |   $\rightarrow$   |   $\leftrightarrow$   |     $\mapsto$      |
|   $\Leftarrow$   |   $\Rightarrow$   |   $\Leftrightarrow$   | $\leftrightarrows$ |
|     $\prod$      |      $\sum$       |        $\int$         |    $\oint_{C}$     |
|    $\uparrow$    |   $\downarrow$    |      $\Uparrow$       |    $\Downarrow$    |
| $\Longleftarrow$ | $\Longrightarrow$ | $\Longleftrightarrow$ |                    |

# 글자꼴 기호

| $\alpha$   | $\beta$  | $\gamma$   | $\delta$   |
| ---------- | -------- | ---------- | ---------- |
| $\epsilon$ | $\zeta$  | $\eta$     | $\theta$   |
| $\iota$    | $\kappa$ | $\lambda$  | $\mu$      |
| $\nu$      | $\xi$    | $\omicron$ | $\pi$      |
| $\rho$     | $\sigma$ | $\tau$     | $\upsilon$ |
| $\phi$     | $\chi$   | $\psi$     | $\omega$   |
| $\Gamma$   | $\Delta$ | $\Theta$   | $\Lambda$  |
| $\Xi$      | $\Pi$    | $\Sigma$   | $\Upsilon$ |
| $\Phi$     | $\Psi$   | $\Omega$   | $\nabla$   |
### 로마자
I
II
III
IV
V
VI
VII
VIII
IX
X
# 화살표

| 기호  | 수식                  | 기호    | 수식                   |
| --- | ------------------- | ----- | -------------------- |
| ←   | \leftarrow          | ⟵     | \longleftarrow       |
| →   | \rightarrow         | ⟶     | \longrightarrow      |
| ↑   | \uparrow            | ↰     | \Lsh                 |
| ↓   | \downarrow<br>      | ↱     | \Rsh                 |
| ⇐   | \Leftarrow          | ⟸<br> | \Longleftarrow       |
| ⇒   | \Rightarrow         | ⟹     | \Longrightarrow      |
| ⇐   | \Leftarrow          | ↢     | \leftarrowtail       |
| ⇒   | \Rightarrow         | ↣     | \rightarrowtail      |
| ⇑   | \Uparrow            | ↩     | \hookleftarrow       |
| ⇓   | \Downarrow          | ↪     | \hookrightarrow      |
| ↼   | \leftharpoonup      | ↞     | \twoheadleftarrow    |
| ⇀   | \rightharpoonup     | ↠     | \twoheadrightarrow   |
| ⇃   | \downharpoonleft    | ⇋     | \leftrightharpoons   |
| ↿   | \upharpoonleft      | ⇌     | \rightleftharpoons   |
| ↽   | \leftharpoondown    | ↶     | \curvearrowleft      |
| ⇁   | \rightharpoondown   | ↷     | \curvearrowright     |
| ↾   | \upharpoonright     | ⇆     | \leftrightarrows     |
| ⇂   | \downharpoonright   | ⇄     | \rightleftarrows     |
| ⇇   | \leftleftarrows     | ↺     | \circlearrowleft     |
| ⇉   | \rightrightarrows   | ↻     | \circlearrowright    |
| ⇈   | \upuparrows         | ⇚     | \Lleftarrow          |
| ⇊   | \downdownarrows     | ⇛     | \Rrightarrow         |
| ↫   | \looparrowleft      | ↔     | \leftrightarrow      |
| ↬   | \looparrowright     | ⇔     | \Leftrightarrow      |
| ↚   | \nleftarrow         | ⇍     | \nLeftarrow          |
| ⟷   | \longleftrightarrow | ⟺     | \Longleftrightarrow  |
| ↛   | \nrightarrow        | ⇏     | \nRightarrow         |
| ↕   | \updownarrow        | ⇕     | \Updownarrow         |
| ↮   | \nleftrightarrow    | ⇎     | \nLeftrightarrow     |
| ↦   | \mapsto             | ⟼     | \longmapsto          |
| ⇝   | \rightsquigarrow    | ↭<br> | \leftrightsquigarrow |
| ↙   | \swarrow            | ↘     | \searrow             |
| ↖   | \nwarrow            | ↗     | \nearrow             |

# 다양한 함수

| $\sin$    | $\cos$     | $\tan$        | $\exp$  |     |
| --------- | ---------- | ------------- | ------- | --- |
| $\arcsin$ | $\arccos$  | $\arctan$     | $\log$  |     |
| $\ln$     | $\sec$     | $\csc$        | $\cot$  |     |
| $\sinh$   | $\cosh$    | $\tanh$       | $\coth$ |     |
| $\;$      | $\min$     | $\max$        | $\arg$  |     |
| $\inf$    | $\sup$     | $\det$        | $\lim$  |     |
| $\deg$    | $\sqrt{x}$ | $\sqrt[3]{x}$ | $\ker$  |     |

# 모자 씌우기

| $\dot{x}$   | $\ddot{x}$    | $\acute{x}$ | $\grave{x}$ |
| ----------- | ------------- | ----------- | ----------- |
| $\check{x}$ | $\breve{x}$   | $\tilde{x}$ | $\bar{x}$   |
| $\hat{x}$   | $\widehat{x}$ | $\vec{x}$   |             |

# 행렬


$$
\begin{matrix}
x & y \newline z & v
\end{matrix}
$$

$$
\begin{vmatrix}
x & y \newline z & v
\end{vmatrix}$$

$$
\begin{pmatrix}
x & y \newline z & v
\end{pmatrix}
$$

$$
\begin{bmatrix}
x & y \newline z & v
\end{bmatrix}
$$
# 경우 나누기

$$
\begin{cases}
    x, & x > 0 \newline
    0, & \text{Otherwise}
\end{cases}
$$


# 여러 줄의 방정식 쓰기

$$
\begin{aligned}
    y =& x^2 + x + 2x + 3 -2 \newline
    =& x^2 + 3x +1
\end{aligned}
$$

# 이항 계수

${\;\;n \choose k\;\;} \;=\; _{n}\mathrm{C}_{k}$

# 구분선

$$
\begin{aligned}
\hline
\end{aligned}
$$
# 글자색

<span style='background-color: #fab005'>노란형광펜</span>
<span style='background-color: #228be6'>파랑형광펜</span>
<span style='background-color: #e64980'>빨강형광펜</span>
<span style='background-color: #40c057'>초록형광펜</span>
<span style='background-color: #be4bdb'>보라형광펜</span>
<span style='background-color: #fd7e14'>주황형광펜</span>

<span style='color: #fab005'>노란형광펜</span>
<span style='color: #228be6'>파랑형광펜</span>
<span style='color: #e64980'>빨강형광펜</span>
<span style='color: #40c057'>초록형광펜</span>
<span style='color: #be4bdb'>보라형광펜</span>
<span style='color: #fd7e14'>주황형광펜</span>

