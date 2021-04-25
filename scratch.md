try:
        dates = dates['DATES']
    except:
        flash("Must enter a valid zip code")
        redirect ("flowers.html")