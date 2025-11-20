<link rel="stylesheet" href="/static/css/header.css">
<header class="header">
    <a href="/home" class="logo">Reser-ápido</a>

    <b>{{title}}</b>

    <nav>
        % if title != "Home":
        <a href="/home" >Home</a>
        % else:
        <a class="disabled" href="/home" >Home</a>
        % end

        % if title != "Minhas Reservas":
         <a href="/my-reserves">Minhas Reservas</a>
        % else:
         <a class="disabled" href="/my-reserves">Minhas Reservas</a>
        % end

        <a onclick=logout()>Sair</a>
    </nav>

    <script>
    function logout(){
        const choice = confirm("Tem certeza que deseja prosseguir? Você será deslogado.")
        if (choice){
            window.location.assign("/logout")
        }
    }
    </script>

</header>