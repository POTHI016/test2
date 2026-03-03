from flask import Flask, jsonify, render_template_string, request
import os

app = Flask(__name__)

data_list = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Scale Dashboard</title>

<script>
function updateTable(){
fetch('/data')
.then(res => res.json())
.then(data => {

let body = document.getElementById("tablebody")
body.innerHTML=""

data.forEach((r)=>{

let row = "<tr>"

row += "<td>"+r.date+"</td>"
row += "<td>"+r.time+"</td>"
row += "<td>"+r.weight+"</td>"
row += "<td>"+r.unit+"</td>"
row += "<td>"+r.lot+"</td>"
row += "<td>"+r.product+"</td>"
row += "<td>"+r.product_code+"</td>"
row += "<td>"+r.notes+"</td>"
row += "<td>"+r.scale_id+"</td>"
row += "<td>"+r.serial+"</td>"
row += "<td>"+r.model+"</td>"
row += "<td>"+r.txn+"</td>"

row += "</tr>"

body.innerHTML += row
})
})
}

setInterval(updateTable,1000)
</script>

<style>
body{font-family:Arial;background:#f5f5f5;text-align:center}
table{border-collapse:collapse;width:95%;margin:auto;background:white}
th,td{border:1px solid #ccc;padding:8px;font-size:14px}
th{background:#444;color:white}
</style>

</head>
<body>

<h2>Scale Data Table (Cloud)</h2>

<table>
<thead>
<tr>
<th>Date</th>
<th>Time</th>
<th>Weight</th>
<th>Unit</th>
<th>Lot number</th>
<th>Product Name</th>
<th>Product Code</th>
<th>Notes</th>
<th>Scale ID</th>
<th>Scale Serial Number</th>
<th>Scale Model Number</th>
<th>Txn Number</th>
</tr>
</thead>
<tbody id="tablebody"></tbody>
</table>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/data")
def data():
    return jsonify(data_list)

# 🔹 API to receive data from local PC
@app.route("/receive", methods=["POST"])
def receive():
    data = request.json
    data_list.insert(0, data)
    if len(data_list) > 100:
        data_list.pop()
    return jsonify({"status": "received"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)