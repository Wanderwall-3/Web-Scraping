from os import system

from playwright.sync_api import sync_playwright
import mysql.connector as mysql

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,   # IMPORTANT
        args=["--start-maximized"]
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        viewport=None
    )
    
    
    try:
        try:
            global con
            con = mysql.connect(
                host="localhost",
                user="root",
                password="wanderwall420.,.",
                database="movie"
            )
            cur = con.cursor()
        except Exception as e:
            print("Database connection failed:", e)
            system.exit(1)

        page = context.new_page()
        page.goto("https://www.imdb.com/chart/top/?view=detailed", timeout=60000)

        print("Title:", page.title())
        page.wait_for_selector("li.ipc-metadata-list-summary-item", timeout=60000)

        # page.wait_for_timeout(8000)

        movies = page.query_selector_all("li.ipc-metadata-list-summary-item")
        
        for movie in movies:
            movie_name = movie.query_selector("h3").inner_text()
            year_of_release = movie.query_selector(".dli-title-metadata-item").inner_text()
            rating = movie.query_selector(".ipc-rating-star--rating").inner_text()
            story = movie.query_selector(".ipc-html-content-inner-div").inner_text()
            director = movie.query_selector(".ipc-link--base").inner_text()
            print(movie_name, year_of_release,rating, director)
            cur.execute("insert into movie_data (name, year_of_release, rating, story, director) values (%s, %s, %s, %s, %s)", (movie_name, year_of_release, rating, story, director))
            
        print("Movies found:", len(movies))

        con.commit()
        cur.close()
        con.close()
        
        browser.close()
        
        
    except Exception as e:
        print("An error occurred:", e)
        con.rollback()
        browser.close()