# googleHashCode2020

# Problem description 

## Books
There are B different books with IDs from 0 to B–1. Many libraries can have a copy of the same book, but we only need to scan each book once.
Each book is described by one parameter: the score that is awarded when the book is scanned.

## Libraries
There are L different libraries with IDs from 0 to L–1. Each library is described by the following parameters:
* the set of books in the library,
* the time in days that it takes to sign the library up for scanning,
* the number of books that can be scanned each day from the library once the library is signed up.

## Time
There are D days from day 0 to day D–1. The first library signup can start on day 0.
D–1 is the last day during which books can be shipped to the scanning facility.

## Library signup
Each library has to go through a signup process before books from that library can be shipped.
Only one library at a time can be going through this process (because it involves lots of planning and on-site visits at
the library by logistics experts): the signup process for a library can start only when no other signup processes are running.
The libraries can be signed up in any order.
Books in a library can be scanned as soon as the signup process for that library completes (that is, on the first day immediately
after the signup process, see the figure below). Books can be scanned in parallel from multiple libraries.
