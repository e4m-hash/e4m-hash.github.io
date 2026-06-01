#### 델타방법으로 근사
$$
\begin{align}
\hat \theta \approx N(\theta, Var(\hat{\theta}))\;\rightarrow\;g(\hat{\theta}) \approx N(g(\theta), [g'(\theta)]^2Var(\hat{\theta}))
\end{align}
$$
### RR 의 분산 유도
#### 2×2 분할표 설정
|     | 사건 발생    | 사건 미발생   | 합계       |
| --- | -------- | -------- | -------- |
| 1군  | $n_{11}$ | $n_{12}$ | $n_{1+}$ |
| 2군  | $n_{21}$ | $n_{22}$ | $n_{2+}$ |

#### 모형 가정
- **독립성**: 두 군은 서로 독립
- **이항분포**: $n_{11} \sim Bin(n_{1+}, p_1)$, $n_{21} \sim Bin(n_{2+}, p_2)$
- **위험률 추정치**: $\hat{p_1} = \frac{n_{11}}{n_{1+}}$, $\hat{p_2} = \frac{n_{21}}{n_{2+}}$

- $Var(\hat{p_i}) = \frac{\hat p_i(1-\hat p_i)}{n_{i+}}$ (이항분포의 분산)
- $RR = \frac{p_1}{p_2}$ (모표본 위험비)
- $\hat{RR} = \frac{\hat{p_1}}{\hat{p_2}}$ (표본 위험비)

- $\ln RR\;=\;g(p_1\;,\;p_2)$
- $\ln \hat {RR}\;=\;g(\hat p_1\;,\;\hat p_2)$ 
- $\hat p_i\;=\;{n_{i1} \over n_{i+}}$
- $Var(\hat p_i)\;=\;{p_i(1-p_i) \over p_{i+}}$
- $Cov(\hat p_1,\hat p_2)=0$ : 독립성 가정
- $g(p_1,p_2)=\ln p_1 - \ln p_2$
- $\nabla g = [ {1 \over p_1}, -{1 \over p_2} ]^T$

##### 델타 방법
$(\hat{p_1}, \hat{p_2})^T$가 근사적으로 이변량 정규분포를 따른다고 하자:
$$(\hat{p_1}, \hat{p_2})^T \sim N_2\left((p_1, p_2)^T, \Sigma\right)$$

여기서 공분산 행렬은:
$$\Sigma = \begin{bmatrix}
Var(\hat{p_1}) & Cov(\hat{p_1}, \hat{p_2}) \\
Cov(\hat{p_1}, \hat{p_2}) & Var(\hat{p_2})
\end{bmatrix}$$

독립성 가정에 의해 $Cov(\hat{p_1}, \hat{p_2}) = 0$이므로:
$$\Sigma = \begin{bmatrix}
\frac{p_1(1-p_1)}{n_{1+}} & 0 \\
0 & \frac{p_2(1-p_2)}{n_{2+}}
\end{bmatrix}$$
$g(p_1, p_2) = \ln p_1 - \ln p_2 = \ln(p_1/p_2)$라 하면:

$$\nabla g = \begin{bmatrix}
\frac{\partial g}{\partial p_1} \\
\frac{\partial g}{\partial p_2}
\end{bmatrix} = \begin{bmatrix}
\frac{1}{p_1} \\
-\frac{1}{p_2}
\end{bmatrix}$$

$$Var(g(\hat{p_1}, \hat{p_2})) \approx \nabla g^T \Sigma \nabla g$$
$$
\begin{align}
Var(\ln \hat{RR}) &\approx \begin{bmatrix} \frac{1}{p_1} & -\frac{1}{p_2} \end{bmatrix} \begin{bmatrix} Var(\hat p_1) & 0 \\ 0 & Var(\hat p_2) \end{bmatrix} \begin{bmatrix} \frac{1}{p_1} \\ -\frac{1}{p_2} \end{bmatrix}
\end{align}
$$
$$
\begin{align}
Var(g(\hat p_1 , \hat p_2))\quad&\approx\quad
\begin{bmatrix}
\frac{1}{p_1}Var(\hat p_1) &-\frac{1}{p_2}Var(\hat p_2)
\end{bmatrix}
\begin{bmatrix}
\frac{1}{p_1} \\
-\frac{1}{ p_2}
\end{bmatrix} \\
&\;=\;(\frac{1}{p_1})^2Var(\hat p_1)\;+\;(\frac{1}{p_2})^2Var(\hat p_2)
\end{align}
$$
$$
\begin{align}
Var(\ln \hat{RR})\;\approx\;\frac{1-p_1}{n_{1+}p_1}\;+\;\frac{1-p_2}{n_{2+}p_2}
\end{align}
$$
- $p_1\;\rightarrow\;\hat p_1\;=\;n_{11}/n_{1+}$
- $p_2\;\rightarrow\;\hat p_2\;=\;n_{21}/n_{2+}$
- $\hat Var(\ln RR)$ : $Var (\ln \hat{RR})$ 의 추정값

$$
\begin{align}
\hat{Var}(\ln \hat{RR})\;\approx\;\frac{1-\hat p_1}{n_{1+}\hat p_1}\;+\;\frac{1-\hat p_2}{n_{2+}\hat p_2}
\end{align}
$$
$$
\begin{align}
\frac{1-\hat p_1}{n_{1+}\hat p_1}\;=\;\frac{1-\frac{n_{11}}{n_{1+}}}{n_{1+}\;*\;\frac{n_{11}}{n_{1+}}}\;=\;\frac{n_{1+}-n_{11}}{n_{1+}n_{11}}\;=\;\frac{1}{n_{11}}-\frac{1}{n_{1+}}
\end{align}
$$
$$
\begin{align}
\frac{1-\hat p_2}{n_{2+}\hat p_2}\;=\;\frac{1}{n_{21}}\;-\;\frac{1}{n_{2+}}
\end{align}
$$

$$
\begin{align}
&\hat Var(\ln RR)\;=\;\frac{1-\hat p_1}{n_{1+}\hat p_1}\;+\;\frac{1-\hat p_2}{n_{2+}\hat p_2} \\
&\therefore \hat Var(\ln RR)\;=\;\frac{1}{n_{11}}-\frac{1}{n_{1+}}+\frac{1}{n_{21}}-\frac{1}{n_{2+}}
\end{align}
$$


$$
\begin{align}
SE(\ln{\hat {RR}})\;=\;\sqrt{\frac{1}{n_{11}}-\frac{1}{n_{1+}}+\frac{1}{n_{21}}-\frac{1}{n_{2+}}}
\end{align}
$$

중심극한정리에 의해 표본크기가 충분히 클 때:
- $\hat{p_1} \sim N(p_1, \frac{p_1(1-p_1)}{n_{1+}})$
- $\hat{p_2} \sim N(p_2, \frac{p_2(1-p_2)}{n_{2+}})$
$$\ln \hat{RR} \approx N\left(\ln RR, \hat{Var}(\ln \hat{RR}\right)$$
$$\ln \hat{RR} \approx N\left(\ln RR, \frac{1-p_1}{n_{1+}p_1} + \frac{1-p_2}{n_{2+}p_2}\right)$$

표준화 :
$$Z = \frac{\ln \hat{RR} - \ln RR}{SE(\ln \hat{RR})} \sim N(0,1)$$