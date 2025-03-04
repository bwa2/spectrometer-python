
def cal_formula(x1,lambda1,x2,lambda2):
    # Given data points
    x1, lambda1 = 7, 405  # UV
    x2, lambda2 = 174, 650  # IR

    # Compute 'a' (slope)
    a = (lambda2 - lambda1) / (x2 - x1)

    # Compute 'b' (intercept)
    b = lambda1 - a * x1

    print(f"Calibration Formula: λ = {a:.4f} * x + {b:.4f}")
    return a,b


