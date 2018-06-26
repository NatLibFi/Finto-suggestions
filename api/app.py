import connexion


app = connexion.FlaskApp(__name__, specification_dir='api/specification/')
app.add_api('suggestion.yaml', base_path="/api/v1")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
