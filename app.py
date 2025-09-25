from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "chave-secreta"

def gerar_pergunta(tipo):
    intervalo = range(1, 11)
    num1 = random.choice(intervalo)
    num2 = random.choice(intervalo)

    if tipo == 'multiplicacao':
        resposta = num1 * num2
        operador = '*'
    elif tipo == 'adicao':
        resposta = num1 + num2
        operador = '+'
    elif tipo == 'subtracao':
        resposta = num1 - num2
        operador = '-'
    else:
        while num2 == 0:
            num2 = random.choice(intervalo)
        resposta = num1 // num2
        operador = '/'

    return num1, num2, resposta, operador

@app.route('/')
def index():
    session.clear()  #  Reseta tudo ao voltar para o início
    return render_template('index.html')

@app.route('/quiz/<tipo>', methods=['GET', 'POST'])
def quiz(tipo):
    if "perguntas" not in session:
        session["perguntas"] = []
        session["acertos"] = 0
        session["atual"] = 0

    # Se já respondeu 5 perguntas, vai para o resultado
    if session["atual"] >= 5:
        return redirect(url_for("resultado"))

    if request.method == "POST":
        resposta_usuario = int(request.form["resposta"])
        correta = session["perguntas"][-1][2]

        if resposta_usuario == correta:
            session["acertos"] += 1
            feedback = "✅ Correto!"
        else:
            feedback = f"❌ Errado! A resposta certa era {correta}"

        #  Depois de responder, gera nova pergunta
        if session["atual"] >= 5:
            return redirect(url_for("resultado"))
        
        num1, num2, resposta, operador = gerar_pergunta(tipo)
        session["perguntas"].append((num1, num2, resposta, operador))
        session["atual"] += 1

        return render_template(
            "quiz.html",
            num1=num1,
            num2=num2,
            operador=operador,
            numero=session["atual"],
            feedback=feedback
        )

    # Primeira pergunta
    num1, num2, resposta, operador = gerar_pergunta(tipo)
    session["perguntas"].append((num1, num2, resposta, operador))
    session["atual"] += 1

    return render_template(
        "quiz.html",
        num1=num1,
        num2=num2,
        operador=operador,
        numero=session["atual"],
        feedback=None
    )

@app.route('/resultado')
def resultado():
    return render_template(
        "resultado.html",
        acertos=session.get("acertos", 0),
        total=session.get("atual", 0)
    )

if __name__ == "__main__":
    app.run(debug=True)
