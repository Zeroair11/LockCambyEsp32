from flask import Flask
from flask import request
from flask import jsonify

from datetime import datetime

import os

# =====================================================
# APP
# =====================================================

app = Flask(__name__)

# =====================================================
# SAVE FOLDER
# =====================================================

SAVE_DIR = "images"

os.makedirs(
    SAVE_DIR,
    exist_ok=True
)

# =====================================================
# HOME
# =====================================================

@app.route("/")

def home():

    return "SERVER RUNNING"

# =====================================================
# UPLOAD
# =====================================================

@app.route(
    "/upload",
    methods=["POST"]
)

def upload():

    try:

        # =============================================
        # GET IMAGE
        # =============================================

        image_data = request.data

        if not image_data:

            return jsonify({

                "status": "error",
                "message": "empty image"

            }), 400

        # =============================================
        # FILE NAME
        # =============================================

        filename = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        ) + ".jpg"

        path = os.path.join(
            SAVE_DIR,
            filename
        )

        # =============================================
        # SAVE FILE
        # =============================================

        with open(path, "wb") as f:

            f.write(image_data)

        print("IMAGE SAVED")

        print(filename)

        print("SIZE:", len(image_data))

        # =============================================
        # RESPONSE
        # =============================================

        return jsonify({

            "status": "success",
            "filename": filename

        })

    except Exception as e:

        print("UPLOAD ERROR")

        print(e)

        return jsonify({

            "status": "error",
            "message": str(e)

        }), 500

# =====================================================
# START
# =====================================================

app.run(

    host="0.0.0.0",

    port=5000,

    debug=False

)