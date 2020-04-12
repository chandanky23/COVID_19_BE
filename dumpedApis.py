
# @app.route('/country/reports')
# def index():
#   requestedDate = request.args.get('date')
#   response = requests.request("GET", listOfCountriesUrl, headers=headers_statistics)
#   jsonData = json.loads(response.text)
#   for key in jsonData:
#     returnData = getReportsPerProvince(jsonData.get(key), requestedDate)
#   return jsonify(jsonData)

# def getReportsPerProvince(countryData, requestedDate):
#   for key in countryData:
#     country_iso = key.get('iso')
#     country_name = key.get('name')
#     dynamic_report_url = reportUrl + '&iso=' + country_iso + '&region_name=' + country_name + '&date=' + requestedDate
#     province_Wise_Report = requests.request("GET", dynamic_report_url, headers=headers_statistics)
#     print(province_Wise_Report)
#   return ""

# @app.route('/total/reports')
# def total():
#   requested_date = request.args.get('date')
#   queryString = {"date": requested_date}
#   print(queryString)
#   response = requests.request("GET", total_reports_url, headers=headers_statistics, params=queryString)
#   json_data = json.loads(response.text)
#   return jsonify(json_data)

# @app.route('/country/current')
# def country_total():
#   requested_country = request.args.get('country')
#   requested_date = request.args.get('date')
#   queryString = {"date": requested_date, "country": requested_country}

#   response = requests.request("GET", country_current_stats, headers=headers_history, params=queryString)
#   json_data = json.loads(response.text)
#   return jsonify(json_data)