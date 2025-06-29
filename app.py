from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rutinas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta_para_sesiones'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Rutina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(50), nullable=False)
    ejercicio = db.Column(db.String(100), nullable=False)
    series = db.Column(db.Integer, nullable=False)
    repeticiones = db.Column(db.Integer, nullable=False)
    grupo_muscular = db.Column(db.String(50), nullable=False)
    dificultad = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    rutinas = Rutina.query.filter_by(usuario_id=current_user.id).all()
    return render_template('index.html', rutinas=rutinas)

@app.route('/agregar', methods=['POST'])
@login_required
def agregar():
    dia = request.form['dia']
    ejercicio = request.form['ejercicio']
    series = request.form['series']
    repeticiones = request.form['repeticiones']
    grupo_muscular = request.form['grupo_muscular']
    dificultad = request.form['dificultad']
    nueva_rutina = Rutina(
        dia=dia,
        ejercicio=ejercicio,
        series=series,
        repeticiones=repeticiones,
        grupo_muscular=grupo_muscular,
        dificultad=dificultad,
        usuario_id=current_user.id
    )
    db.session.add(nueva_rutina)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    rutina = Rutina.query.get_or_404(id)
    if rutina.usuario_id != current_user.id:
        return redirect(url_for('index'))
    db.session.delete(rutina)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['POST'])
@login_required
def editar(id):
    rutina = Rutina.query.get_or_404(id)
    if rutina.usuario_id != current_user.id:
        return redirect(url_for('index'))
    rutina.dia = request.form['dia']
    rutina.ejercicio = request.form['ejercicio']
    rutina.series = request.form['series']
    rutina.repeticiones = request.form['repeticiones']
    rutina.grupo_muscular = request.form['grupo_muscular']
    rutina.dificultad = request.form['dificultad']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nuevo_usuario = Usuario(
            username=request.form['username'],
            password=request.form['password']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registrar.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
