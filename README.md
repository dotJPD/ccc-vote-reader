# YouTube Comment Vote Reader 
Vote reader made for an interactive online Youtube series, where viewers can vote in the comments for which contestant in the show they want to eliminate, save, etc. 
These votes are in the format [x], where x is any character in the roman alphabet, upper- or lowercase. These votes can be anywhere in the comment.

This uses the YouTube Data API v3, and uses the [sample code in the official CommentThread documentation](https://developers.google.com/youtube/v3/docs/commentThreads/list) as a baseline.

Example input, from newest to oldest:
```
Commenter 1   "I vote for [A]!"
Commenter 2   "[B][C][D][A][D]lol"
Commenter 3   "x[B]f"
Commenter 2   "[C]"
Commenter 4   "[B]"
Commenter 5   "(b)"
Commenter 6   "[b]"
```

Would yield the following results:

```
[A] got 1 vote
[B] got 3 votes
[C] got 0 votes
[D] got 1 vote
```
