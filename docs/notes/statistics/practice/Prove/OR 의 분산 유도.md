
$$
\begin{align}
\hat \theta \approx N(\theta, Var(\hat{\theta}))\;\rightarrow\;g(\hat{\theta}) \approx N(g(\theta), [g'(\theta)]^2Var(\hat{\theta}))
\end{align}
$$
#### 2×2 분할표 설정
|     | 사건 발생    | 사건 미발생   | 합계       |
| --- | -------- | -------- | -------- |
| 1군  | $n_{11}$ | $n_{12}$ | $n_{1+}$ |
| 2군  | $n_{21}$ | $n_{22}$ | $n_{2+}$ |

#### 모형 가정
- 독립성: 두 군은 서로 독립
- 이항분포: $n_{11} \sim Bin(n_{1+}, p_1)$, $n_{21} \sim Bin(n_{2+}, p_2)$
- 위험률 추정치: $\hat{p_1} = \frac{n_{11}}{n_{1+}}$, $\hat{p_2} = \frac{n_{21}}{n_{2+}}$
- OR 추정치: $\hat{OR} = \frac{\hat{p_1}/(1-\hat{p_1})}{\hat{p_2}/(1-\hat{p_2})} = \frac{n_{11} \times n_{22}}{n_{12} \times n_{21}}$
- 로그 변환 함수: $g(p_1, p_2) = \ln OR = \ln\left(\frac{p_1/(1-p_1)}{p_2/(1-p_2)}\right)$

로그 변환을 통해 정규 근사 · 선형결합을 기대할 수 있다.

- $Var(\hat{p_i}) = \frac{p_i(1-p_i)}{n_{i+}}$ (각 확률변수의 분산)
- $Cov(\hat{p_1}, \hat{p_2}) = 0$ (독립성 가정)
- $OR = \frac{p_1/(1-p_1)}{p_2/(1-p_2)}$ (모집단 오즈비)
- $\hat{OR} = \frac{\hat{p_1}/(1-\hat p_1)}{\hat{p_2}/(1-\hat p_2)}$ (표본 오즈비)
- $\ln \hat{OR} = \ln (\hat{p_1}/(1-\hat p_1)) - \ln (\hat{p_2}/(1-\hat p_2))$
	- $n_{ij} > 0, 0<p_i<1$

$(\hat{p_1}, \hat{p_2})^T$가 근사적으로 정규분포를 따른다고 하자:
$$(\hat{p_1}, \hat{p_2})^T \sim N\left((p_1, p_2)^T, \Sigma\right)$$

$$g(p_1, p_2) = \ln \frac{p_1}{1-p_1} - \ln \frac{p_2}{1-p_2}$$


여기서 공분산 행렬은:
$$\Sigma = \begin{bmatrix}
Var(\hat{p_1}) & Cov(\hat{p_1}, \hat{p_2}) \\
Cov(\hat{p_1}, \hat{p_2}) & Var(\hat{p_2})
\end{bmatrix}$$

독립성 가정에 의해 $Cov(\hat{p_1}, \hat{p_2}) = 0$이므로 :
$$\Sigma = \begin{bmatrix}
\frac{p_1(1-p_1)}{n_{1+}} & 0 \\
0 & \frac{p_2(1-p_2)}{n_{2+}}
\end{bmatrix}$$

$$\nabla g = \begin{bmatrix}
\frac{\partial g}{\partial p_1} \\
\frac{\partial g}{\partial p_2}
\end{bmatrix}
=
\begin{bmatrix}
\frac{1}{p_1}+\frac{1}{1-p_1} \\
-(\frac{1}{p_2}+\frac{1}{1-p_2})
\end{bmatrix}
=
\begin{bmatrix}
\frac{1}{p_1(1-p_1)} \\
-\frac{1}{p_2(1-p_2)}
\end{bmatrix}
$$

델타 방법에 의해 :
$$Var(g(\hat{p_1}, \hat{p_2})) \approx \nabla g^T \Sigma \nabla g$$
$$
\begin{align}
Var(\ln \hat{OR}) &\approx \begin{bmatrix} \frac{1}{p_1(1-p_1)}, -\frac{1}{p_2(1-p_2)} \end{bmatrix} \begin{bmatrix} Var(\hat p_1) & 0 \\ 0 & Var(\hat p_2) \end{bmatrix} \begin{bmatrix} \frac{1}{p_1(1-p_1)} \\ -\frac{1}{p_2(1-p_2)} \end{bmatrix}
\end{align}
$$
$$
\begin{align}
Var(\ln \hat{OR})\quad&\approx\quad
\begin{bmatrix}
\frac{1}{p_1(1-p_1)}Var(\hat p_1), & -\frac{1}{p_2(1-p_2)}Var(\hat p_2)
\end{bmatrix}
\begin{bmatrix}
\frac{1}{p_1(1-p_1)} \\
-\frac{1}{ p_2(1-p_2)}
\end{bmatrix} \\
&\;=\;(\frac{1}{p_1(1-p_1)})^2Var(\hat p_1)\;+\;(\frac{1}{p_2(1-p_2)})^2Var(\hat p_2)
\end{align}
$$$$
\begin{align}
Var(\ln \hat{OR})\;\approx\;\frac{1}{n_{1+}p_1(1-p_1)}\;+\;\frac{1}{n_{2+}p_2(1-p_2)}
\end{align}
$$
- $p_1\;\rightarrow\;\hat p_1\;=\;n_{11}/n_{1+}$
- $p_2\;\rightarrow\;\hat p_2\;=\;n_{21}/n_{2+}$
- $\hat{Var}(\ln \hat{OR})$ : $Var(\ln \hat{OR})$ 근사 추정값

이를 추정치로 치환하면:
$$
\begin{align}
\hat{Var}(\ln \hat{OR})\;\approx\;\frac{1}{n_{1+}\hat p_1(1-\hat p_1)}\;+\;\frac{1}{n_{2+}\hat p_2(1-\hat p_2)}
\end{align}
$$
$$
\begin{align}
\frac{1}{n_{1+}\hat p_1(1- \hat p_1)}\;=\;\frac{1}{n_{1+}\;*\;\frac{n_{11}}{n_{1+}}*\frac{n_{12}}{n_{1+}}}\;=\;\frac{n_{1+}}{n_{11}n_{12}}\;=\;\frac{1}{n_{11}}+\frac{1}{n_{12}}
\end{align}
$$
$$
\begin{align}
\frac{1}{n_{2+}\hat p_2(1-\hat p_2)}\;=\;\frac{1}{n_{21}}\;+\;\frac{1}{n_{22}}
\end{align}
$$
$$
\begin{align}
&\therefore \hat{Var}(\ln \hat{OR})\;=\;\frac{1}{n_{11}}+\frac{1}{n_{12}}+\frac{1}{n_{21}}+\frac{1}{n_{22}}
\end{align}
$$
$$
\begin{align}
SE(\ln \hat{OR})\;=\;\sqrt{\frac{1}{n_{11}}+\frac{1}{n_{12}}+\frac{1}{n_{21}}+\frac{1}{n_{22}}}
\end{align}
$$

OR 의 95% 신뢰구간은 다음과 같이 구할 수 있다.

$exp(x)=e^x$, $SE=\sqrt{\hat{Var} (\ln{OR})}$
$z$ 는 평균이 0이고 분산이 1 인 정규 분포를 따른다.


$$
\begin{align}
Z\;=\;{{\ln \hat{OR} -\ln {OR}} \over SE(\ln \hat{OR})}\quad\approx\quad N(0,1)
\end{align}
$$

양측 95% 신뢰구간은 $P(-z \leq Z \geq z)=0.95$
표준정규분포에서 양 끝단 0.025 근방에 존재하는 z 값은 다음과 같다.
$z_{0.975}=1.96$
$$
\begin{align}
CI(95\%)\;&=\;[exp(\ln \hat{OR}-z_{0.975}\sqrt{\hat Var(\ln \hat{ OR})}),exp(\ln \hat {OR}+z_{0.975}\sqrt{\hat Var(\ln \hat{OR})})] \\\\
&=\;[e^{ln{\hat {OR}}}e^{-z_{0.975}SE},e^{ln{\hat {OR}}}e^{z_{0.975}SE}] \\\\
&=\;[\hat {OR}\;e^{-z_{0.975}SE},\hat {OR}\;e^{+z_{0.975}SE}]
\end{align}
$$