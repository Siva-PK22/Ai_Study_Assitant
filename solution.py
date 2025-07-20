class Solution:
    def processStr(self, s: str) -> str:
        result = ""
        
        for char in s:
            if char.islower():  # Lowercase English letter
                result += char
            elif char == '*':   # Remove last character
                if result:
                    result = result[:-1]
            elif char == '#':   # Duplicate current result
                result = result + result
            elif char == '%':   # Reverse current result
                result = result[::-1]
        
        return result


# Test cases
if __name__ == "__main__":
    solution = Solution()
    
    # Example 1
    test1 = "a#b%*"
    result1 = solution.processStr(test1)
    print(f"Input: {test1}")
    print(f"Output: '{result1}'")
    print(f"Expected: 'ba'")
    print()
    
    # Example 2
    test2 = "z*#"
    result2 = solution.processStr(test2)
    print(f"Input: {test2}")
    print(f"Output: '{result2}'")
    print(f"Expected: ''")
    print()
    
    # Additional test case
    test3 = "abc*#%"
    result3 = solution.processStr(test3)
    print(f"Input: {test3}")
    print(f"Output: '{result3}'")
