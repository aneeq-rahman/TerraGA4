from flask import Flask, jsonify
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

app = Flask(__name__)

@app.route('/analytics_report', methods=['GET'])
def get_analytics_report():
    property_id = "xxx"  # Replace with your actual GA4 property ID
    try:
        # Initialize the Google Analytics client
        client = BetaAnalyticsDataClient()
         
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
    app.run(debug=True)
