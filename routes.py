import os
import flask
import datetime
import io
from PIL import Image
from flask import render_template, send_file, request

from database import DataBase


def add_routes(app: flask.Flask, db: DataBase):
    @app.route('/', methods=['GET'])
    def get_main_route():
        context = {
            'title': 'BLACKPINK | Cafe'
        }
        return render_template(
            'main.html',
            **context
        )

    @app.route('/booking/', methods=['GET'])
    def get_booking_route():
        context = {
            'title': 'BLACKPINK | Cafe | Booking',
            'date_placeholder': datetime.datetime.today().strftime("%d.%m.%Y")
        }
        return render_template(
            'booking.html',
            **context
        )

    @app.route('/booking/', methods=['POST'])
    def post_booking_route():
        try:
            table = int(request.args['table'][-1])
            if db.check_can_book(request.args['date'], request.args['time'], table):
                uuid = db.add_record(
                    request.args['name'], request.args['phone'],
                    request.args['date'], request.args['time'],
                    table, request.args['comment']
                )
                return {
                    'status': 'ok',
                    'uuid': uuid
                }
            return {
                'status': 'booked'
            }
        except:
            return {
                'status': 'error'
            }

    @app.route('/booking/<string:uuid>', methods=['GET'])
    def get_booking_qr_code_route(uuid: str):
        context = {
            'title': 'BLACKPINK | Cafe | Booking',
            'uuid': uuid
        }
        return render_template(
            'qr_code.html',
            **context
        )

    @app.route('/qr-code/<string:uuid>', methods=['GET'])
    def get_qr_code_route(uuid: str):
        image_data = db.get_qr_code(uuid)
        image = Image.open(io.BytesIO(image_data))
        img_io = io.BytesIO()
        image.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
