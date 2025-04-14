import math
import cmath

class QuadraticSolver:
    """
    A class to solve quadratic equations of the form ax^2 + bx + c = 0
    """
    
    @staticmethod
    def solve(a, b, c):
        """
        Solves the quadratic equation ax^2 + bx + c = 0
        
        Args:
            a (float): Coefficient of x^2
            b (float): Coefficient of x
            c (float): Constant term
            
        Returns:
            tuple or str: A tuple containing the roots of the equation,
                          or a string message for special cases
            
        Raises:
            ValueError: If inputs are not numeric
        """
        # Validate inputs
        if not all(isinstance(coef, (int, float)) for coef in [a, b, c]):
            raise ValueError("All coefficients must be numeric")
        
        # Handle special cases
        if a == 0:
            # Linear equation: bx + c = 0
            if b == 0:
                if c == 0:
                    return "Infinite solutions"  # 0 = 0
                else:
                    return "No solution"  # 0 = non-zero
            else:
                return (-c / b,)  # bx + c = 0 -> x = -c/b
        
        # Calculate the discriminant
        discriminant = b**2 - 4*a*c
        
        # Calculate roots based on discriminant
        if discriminant > 0:
            # Two distinct real roots
            root1 = (-b + math.sqrt(discriminant)) / (2*a)
            root2 = (-b - math.sqrt(discriminant)) / (2*a)
            return (root1, root2)
        elif discriminant == 0:
            # One real root (repeated)
            root = -b / (2*a)
            return (root, root)
        else:
            # Complex roots
            root1 = (-b + cmath.sqrt(discriminant)) / (2*a)
            root2 = (-b - cmath.sqrt(discriminant)) / (2*a)
            return (root1, root2)