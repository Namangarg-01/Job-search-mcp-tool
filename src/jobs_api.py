from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_KEY"))

#Function to get info about the open jobs from the Apify API Key 

#Fetch Linkdin Jobs based on search query and the location
def fetch_linkdin_jobs(search_query, location = "india", row = 60): # rows is the number of jobs you want to see 
    run_input = {
        "title" : search_query,
        "location" : location,
        "rows":row,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        }
    }
    # Change the ID inside the .actor() method
    run = apify_client.actor("worldunboxer/rapid-linkedin-scraper").call(run_input=run_input)
    # run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items()) #Returning list of Jobs
    return jobs

#Fetch Nauki Jobs 
def fetch_naukri_jobs(search_query, location = "india", row = 60):
    run_input = {
        "keyword":search_query,
        "maxJobs": row,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
    }
    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs