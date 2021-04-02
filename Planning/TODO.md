

# To Do for capstone
- [ ] Do main page for virtual memorials
- [ ] Add link to go back to virtual-memorials
- [ ] Do new gateway look-up/main page for memorials
- [ ] Set up server:
  - [ ] install linux on desktop
  - [ ] Re-set up Apache or Gunicorn
  - [ ] get dynamic IP address/domain name setup
- [ ] Or do on Heroku

# To Do before demo
- [ ] Change memorial pages so it's just "virtual-memorial.net/firstname-lastname" so it searches by that instead of id and set up an intermediate page that makes sure it's the right one only if there is more than one person with that name
- [ ] Make admin page
    - [ ] Have to sign into it
    - [ ] offer 3 levels
        - [ ] need memorial code to view.  Need admin code to edit or post
        - [ ] need memorial code to view and post.  Need admin code to edit
        - [ ] anyone w/name can view.  Need admin code to edit or post
        - [ ] anyone w/name can view or post.  Need admin code to edit.

# To Do before going live
- [ ] Get back-up hard drive and set up chron jobs
  - [ ] set up a "forget password" section that will email them a new password if needed.  and/or double security(?)
    - [ ] link to page -> enter password
    - [ ] set up flask password
- [ ] Do crap-tons of testing