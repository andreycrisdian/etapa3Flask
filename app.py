from flask import Flask, render_template, request

app = Flask(__name__)

listaCliente = []
listaConta = []
proximaConta = 1

@app.route("/", methods=["GET", "POST"])
def sistema_bancario():
    global proximaConta
    mensagem = ""
    
    if request.method == "POST":
        operacao = request.form.get("operacao", "").upper()

        if operacao == "1" or operacao == "CADASTRAR CLIENTE":
            nome = request.form.get("nome")
            listaCliente.append([nome])
            mensagem = f"Cliente '{nome}' cadastrado com sucesso!"

        elif operacao == "2" or operacao == "CADASTRAR CONTA":
            nome = request.form.get("nome")
            for cliente in listaCliente:
                if cliente[0] == nome:
                    listaConta.append([proximaConta, nome, 0])
                    mensagem = f"Conta criada! Número da conta: {proximaConta}"
                    proximaConta = proximaConta + 1
                    break
            else:
                mensagem = "Cliente não encontrado"

        elif operacao == "4" or operacao == "PROCURAR CONTA" or operacao == "5" or operacao == "CONSULTAR SALDO":
            try:
                numeroConta = int(request.form.get("numeroConta"))
                for conta in listaConta:
                    if conta[0] == numeroConta:
                        mensagem = f"Conta encontrada! Número: {conta[0]} | Cliente: {conta[1]} | Saldo: R$ {conta[2]:.2f}"
                        break
                else:
                    mensagem = "Conta não encontrada"
            except (ValueError, TypeError):
                mensagem = "Número de conta inválido"

        elif operacao == "6" or operacao == "REALIZAR DEPOSITO":
            try:
                numeroConta = int(request.form.get("numeroConta"))
                deposito = float(request.form.get("deposito"))

                for conta in listaConta:
                    if conta[0] == numeroConta:
                        if deposito > 0:
                            conta[2] = conta[2] + deposito
                            mensagem = f"Depósito realizado com sucesso! Novo saldo: R$ {conta[2]:.2f}"
                        else:
                            mensagem = "Valor inválido"
                        break
                else:
                    mensagem = "Conta não encontrada"
            except (ValueError, TypeError):
                mensagem = "Informe um número de conta e valor válidos"

        elif operacao == "7" or operacao == "REALIZAR SAQUE":
            try:
                numeroConta = int(request.form.get("numeroConta"))
                saque = float(request.form.get("saque"))

                for conta in listaConta:
                    if conta[0] == numeroConta:
                        if saque > 0 and saque <= conta[2]:
                            conta[2] = conta[2] - saque
                            mensagem = f"Saque realizado com sucesso! Novo saldo: R$ {conta[2]:.2f}"
                        elif saque > conta[2]:
                            mensagem = "Saldo insuficiente"
                        else:
                            mensagem = "Valor inválido"
                        break
                else:
                    mensagem = "Conta não encontrada"
            except (ValueError, TypeError):
                mensagem = "Informe um número de conta e valor válidos"

    return render_template(
        "index.html", 
        listaCliente=listaCliente, 
        listaConta=listaConta, 
        mensagem=mensagem
    )

if __name__ == "__main__":
    app.run(debug=True)