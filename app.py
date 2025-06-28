from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rutinas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Rutina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(50), nullable=False)
    ejercicio = db.Column(db.String(100), nullable=False)
    series = db.Column(db.Integer, nullable=False)
    repeticiones = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    rutinas = Rutina.query.all()
    return render_template('index.html', rutinas=rutinas)

@app.route('/agregar', methods=['POST'])
def agregar():
    dia = request.form['dia']
    ejercicio = request.form['ejercicio']
    series = request.form['series']
    repeticiones = request.form['repeticiones']
    nueva_rutina = Rutina(dia=dia, ejercicio=ejercicio, series=series, repeticiones=repeticiones)
    db.session.add(nueva_rutina)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    rutina = Rutina.query.get_or_404(id)
    db.session.delete(rutina)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
