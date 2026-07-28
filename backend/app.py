from extensions import app

import routes

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)