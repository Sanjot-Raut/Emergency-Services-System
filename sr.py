from twilio.rest import Client

account_sid = 'ACf6b4ed44dccad6c9ceb4a8effbcd0fe9'
auth_token = '356755df96baa08bcfa955f070936d5d'


client = Client(account_sid, auth_token)


message = client.messages.create(
    to='+919370321080', 
    from_='+13343779631', 
    body='Hello I am SR.'
)

print(f"SMS sent with message SID: {message.sid}")




# @app.route('/submit_request', methods=['POST'])
# def submit_request():
#     data = request.get_json()
#     user_id = data['user_id']
#     location = data['location']
#     request_type = data['request_type']
#     new_request = Request(user_id=user_id, location=location, request_type=request_type)
#     db.session.add(new_request)
#     db.session.commit()
#     return jsonify({'message': 'Request submitted successfully'})

# @app.route('/list_requests', methods=['GET'])
# def list_requests():
#     pending_requests = Request.query.filter_by(status='Pending').all()
#     requests = [{'id': request.id, 'user_id': request.user_id, 'location': request.location, 'request_type': request.request_type} for request in pending_requests]
    
#     return jsonify({'requests': requests})


# @app.route('/accept_request/<int:request_id>/<int:service_provider_id>', methods=['PUT'])
# def accept_request(request_id, service_provider_id):
#     request = Request.query.get(request_id)
#     if request:
#         request.status = 'Accepted'
#         request.service_provider_id = service_provider_id
#         db.session.commit()
#         return jsonify({'message': 'Request accepted successfully'})
#     else:
#         return jsonify({'message': 'Request not found'}, 404)



# @app.route('/select_service_provider/<int:request_id>/<int:service_provider_id>', methods=['PUT'])
# def select_service_provider(request_id, service_provider_id):
#     request = Request.query.get(request_id)
#     if request:
#         if request.status == 'Accepted' and request.service_provider_id == service_provider_id:
#             return jsonify({'message': 'Service provider selected successfully'})
#         else:
#             return jsonify({'message': 'Invalid request or service provider'}, 400)
#     else:
#         return jsonify({'message': 'Request not found'}, 404)