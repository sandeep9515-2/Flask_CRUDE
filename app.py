
from flask import Flask,request,jsonify
import csv

# Create the Flask application
app = Flask(__name__)

# a route to provide all  the appointments details
@app.route('/get_appointments',methods=['GET'])
def get_appointments():
   with open('appointments.csv','r',newline='') as file:
       reader=csv.DictReader(file)
       appointments=list(reader)
   return jsonify(appointments)

#  a route to provide appointment details of selected id 
@app.route('/get_selected_appointmentID/<appointment_ID>',methods=['GET'])
def get_id_appointment(appointment_ID):
    with open('appointments.csv','r') as file:
       reader=csv.DictReader(file)
       for i in reader:                                        # i refers a row in csv file.
           if(i['ID']==appointment_ID):
               return jsonify(i)
    return "INVALID ID : please provide a valid id"

# a route to add a new record of appointment details to the existing csv file using post request.

@app.route('/add_record',methods=['POST'])
def add_record():
    new_appointmnet=request.json
    if not new_appointmnet:
        return jsonify({'status':'error','id':200})
    names = ['ID', 'title', 'date', 'time']
    with open('appointments.csv','a',newline='') as file:
        writer = csv.DictWriter(file, fieldnames=names)
        writer.writerow(new_appointmnet)
    return jsonify({'status':'record added  successfully','code':201})

# a route to update a record of appointment details of the existing csv file using post request

@app.route('/update_record/<appointment_id>',methods=['PUT'])
def update_record(appointment_id):
    info=request.json
    updated_record=None
    flag=False
    with open('appointments.csv','r',newline='') as file:
        records=list(csv.DictReader(file))
        for i in records:
            if(i['ID']==appointment_id):
                i.update(info)
                updated_record=i
                flag=True
    if not flag:
        return jsonify({'satus':"NOT FOUND","code":201})
    names = ['ID', 'title', 'date', 'time']
    with open('appointments.csv','w',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=names)
        writer.writeheader()
        writer.writerow(records)
    return jsonify({'status':'succefully_updated','code':200})

    







if __name__ == '__main__':
    app.run(debug=True)