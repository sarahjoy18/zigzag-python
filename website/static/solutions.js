/*
Author: Sarah Joy Lambino
Date Created: Nov 27, 2021
Last Modified: Nov 28, 2021

The following codes are for:
 1. Determining if a string is a palindrome
 2. Determining the longest palindromic substring
 3. Slicing string into set of palindromes

 Related modules: index.html
*/

/*
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
*/
function isPalindrome(input_string) {
    //remove the spaces in the input string first
    input_string = input_string.replaceAll(' ', '');

    //change all letters to lowercase
    input_string = input_string.toLowerCase();

    //separate the input string per letter and put it into an array
    var letters = input_string.split('');

    //reverse the elements inside the array and store it in an array variable
    var reversed_array = letters.reverse();

    //join the array elements (reversed) into a new string
    var reversed_string = reversed_array.join('');

    //compare the reversed string with the input string 
    //if it has the same value, then it is considered a palindrome
    //return the result of comparison
    return input_string === reversed_string;

    //The code above could also be optimized into a one line of code 
    //like this
    // return input_string == input_string.replaceAll(' ', '').toLowerCase().split('').reverse().join('');
}



/*
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
*/
function getLongestPalindrome(input_string) {
    //first, declare the variables that we want to compute using this function

    var longest_palindrome = ""; //will contain the value of the longest palindrome
    var best_length = 0; //will contain the length of the longest palindrome
    var left_pointer = 0;
    var right_pointer = 0;

    //remove the spaces in the input string
    input_string = input_string.replaceAll(' ', '');

    //store the total length of the input string with no spaces in a variable
    //we will use it later multiple times
    var total_length = input_string.length;


    //loop thru the letters of the input string
    //set each letter as the center pointer
    for (center = 0; center < total_length; center++) {

        //check if total_length is even or odd
        if (total_length % 2 == 0) {
            //if even
            //check it from pair of letters from the center then outward
            left_pointer = center;
            right_pointer = center + 1;

        } else {
            //if odd
            //check it from the centermost letter then outward
            left_pointer = center - 1;
            right_pointer = center + 1;

        }

        //start checking outward increment the distance from the center by 1
        for (distance = 1; distance < total_length; distance++) {

            //check if the pointers are within the range of the input string
            //this will save time, in case the center pointer doesn't have a valid prefix or suffix 
            //because the left pointer or right pointer might have exceeded the input string
            if (left_pointer >= 0 || right_pointer < total_length) {

                //set the value of the current substring
                var current_substring = input_string.substring(left_pointer, right_pointer + 1);

                //check if the current substring is a palindrome, reuse the function created in Level 1 Challenge
                //compare if it has greater length than the currently considered 'best length'
                if (isPalindrome(current_substring) && best_length < current_substring.length) {

                    //declare it as the best length and the longest palindrome
                    best_length = current_substring.length;
                    longest_palindrome = current_substring;
                }
            }

            //keep moving the pointers outward
            left_pointer--;
            right_pointer++;
        }
    }

    //after going thru all the letters of the input string
    //return the value of the currently considered 'longest palindrome'
    return longest_palindrome;
}


/*
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


*/
function getPalindromeCuts(input_string) {
    //first, declare the variables that we want to compute using this function
    var palindromes = []; //will contain all the best palindrome cuts within the  input string
    var remaining_letters = []; // will contain all the letters that are not palindrome and those not yet checked if palindrome
    var sorted_palindromes = []; //will contain the sorted palindrome cuts based on the input string


    //first, remove the spaces in the input string
    input_string = input_string.replaceAll(' ', '');

    //copy the value of input string to the remaining letters
    //initially, all letters are not yet checked
    remaining_letters = input_string;

    //loop thru the input string and check the best palindrome cuts, from the beginning to end of the string
    for (i = 0; i < input_string.length; i++) {
        //recursive checking of the possible best cuts in the remaining letters
        //use the function created in the Level 2 Challenge
        var palindrome = getLongestPalindrome(remaining_letters);

        //check if there is a palindrome within the remaining_letters
        if (palindrome) {
            //if the has a palindrome, add it in the array of palindromes
            palindromes.push(palindrome);

            //remove that palindrome cut from the remaining letters
            remaining_letters = remaining_letters.replaceAll(palindrome, '');
        }
    }



    //sort the saved palindromes from the array based on its position in the input string
    $.each(palindromes, function(key, value) {
        var position_in_string = input_string.lastIndexOf(value);
        sorted_palindromes[position_in_string] = value;
    });

    //include the remaining letters from the input string that are not palindromes
    if (remaining_letters.length > 0) {
        //sort the remaining_letters from the array based on its position in the input string
        $.each(remaining_letters.split(''), function(key, value) {
            var position_in_string = input_string.lastIndexOf(value);
            sorted_palindromes[position_in_string] = value;
        })
    }

    //make sure that the elements of the sorted_palindrome is not empty
    sorted_palindromes = sorted_palindromes.filter(Boolean);

    //return the value of the currently considered 'best palindrome cuts' inside the string
    //return how many cuts are there and display the sorted palindromes array
    return (sorted_palindromes.length - 1) + ' <code>' + sorted_palindromes.join(' | ') + '</code>';
}