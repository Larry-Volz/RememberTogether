

# To Do for capstone
- [ ] Do main page for virtual memorials
- [ ] Change /dos to /
- [ ] Do new gateway look-up/main page for memorials
- [ ] Add link to go back to virtual-memorials
- [ ] Set up server:
  - [ ] install linux on desktop
  - [ ] Re-set up Apache or Gunicorn
  - [ ] get dynamic IP address/domain name setup
- [ ] Or do on Heroku
- [ ] Set up upload image functionality

# To Do before demo
- [ ] Change memorial pages so it's just "virtual-memorial.net/firstname-lastname" so it searches by that instead of id and set up an intermediate page that makes sure it's the right one only if there is more than one person with that name
- [ ] Make admin page
    - [ ] Have to sign into it
    - [ ] offer 3 levels
        - [ ] need memorial code to view.  Need admin code to edit or post
        - [ ] need memorial code to view and post.  Need admin code to edit
        - [ ] anyone w/name can view.  Need admin code to edit or post
        - [ ] anyone w/name can view or post.  Need admin code to edit.
- [ ] make an "Add a post" link in menu that only shows up if someone is signed in
- [ ] Make an "add a post" linke under each post when they are signed in
- [ ] Make an "edit this post" link next to user's posts only when they are signed in and only for their own posts
- [ ] Make a "delete post" with check on it to make sure they mean to do it

# To Do before going live
- [ ] Get back-up hard drive and set up chron jobs
- [ ] Change lookup form to be onsubmit rather than on button click
- [ ] Create databases/relationships with participating (?) funeral homes? need for integration with streaming?
  - [ ] set up a "forget password" section that will email them a new password if needed.  and/or double security(?)
    - [ ] link to page -> enter password
    - [ ] set up flask password
- [ ] Do crap-tons of testing
- [ ] Set up a "contact us" page
- [ ] Set up a donations page (?)
- [ ] Fix datetime so it works in every timezone
- [ ] Set up an auto-resize system (through API/picresize?)