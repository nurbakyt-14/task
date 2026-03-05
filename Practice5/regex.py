import re

# 1. 'a' followed by zero or more 'b'
text1 = "abbb a acb abb"
pattern1 = r'ab*'
print("1:", re.findall(pattern1, text1))


# 2. 'a' followed by two to three 'b'
text2 = "ab abb abbb abbbb"
pattern2 = r'ab{2,3}'
print("2:", re.findall(pattern2, text2))


# 3. lowercase letters joined with underscore
text3 = "hello_world this_is a_test example"
pattern3 = r'[a-z]+_[a-z]+'
print("3:", re.findall(pattern3, text3))


# 4. one uppercase followed by lowercase
text4 = "Hello World Python Is Fun"
pattern4 = r'[A-Z][a-z]+'
print("4:", re.findall(pattern4, text4))


# 5. 'a' followed by anything ending with 'b'
text5 = "acb a123b ab axxxb"
pattern5 = r'a.*b'
print("5:", re.findall(pattern5, text5))


# 6. replace space, comma, dot with colon
text6 = "Hello, world. How are you"
result6 = re.sub(r'[ ,.]', ':', text6)
print("6:", result6)


# 7. snake_case to camelCase
snake = "hello_world_python"
parts = snake.split('_')
camel = parts[0] + ''.join(word.title() for word in parts[1:])
print("7:", camel)


# 8. split string at uppercase letters
text8 = "HelloWorldPython"
result8 = re.split(r'(?=[A-Z])', text8)
print("8:", result8)


# 9. insert spaces between capital words
text9 = "HelloWorldPython"
result9 = re.sub(r'(?<!^)(?=[A-Z])', ' ', text9)
print("9:", result9)


# 10. camelCase to snake_case
camel10 = "HelloWorldPython"
snake10 = re.sub(r'(?<!^)(?=[A-Z])', '_', camel10).lower()
print("10:", snake10)