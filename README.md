# UIL Enhanced Archives

A searchable archive of past UIL competition results

## Features

  - **Archives**:
    - Takes the benefits of the old archive system being all on one page and combines it with the recency of speechwire.
    - Able to export as a csv file to import into spreadsheets.

  - **Virtual Contest**:
    - Able to combine multiple archives into one mega contest.
    - Able to add your own scores to add yourself to the past contest.
    - Use Case: See how you stack up against all the districts in your region or all the regions in your state
    - Use Case: See how one school in 4A stacks up against all the schools in 5A
    - Use Case: See how you would have done at a meet many years ago.

  - **Search for a Competitor or School**:
    - See all instances of a competitor or a school in past years.

  - **Live Results**:
    - See what results for what events have been submitted for a particular year.
    - Green if results are posted. Red if they aren't

  - **Academic Alignments**:
    - Type in a school name and see what district and region they're in as well as the other schools in their district

## Architecture

  - **Frontend**:
    - Technologies: HTML, CSS, JavaScript
    - Role: Provides the UI for searching and comparing results
    - Hosting: Netlify
  - **Backend API**:
    - Technologies: Python, Flask
    - Role: Takes frontend parameters, queries the database, and returns a JSON for the table of results
    - Hosting: Render
  - **Backend Web Scraping**:
    - Technologies: Python Scripts
    - Role: Retrieves raw results from official UIL archives and adds to the database
  - **Database**:
    - Technology: SQLite
    - Role: Primary data source, storing all UIL competition results to be queried by API

## To Do
  - Implement a Web Scraper to get past contest results from existing archives with Python (?)
  - Implement filters and sorters for each section with JavaScript or React (?)
  - Add CSS for each page

## Project Link
  - **Live Website**: https://uil-enhanced-archives.netlify.app/
