from mcp.server.fastmcp import FastMCP
from src.jobs_api import fetch_linkdin_jobs, fetch_naukri_jobs

mcp = FastMCP("Job Recommender")

@mcp.tool()
async def fetch_linkdin(listofkey):
    return fetch_linkdin_jobs(listofkey)

@mcp.tool()
async def fetch_naukri(listofkey):
    return fetch_naukri_jobs(listofkey)


if __name__ == "__main__":
    mcp.run(transport="stdio")