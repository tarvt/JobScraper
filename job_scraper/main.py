# main.py
import json
from JobSearcher import JobinjaSearcher, JobVisionSearcher  

def perform_job_search(searcher, keywords, locations=None, categories=None):
    return searcher.search_jobs(keywords, locations, categories)

def write_results_to_file(file_name, results):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(results)


def write_results_to_json_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def main():

    search_keywords = input("Enter search keywords: ")

    # Initialize the searchers for both platforms
    jobinja_searcher = JobinjaSearcher("https://jobinja.ir/jobs")
    jobvision_searcher = JobVisionSearcher()
    # Perform job searches
    jobinja_results = perform_job_search(jobinja_searcher, search_keywords)
    jobvision_results = perform_job_search(jobvision_searcher, search_keywords)
    # Combine results from both searchers
    all_results = jobinja_results + jobvision_results
    # Create a JSON output file name
    output_file_name = f"job_search_results_{search_keywords.replace(' ', '_')}.json"
    # Write combined results to JSON file
    write_results_to_json_file(output_file_name, all_results)
    print(f"Results have been saved to {output_file_name}")

if __name__ == "__main__":

    main()
