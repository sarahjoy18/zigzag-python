
""" Author: Sarah Joy Lambino
Date Created: Nov 28, 2021
Last Modified: Nov 28, 2021

The following codes are for:
 1. Determining if a string is a palindrome
 2. Determining the longest palindromic substring
 3. Slicing string into set of palindromes

 Related modules: /website/templates/index.html """

from os import name
from flask import Blueprint, render_template, request, flash
import json

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/level1')
def level1():
    return render_template('level1.html')


@views.route('/level2')
def level2():
    return render_template('level2.html')


@views.route('/level3')
def level3():
    return render_template('level3.html')


"""
Solution for Level 1 Challenge

Expected parameters: input_string

Sample Input:
input_string = "Nurses run"

Sample Output:
true

Time Complexity:
O(1) - Constant time, no matter how big the input string is, it takes the same amount of time to get the palindrome

Space Complexity:
O(1) - Constant space
"""


@views.route("/isPalindrome/<input_string>", methods=["POST", "GET"])
def isPalindrome(input_string):

    # compare the reversed string with the input string
    # if it has the same value, then it is considered a palindrome
    # return the result of comparison as json (response to ajax request)
    result = (input_string == input_string[::-1])
    return json.dumps(result)


"""
Solution for Level 2 Challenge

Expected parameters: input_string


Sample Input:
input_string = "Banana"

Sample Output:
anana


Sample Input:
input_string = "Madama"

Sample Output:
madam

Time Complexity:
O(n^2) Quadratic for determining and checking if the current_substring is a palindrome with the best length

Space Complexity: 
O(1) - Constant Space for the longest_palindrome
"""


@views.route("/getLongestPalindrome/<input_string>", methods=["POST", "GET"])
def getLongestPalindrome(input_string):
    # first, declare the variables that we want to compute using this function

    # will contain the value of the longest palindrome
    longest_palindrome = ""

    # will contain the length of the longest palindrome
    best_length = 0

    # remove the spaces in the input string
    input_string = input_string.replace(' ', '')
    total_len = len(input_string)

    # loop thru the letters of the input string
    # set each letter of the input string as the center
    for center in range(total_len):
        # check if total_length is even or odd
        if total_len % 2 == 0:
            # if even
            # check it from pair of letters from the center then outward
            left_pointer = center
            right_pointer = center+1
        else:
            # if odd
            # check it from the centermost letter then outward
            left_pointer = center+1
            right_pointer = center+1

        # start checking outward increment the distance from the center by 1
        for distance in range(total_len):

            # check if the pointers are within the range of the input string
            # this will save time, in case the center pointer doesn't have a valid prefix or suffix
            # because the left pointer or right pointer might have exceeded the input string
            if left_pointer >= 0 or right_pointer < total_len:
                if(left_pointer < 0):
                    current_substring = input_string[0:right_pointer+1]
                elif(right_pointer >= total_len):
                    current_substring = input_string[left_pointer:total_len]
                else:
                    current_substring = input_string[left_pointer:right_pointer+1]

                # check if the current substring is not a single character
                if(len(current_substring) > 1):
                    # check if the current substring is a palindrome, reuse the function created in Level 1 Challenge
                    # compare if it has greater length than the currently considered 'best length'
                    # another checking is if it has the same length but positioned in the input string before the longest palindrome
                    if (isPalindrome(current_substring) == "true") and ((len(current_substring) > best_length) or (len(current_substring) > best_length and (input_string.rfind(current_substring) < input_string.rfind(longest_palindrome)))):
                        longest_palindrome = current_substring
                        best_length = len(current_substring)

            # keep moving the pointers outward
            left_pointer -= 1
            right_pointer += 1

    # after going thru all the letters of the input string
    # return the value of the currently considered 'longest palindrome'
    return json.dumps(longest_palindrome)


"""
Solution for Level 3 Challenge

Expected parameters: input_string

Sample Input:
input_string = "noonabbada"

Sample Output:
3 // noon | abba | d | a

Time Complexity:
O(n^2) for the possible substrings (remaining_letters) and checking the best palindrome cuts
O(n) for sorting the palindromes

=O(n^2 x n)
=O(n^3)

Space Complexity
O(n^2) for the recursion on remaining_letters
O(n) for the palindrome cuts (stored in 1 dimensional array)

=O(n^2 x n)
=O(n^3)
"""


@ views.route("/getPalindromeCuts/<input_string>", methods=["POST", "GET"])
def getPalindromeCuts(input_string):
    palindromes = []  # will contain all the palindrome cuts
    remaining_letters = []  # will contain all the remaining letters per checking

    # will contain the sorted palindrome cuts and the remaining letters
    sorted_palindromes = []

    # remove the spaces from the input string
    input_string = input_string.replace(' ', '')

    # copy all the letters from the input string - initial value
    remaining_letters.append(input_string)

    # loop thru all the letters of the input string
    for i in range(len(input_string)):
        # recursive checking as long as there are remaining letters
        if(i < len(remaining_letters)):
            # get the possible best palindrome cut
            # use the function created in the Level 2 Challenge
            # remove the surrounding qoutes since it is return as json
            palindrome = getLongestPalindrome(
                remaining_letters[i]).replace('"', '')

            # check if there's a palindrome in the remaining letters
            if (len(palindrome) > 1):
                # remove the palindrome from the set of remaining letters
                # needed to save the remaining letters in list because strings in python are immutable
                new_remaining_letters = remaining_letters[i].replace(
                    palindrome, '')

                # store the remaining letters for the next checking
                remaining_letters.append(new_remaining_letters)

                # store the palindrome in palindromes array to be sorted later
                position_in_string = input_string.rfind(palindrome)
                palindromes.append([position_in_string, palindrome])
            else:
                # else stop the recursive checking
                break

    # add the remaining letter based on their position in the input string
    for remaining_letter in remaining_letters[-1]:
        position_in_string = input_string.rfind(remaining_letter)
        palindromes.append([position_in_string, remaining_letter])

    # sort the palindromes based on their position in the input string
    for palindrome in enumerate(sorted(palindromes, key=lambda palindromes: palindromes[0]), start=1):
        sorted_palindromes.append(palindrome[1][1])

    # set the value of result
    # return the value of the currently considered 'best palindrome cuts' inside the string
    # return how many cuts are there and display the sorted palindromes array
    result = '<b>'+str(len(sorted_palindromes)-1)+'</b> // ' + \
        ' | '.join(sorted_palindromes)

    # return the result markup to ajax request
    return json.dumps(result)
