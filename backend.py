from flask import Flask, jsonify, request
import pyautogui
import time

app = Flask(__name__)

@app.route('/action/<string:left_or_right>', methods=['GET'])
def action(left_or_right):
    if left_or_right == "left":
        # return left arrow key
        time.sleep(1)
        pyautogui.press('left', presses = 1)

        return jsonify({'message' : 'left'})
    elif left_or_right == "right":
        # return right arrow key
        time.sleep(1)
        pyautogui.press('right', presses = 1)
        return jsonify({'message' : 'right'})

    else:
        return jsonify({'message' : 'ERROR!!!!'})
    
if __name__ == "__main__":
    app.run(debug=True)