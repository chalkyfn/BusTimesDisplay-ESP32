# from flask import Flask, request, jsonify
# import subprocess

# app = Flask(__name__)

# @app.route('/run-script', methods=['POST'])
# def run_script():
#     try:
#         # Execute the Python script and capture its output
#         result = subprocess.run(['python', 'real.py'], capture_output=True, text=True)
#         output = result.stdout
#         return jsonify({"output": output})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Execute the Python script and capture its output and errors
        result = subprocess.run(
            ['python', 'bus-times-api.py'], 
            capture_output=True, 
            text=True
        )

        # Check if the script executed successfully
        if result.returncode == 0:
            return jsonify({"output": result.stdout.strip()})
        else:
            return jsonify({
                "error": "Script execution failed",
                "details": result.stderr.strip()
            }), 400  # 400 Bad Request for script errors

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # 500 Internal Server Error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)