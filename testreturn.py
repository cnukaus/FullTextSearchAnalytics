# A Python program to to return multiple 
# values from a method using tuple
 
# This function returns a tuple
def fun():
    str = "geeksforgeeks"
    x   = 20
    return str, x;  # Return tuple, we could also
                    # write (str, x)
 
# Driver code to test above method
str, x = fun() # Assign returned tuple
print(str)
print(x)