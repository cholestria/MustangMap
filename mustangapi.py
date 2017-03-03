from flask_restful import Resource
from calculations import ha_data_for_ha_chart, master_state_dict, nationwide_pop_ar_totals, all_years_state_comparison


class PopByYearAPI(Resource):
    """Populations of All States"""

    def get(self):
        return all_years_state_comparison()


class HerdAreaDataAPI(Resource):
    """Data for each herd area"""

    def get(self, herd_id):
        return ha_data_for_ha_chart(herd_id)


class StateDataAPI(Resource):
    """Data for each state"""
    def get(self, state_id):
        return master_state_dict(state_id)


class TotalDataAPI(Resource):
    """Nationwide Data"""
    def get(self):
        return nationwide_pop_ar_totals()


if __name__ == '__main__':
    # app.run(debug=True)

    app.run(port=5001, host='0.0.0.0')
