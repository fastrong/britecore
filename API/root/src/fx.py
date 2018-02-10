from flask import Flask, Response
import psycopg2
from flask_sqlalchemy import SQLAlchemy
import enum
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@davko.net:5432/britecore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class serializer:
    def serializex(self):
        """
        Jsonify the sql alchemy query result.
        """
        convert = dict()
        d = dict()
        for c in self.__class__.__table__.columns:
            v = getattr(self, c.name)
            if c.type in convert.keys() and v is not None:
                try:
                    d[c.name] = convert[c.type](v)
                except:
                    d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
            elif v is None:
                d[c.name] = str()
            else:
                d[c.name] = v
        return d

class FieldType(enum.Enum):
  TEXT = 'text'
  NUMBER = 'number'
  DATE = 'date'
  ENUM = 'enum'

class RiskType(db.Model, serializer):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(256), unique=True)

class RiskField(db.Model, serializer):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(256))
  type=db.Column(db.Enum(FieldType))

  riskFieldEnum = db.relationship("RiskFieldEnum", backref='riskField', lazy=True)

class RiskTypeField(db.Model, serializer):
  riskTypeId = db.Column(db.Integer, db.ForeignKey('risk_type.id'), primary_key=True)
  riskFieldId = db.Column(db.Integer, db.ForeignKey('risk_field.id'), primary_key=True)

  riskType = db.relationship("RiskType", lazy=True)
  riskField = db.relationship("RiskField", lazy=True)

class RiskFieldEnum(db.Model, serializer):
  id = db.Column(db.Integer, primary_key=True)
  riskFieldId = db.Column(db.Integer, db.ForeignKey('risk_field.id'))
  name = db.Column(db.String(256))

def insertSampleData():
  rt1 = RiskType(name = 'Automobile')
  rt2 = RiskType(name = 'House')

  rf1 = RiskField(name = 'Serial number', type = "TEXT")
  rf2 = RiskField(name = 'Production date', type = "DATE")
  rf3 = RiskField(name = 'Top speed ( mph )', type = "NUMBER")
  rf4 = RiskField(name = 'Fuel type', type = "ENUM")

  rf5 = RiskField(name = 'Size ( square feet )', type = "NUMBER")
  rf6 = RiskField(name = 'Build date', type = "DATE")
  rf7 = RiskField(name = 'Address', type = "TEXT")
  rf9 = RiskField(name = 'Construction type', type = "ENUM")

  rf8 = RiskField(name = 'Market prize', type='NUMBER')

  rtf1 = RiskTypeField(riskType = rt1, riskField = rf1)
  rtf2 = RiskTypeField(riskType = rt1, riskField = rf2)
  rtf3 = RiskTypeField(riskType = rt1, riskField = rf3)
  rtf4 = RiskTypeField(riskType = rt1, riskField = rf4)
  rtf5 = RiskTypeField(riskType = rt1, riskField = rf8)

  rtf6 = RiskTypeField(riskType = rt2, riskField = rf5)
  rtf7 = RiskTypeField(riskType = rt2, riskField = rf6)
  rtf8 = RiskTypeField(riskType = rt2, riskField = rf7)
  rtf9 = RiskTypeField(riskType = rt2, riskField = rf8)
  rtf10 = RiskTypeField(riskType = rt2, riskField = rf9)

  rfe1 = RiskFieldEnum(riskField = rf4, name = 'Petrol')
  rfe2 = RiskFieldEnum(riskField = rf4, name = 'Diesel')
  rfe3 = RiskFieldEnum(riskField = rf4, name = 'LPG')

  rfe4 = RiskFieldEnum(riskField = rf9, name = 'Brick and block')
  rfe5 = RiskFieldEnum(riskField = rf9, name = 'Timber frame')
  rfe6 = RiskFieldEnum(riskField = rf9, name = 'Steel frame')
  rfe7 = RiskFieldEnum(riskField = rf9, name = 'Structural insulated panels')
  rfe8 = RiskFieldEnum(riskField = rf9, name = 'Insulated concrete formwork')

  db.session.add_all([rt1, rt2, rf1, rf2, rf3, rf4, rf5, rf6, rf7, rf8, rf9, rtf1, rtf2, rtf3, rtf4, rtf5, rtf6, rtf7, rtf8, rtf9, rtf10, rfe1, rfe2, rfe3, rfe4, rfe5, rfe6, rfe7, rfe7, rfe8])
  db.session.commit()

db.drop_all()
db.create_all()
insertSampleData()

@app.route("/")
def hi():
  return "hello"

@app.route("/riskType/<id>", methods=["GET"])
def get_risk(id):
  risk = db.session.query(RiskType).filter_by(id=id).first()
  farr = []
  rtfs = db.session.query(RiskTypeField).filter_by(riskType = risk)
  for rtf in rtfs:
    earr = []
    fenum = db.session.query(RiskFieldEnum).filter_by(riskField = rtf.riskField)
    for en in fenum:
      earr.append(en.serializex())
    farr.append({
      "id" : rtf.riskField.id,
      "name" : rtf.riskField.name,
      "type" : rtf.riskField.type.value,
      "enum" : earr
    })
  
  if risk is not None:
    return Response(json.dumps({ "risk" : risk.serializex(), "fields" : farr }), status=200, mimetype="application/json")
  else:
    return Response(json.dumps({"error" : "Risk with ID does not exist"}), status=404, mimetype="application/json")

@app.route("/riskTypes", methods=["GET"])
def get_risks():
  rarr = []
  risks = db.session.query(RiskType).all()
  for risk in risks:
    rarr.append(risk.serializex())
  ret = {
    "risks" : rarr
  }
  return Response(json.dumps(ret), status=200, mimetype="application/json")

if __name__ == '__main__':
  app.run()
