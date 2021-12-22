# YouTube Comment Vote Reader 
Vote reader made for an interactive online Youtube series, where viewers can vote in the comments for which contestant in the show they want to eliminate, save, etc. 
These votes are in the format \[x\], where x is any character in the roman alphabet, upper- or lowercase. These votes can be anywhere in the comment.

This uses the YouTube Data API v3, and uses the [sample code in the official CommentThread documentation](https://developers.google.com/youtube/v3/docs/commentThreads/list) as a baseline.

Example input, from newest to oldest:
```
USER             | COMMENT
------------------------------------
cooldude917      | "I vote for [A]!"
catsilovecats    | "[B][C][D][A][D]lol"
bjorkfan123      | "x[B]f"
catsilovecats    | "[C]"
gopacersgo       | "[B]"
zzxxzz           | "(b)"
letsgoooooo      | "[b]"
```

Some things to note:

- The user "catsilovecats" made two comments with votes, so the newer comment (higher on the list) was used for their vote. In this newer comment, they also attempted to vote multiple times. With the design choices we made here, their *last vote* will be counted, so this comment will count as a vote for \[D\]. 
- The user "zzxxzz" voted in an unaccepted format, so it is not counted.
- The user "letsgooooooo" made a vote with a lowercase letter. It is valid and counts as a vote for \[B\].

So, this input would yield the following results:

```
[A] got 1 vote
[B] got 3 votes
[C] got 0 votes
[D] got 1 vote
```
