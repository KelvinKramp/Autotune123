from flask import request, jsonify
from autotune import Autotune
from datetime import datetime as dt
from datetime import timedelta



autotune = Autotune()

def autotune_api():
    if request.method == "POST":
        message = request.get_json()
        possible_input = ["start_date", "end_date", "NS_URL", "token", "filter", "insulin_type", "uam"]
        end_date = str(dt.now().date())
        start_date = str(dt.now().date() - timedelta(3))
        default_input = [start_date, end_date, None, None, None, "rapid-acting",None]
        for i in possible_input:
            if i not in message.items():
                message[i] = default_input[i]
        if message[2] == None:
            return jsonify({"something":"somethings"})
        start_date = message["start_date"]
        end_date = message["end_date"]
        NS_HOST = message["NS_URL"]
        token = message["token"]
        dropdown_value = message["filter"]
        insulin_type = message["insulin_type"]
        uam = message["uam"]
        # run autotune
        print("getting profile")
        autotune.get(NS_HOST, token, insulin_type)
        _, _, profile = autotune.get(NS_HOST, token)
        print(profile)
        print("running autotune")
        print(start_date, end_date, NS_HOST, uam)
        autotune.run(NS_HOST, start_date, end_date, uam)
        print("creating recommendations")
        df_recommendations, graph, y1_sum_graph, y2_sum_graph = data_preperation(dropdown_value)
        json_data = df_recommendations.to_dict('records')
        new_profile = autotune.create_adjusted_profile(json_data, profile)
        print("attempting to upload")
        print(new_profile)
        # result = autotune.upload(NS_HOST, new_profile, token)

        return jsonify({"Autotune ran succesfully, new profile activated on phone via": NS_HOST,
                        "Filter": dropdown_value,
                        "Start_date": start_date,
                        "End_date": end_date}), 200
    return jsonify({"you ": request.get_json()}), 200