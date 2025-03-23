from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def root():
    return send_from_directory(".", "dashboard.html")

@app.route("/plots/<version>/<filename>")
def plots(version, filename):
    return send_from_directory(f"plots/{version}", filename)

@app.route("/models/<version>/<filename>")
def models(version, filename):
    return send_from_directory(f"models/{version}", filename)

@app.route("/plots/<filename>")
def root_plots(filename):
    return send_from_directory("plots", filename)

if __name__ == "__main__":
    print("🌐 Dashboard running at: http://localhost:5000")
    app.run(debug=True)
