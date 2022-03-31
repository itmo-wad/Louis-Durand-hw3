# Homework 3 Louis Durand

This is my submission for Homework 3


## Description of what I've done
I have implemented a blog website in which a user can register and login into his account.
The website can handle multi user and displays all blogs at root page with the author but ONLY if the privacy of blog is public.
A user can see all his blogs (Public and Private) in `/posts` My posts button on root.
From there he can create a new blog and choose it's privacy setting.

A user that is not logged in will not be able to create blogs but just see all public ones.

## Routes
- `/register` - Create an account
- `/login` - Login with your name and your password
- `/disconnect` - Disconnect from your account
- `/` - View all public posts if connected or not
- `/posts` - View my own posts private and public, only if logged in
- `/add-blog` - Add a blog and choose it's privacy

## Checklist

Basic part: Implement blog website features:
- [x] A public "Story" page where everyone can see all blog posts
- [x] Only authenticated user can add new post
--------
Advanced part:
- [x] Post can have a theme image (and author name if your app is multi-user)
- [x] Add visibility of the post (public/private) so guest can see only public posts (authenticated user can see his/her own private/public posts)
- [ ] Deploy your app using docker-compose (docker-compose.yaml will be evaluated)
--------
Challenging part:
- [ ] Implement editing and deleting post feature
- [ ] "Story" page automatically check and update for new posts


## How to run the Web Application

`python app.py`
or 
`flask run`