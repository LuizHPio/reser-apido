<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reser-ápido - Login</title>
    <link rel="stylesheet" type="text/css" href="static/css/login.css">
</head>

<body>

    <div class="login-container">
        <h1>Reser-ápido login</h1>
        <form method="POST">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="senha">Senha</label>
                <input type="password" id="senha" name="senha" pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$" required>
            </div>
            <button type="submit" class="btn">Entrar</button>
        </form>
        <a href="/register" class="link-register">Não tem uma conta? Crie uma</a>
    </div>

</body>
</html>