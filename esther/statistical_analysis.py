from scipy.stats import shapiro, wilcoxon

x = [-4.417970517, -2.757135585, -24.66272049, 5.878935787, 4.585321775, 5.560443914, 3.311377852]

shapiro_test = shapiro(x)

print(f"Shapiro-Wilk test statistic: {shapiro_test.statistic}, p-value: {shapiro_test.pvalue}")


y = [2.815316478, -4.096579438, -3.030676412, -0.350649756, -1.93732666, -3.27937074, 0.943779916]


shapiro_test = shapiro(y)


print(f"Shapiro-Wilk test statistic: {shapiro_test.statistic}, p-value: {shapiro_test.pvalue}")


wilcoxon_test = wilcoxon(x, y)

print(f"Wilcoxon test statistic: {wilcoxon_test.statistic}, p-value: {wilcoxon_test.pvalue}")



narrow_0001 = [-8.429597154, -25.70697531, -20.52558281, -10.30172977, 3.37612016, 2.229852978, 3.157790601]

shapiro_test = shapiro(narrow_0001)


print(f"Shapiro-Wilk test statistic: {shapiro_test.statistic}, p-value: {shapiro_test.pvalue}")

wilcoxon_test = wilcoxon(narrow_0001, y)

print(f"Wilcoxon test statistic: {wilcoxon_test.statistic}, p-value: {wilcoxon_test.pvalue}")


narrow_0005 = [-8.51, -9.97, -40.02, 0.83, 4.57, 2.16, 40.33]

shapiro_test = shapiro(narrow_0005)


print(f"Shapiro-Wilk test statistic: {shapiro_test.statistic}, p-value: {shapiro_test.pvalue}")

wilcoxon_test = wilcoxon(narrow_0005, y)

print(f"Wilcoxon test statistic: {wilcoxon_test.statistic}, p-value: {wilcoxon_test.pvalue}")