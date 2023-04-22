import json

import quart
import quart_cors
from quart import request
from quart.wrappers.response import Response
import base64
from quart import jsonify

app = quart_cors.cors(quart.Quart(__name__),
                      allow_origin="https://chat.openai.com")

# Keep track of todo's. Does not persist if Python session is restarted.
_TODOS = {
  'neo': ['https://plugins-quickstart.datboineo.repl.co/logo.png', 'write a poem about turtles', 'lose 10 pounds', 'calculate 3+5 in python']
}

# "Figure out this coding problem in python: \n\n Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order. \n\n use this function for the two sum implementation: int* twoSum(int* nums, int numsSize, int target, int* returnSize){} \n\n run the code and make sure it works for edge cases"

@app.get("/")
async def base():
  return quart.Response(response='OK', status=200)


@app.route("/todos/<string:username>")
async def get_todos(username):
  todos = _TODOS.get('neo', [])
  print("todos", todos)
  return jsonify({'todos': todos}), 200

@app.route("/eval", methods=["GET"])
async def eval_endpoint():
    string = request.args.get("string")
    if string is None:
        return jsonify({"error": "Missing 'string' parameter"}), 400
    try:
        result = eval(string)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.get("/logo.png")
async def plugin_logo():
  filename = 'logo.png'
  return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
  host = request.headers['Host']
  with open("./.well-known/ai-plugin.json") as f:
    text = f.read()
    return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
  host = request.headers['Host']
  with open("openapi.yaml") as f:
    text = f.read()
    return quart.Response(text, mimetype="text/yaml")


def main():
  app.run(debug=True, host="0.0.0.0", port=5003)


if __name__ == "__main__":
  main()
