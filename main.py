import os
import json
from flask import Flask, jsonify
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account

app = Flask(__name__)

# Load Google Application Credentials from environment variable
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
credentials_info = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Replace with your actual GA4 property ID, set as an environment variable for security
property_id = os.getenv("GA4_PROPERTY_ID")

@app.route('/analytics_report', methods=['GET'])
def get_analytics_report():
    if not property_id:
        return jsonify({"error": "GA4 Property ID is not set in environment variables"}), 500

    try:
        # Initialize the Google Analytics client with credentials
        client = BetaAnalyticsDataClient(credentials=credentials)

        # Set up the request
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="country")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date="2024-11-01", end_date="2024-11-12")],
        )

        # Get the report data
        response = client.run_report(request)

        # Format the response to return a JSON-friendly structure
        report_data = []
        for row in response.rows:
            row_data = {}
            for i, dimension_value in enumerate(row.dimension_values):
                row_data[response.dimension_headers[i].name] = dimension_value.value
            for i, metric_value in enumerate(row.metric_values):
                row_data[response.metric_headers[i].name] = metric_value.value
            report_data.append(row_data)

        return jsonify(report_data)  # Return the data as JSON

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run in debug mode if needed; for production, this should be set to False
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")
