# JobScraper

JobScraper automates the process of searching and collecting job postings from multiple online job boards. This project is built to simplify the job hunting experience by providing timely notifications of new job listings that match your criteria.

## Features

- Search for job listings using keywords.
- Combines results from multiple job search platforms.
- Saves the results in a structured JSON format.

## Technologies Used

- Python 3.x
- JSON for data storage
- Custom classes for Job searchers: `JobinjaSearcher` and `JobVisionSearcher`

## Usage:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/job-search-app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd job-search-app
   ```
3. Run the application:
   ```bash
   cd job-search-app
   ```
4. When prompted, enter the search keywords for the job you are looking for.
5. The application generates a JSON file containing the combined job listings from both platforms.
   The filename is formatted as job*search_results*<search_keywords>.json, where <search_keywords> is replaced with the user-provided keywords.
