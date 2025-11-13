<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reser-ápido - Criar Conta</title>
    <link rel="stylesheet" type="text/css" href="static/css/register.css">
</head>

<body>

    <div class="register-container">
        <h1>Criar Conta</h1>
        <form id="register-form">
            <div class="form-grupo">
                <label for="nome">Nome</label>
                <input type="text" id="nome" name="nome" required>
            </div>
            <div class="form-grupo">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-grupo">
                <label for="senha">Senha</label>
                <input type="password" id="senha" name="senha" required>
            </div>
            <p class="hint"> A senha deve possuir no mínimo 8 caracteres, um número e uma letra maiúscula </p>
             <div class="form-grupo">
                <label for="confirmar-senha">Confirmar Senha</label>
                <input type="password" id="confirmar-senha" name="confirmar-senha" required>
            </div>
            <button type="submit" class="btn">Registrar</button>
        </form>
        <a href="/login" class="link-login">Já tem uma conta? Entre</a>
    </div>

    <script src="static/js/register.js"></script>
</body>
</html>