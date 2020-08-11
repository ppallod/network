# Network

Network is a Web Application built using Django framework that allows users to create new posts, follow other users and like posts.     

### New Post

Users that are logged in can visit `/new` route by using `New Post` button to be able to create a new post through a text based form. Submitting this form creates a new post which can be viewed in `All Posts`. 

### All Posts

The `All Posts` link in the navigation bar takes the user to the route `/allposts` which lets the user see all posts from all users in reverse chronological order. Each post on this page shows: username of the poster, the actual text from the post, timestamp as well as the number of likes the post have got.

### Profile Page

Clicking on any username loads that user's profile page which displays number of followers, number of users that user follows as well as all their posts in reverse chronological order. Moreover, if some other user visits their page, they are provided with a button to either follow or unfollow this user.

### Following

Using the `Following` button from navigation bar, the user is directed to the route `/following` which displays all the posts made by users that the current user follows. This link behaves similar to `All Posts` but the only difference is that it shows limited number of posts.

### Pagination

This django project uses `Paginator` class to display only 10 posts at a time. When a user visits either `All Posts`, `Following` or `Profile Page`, they are displayed 10 posts at a time. They can use the next of previous buttons to view all the remaining posts.

### Edit Post

When a user clicks `edit` button on any of their posts, they are presented with a `textarea` which lets them edit their posts. On clicking the save button, the original text of the posts is modified by the updated text.

### Like and Unlike

Every post contains a `like` or `unlike` which lets the users to toggle between whether they like or unlike posts.
