from flask import Flask,render_template
import views



def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/parameters", view_func=views.parameters_page, methods=["GET", "POST"])
    app.add_url_rule("/parameters/<int:parameter_id>", view_func=views.parameter_page)
    app.add_url_rule("/Measurement", view_func=views.Measurement_page, methods=["GET", "POST"])
    app.add_url_rule("/Calibration_fs", view_func=views.Calibration_fs_page, methods=["GET", "POST"])
    app.add_url_rule("/Calibration_cable", view_func=views.Calibration_cable_page, methods=["GET", "POST"])
    app.add_url_rule("/Process_Measurement", view_func=views.Process_Measurement_page, methods=["GET", "POST"])
    app.add_url_rule("/Process_CalibrationCable", view_func=views.Process_CalibrationCable_page, methods=["GET", "POST"])
    app.add_url_rule("/Process_CalibrationFreeSpace", view_func=views.Process_CalibrationFreeSpace_page, methods=["GET", "POST"])
    return app




if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, use_reloader=False)
    #app.run(host="0.0.0.0")
