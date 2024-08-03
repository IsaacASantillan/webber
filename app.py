import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class MassSpectral(db.Model):
    name = db.Column(db.String(64), primary_key = True)
    rt1 = db.Column(db.String(64), index = True)
    rt2 = db.Column(db.String(64))
    suspected_matches = db.Column(db.String(64))
    formula = db.Column(db.String(64))
    mw = db.Column(db.String(64))
    exactmass = db.Column(db.String(64))
    casnumber = db.Column(db.String(64))
    derivatization_agent = db.Column(db.String(64))
    comments = db.Column(db.String(64))
    retention_index = db.Column(db.String(64))
    num_peaks = db.Column(db.String(64))
    x_values = db.Column(db.String(64))
    y_values = db.Column(db.String(64))
    description = db.Column(db.String(64))
    db_number = db.Column(db.String(64))
    synon = db.Column(db.String(64))

    def to_dict(self):
        return {
            "name": self.name,
            "rt1": self.rt1,
            "rt2": self.rt2,
            "suspected_match": self.suspected_matches,
            "formula": self.formula,
            "mw": self.mw,
            "exactmass": self.exactmass,
            "casnumber": self.casnumber,
            "derivatization_agent": self.derivatization_agent,
            #"comment": self.comments,
            "retention_index": self.retention_index,
            "num_peaks": self.num_peaks,
            #"x_values": self.x_values,
            #"y_values": self.y_values,
            "description": self.description,
            "db_number": self.db_number,
            "synon": self.synon
        }

with app.app_context():
    db.create_all()



###########Abstracted away###################
@app.route('/')
def index():
    return render_template('server_table.html')


@app.route('/api/data')
def data():
    query = MassSpectral.query

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            MassSpectral.name.like(f'%{search}%'),
            MassSpectral.rt1.like(f"%{search}%"))
        )
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in ['name']:
                name = 'name'
            col = getattr(MassSpectral, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [ms.to_dict() for ms in query],
        'total': total,
    }


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
