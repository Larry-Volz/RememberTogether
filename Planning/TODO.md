

# To Do for capstone
- [ ] Do delete post route
- [ ] If somone types in a non-existant departed.id in search box -> flash
- [ ] Do delete mrmorial route
- [ ] Fix it so Date and time start and pictures re-populate for edit_memorial
- [ ] Set up css for a flash including dismissable and add flash to each page
- [ ] Set up server:
  - [ ] install linux on desktop
  - [ ] Re-set up Apache or Gunicorn
  - [ ] get dynamic IP address/domain name setup
- [ ] Or do on Heroku
- [x] Fix time and date fields so they are working
- [x] Do new gateway look-up/main page for memorials
- [x] Change /dos to /
- [x] Do main page for virtual memorials
- [x] Add link to go back to virtual-memorials
- [x] Set up upload image functionality
- [x] Make an edit memorial sequence
- [ ] Make register or login and return to where started: pass through starting URL and then send back to there (via ginger and python) once form is finished

# To Do before demo
- [ ] Change memorial pages so it's just "virtual-memorial.net/firstname-lastname" so it searches by that instead of id and set up an intermediate page that makes sure it's the right one only if there is more than one person with that name
- [ ] Add a "are you sure you want to cancel your changes and go back" confirmation box with the edit -> 'cancel' button
- [ ] Make admin page
    - [ ] Have to sign into it
    - [ ] offer 3 levels
        - [ ] need memorial code to view.  Need admin code to edit or post
        - [ ] need memorial code to view and post.  Need admin code to edit
        - [ ] anyone w/name can view.  Need admin code to edit or post
        - [ ] anyone w/name can view or post.  Need admin code to edit.
- [ ] make an "Add a post" link in menu that only shows up if someone is signed in
- [ ] Make an "add a post" linke under each post when they are signed in
- [ ] Fix datetime so it works in every timezone
- [ ] Make an "edit this post" link next to user's posts only when they are signed in and only for their own posts
- [ ] Make a "delete post" with check on it to make sure they mean to do it

# To Do before going live
- [ ] Create ability to upload picture from facebook
- [ ] Fix it so it does not duplicate a picture in the files - if there is another of the same name maybe give opportunity to rename it?
- [ ] Get back-up hard drive and set up chron jobs
- [ ] Have another address/contact info for the wake and/or reception if not at the funeral home
- [ ] add e-mail to the funeral home data
- [ ] Change lookup form to be onsubmit rather than on button click
- [ ] Create databases/relationships with participating (?) funeral homes? need for integration with streaming?
  - [ ] set up a "forget password" section that will email them a new password if needed.  and/or double security(?)
    - [ ] link to page -> enter password
    - [ ] set up flask password
- [ ] Do crap-tons of testing
- [ ] Set up a "contact us" page
- [ ] Set up a donations page (?)
- [ ] Set up an auto-resize system (through API/picresize?)

# Later functionality
- [ ] Add ability to upload videos or youtube videos
- [ ] Add ability to measure how much data is uploaded
- [ ] Learn about AWS for lots of content/etc.
- [ ] 