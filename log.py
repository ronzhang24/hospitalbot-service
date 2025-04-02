from google.cloud import bigquery

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Initialize BigQuery client
client = bigquery.Client()

# Function to check if user exists and retrieve names by MRN
def save_chat_history(session_id, request, query, response):
    try:
        logger.info(f"Request: {request}")
        logger.info(f"Response: {response}")
        insert_query = """
            INSERT INTO `hospitalbot-bwpg.hospitalbot.transaction` (session_id, request, query, response, timestamp)
            VALUES (@session_id, @request, @query, @response, CURRENT_TIMESTAMP())
            """
            
        # Set up the job configuration with query parameters
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("session_id", "STRING", session_id),
                bigquery.ScalarQueryParameter("request", "STRING", request),
                bigquery.ScalarQueryParameter("query", "STRING", query),
                bigquery.ScalarQueryParameter("response", "STRING", response)
            ]
        )

        # Run the query with parameters
        query_job = client.query(insert_query, job_config=job_config)

        # Wait for the query to complete
        query_job.result()
        
        logger.info("Log has been successfully inserted.")
        return True
    except Exception as e:
        logger.info(e)
        return False
    
def get_session_chat_history(session_id):
    client = bigquery.Client()
    
    query = f"""
        SELECT 
            session_id, 
            STRING_AGG(query, ' ' ORDER BY timestamp ASC) AS chat_history
        FROM `hospitalbot-bwpg.hospitalbot.transaction`
        WHERE session_id = '{session_id}'
        GROUP BY session_id
    """
    
    logger.info(f"Running Query:{query}")
    query_job = client.query(query)
    results = query_job.result()

    # Assuming `results` contains the query result from BigQuery
    logger.info(f"Result:{results}")

    # Since you're expecting only one row, we can directly access it.
    # Extract the chat_history from the first (and only) row in the result.
    if results.total_rows > 0:
        # Get the first row
        row = list(results)[0]
        chat_history = row.chat_history
        logger.info(f"Chat History: {chat_history}")
    else:
        chat_history = ""
        logger.warning("No results found for the given session_id.")

    return chat_history + ", "
