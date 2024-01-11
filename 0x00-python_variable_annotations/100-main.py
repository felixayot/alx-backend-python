#!/usr/bin/env python3

safe_first_element =  __import__('100-safe_first_element').safe_first_element

print(safe_first_element.__annotations__)
print(safe_first_element(['James', 'Bond', 'Felix', 'Manchester United']))
print(safe_first_element('Felix'))
print(safe_first_element([1000000000]))
