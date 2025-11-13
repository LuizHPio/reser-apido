<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale-1.0">
    <title>Reser-ápido - Home</title>
    <link rel="stylesheet" href="/static/css/home.css">
</head>
<body>

    <header class="header">
        <a href="/home" class="logo">Reser-ápido</a>
        <nav>
            <a href="/my-reserves">Minhas Reservas</a>
            <a href="/logout">Sair</a>
        </nav>
    </header>

    <main class="container">
        
        <section class="resource-section">
            <h2>Salas Disponíveis</h2>
            <div class="resource-list">
                %if salas:
                
                % for sala in salas:

                <div class="resource-item">
                    <div class="resource-info">
                        <h3>{{ sala['nome'] }}</h3>
                        <p>{{ sala['descricao'] }}</p>
                        
                        % if sala['available']:
                            <span class="status available">Disponível</span>
                        % else:
                            <span class="status in-use">Em Uso</span>
                        % end
                    </div>
                    
                    % if sala['available']:
                        <a href="/reservar/sala/{{ sala['id'] }}" class="btn">Reservar</a>
                    % else:
                        <a href="#" class="btn" disabled>Reservar</a>
                    % end
                </div>
                % end

                % else:
                
                  <div class="resource-info"> 
                    Nenhuma sala disponível
                  </div>

                % end

            </div>
        </section>

        <section class="resource-section">
            <h2>Equipamentos Disponíveis</h2>
            <div class="resource-list">
                
                % if equipamentos:
                
                % for eq in equipamentos:
                <div class="resource-item">
                    <div class="resource-info">
                        <h3>{{ eq['nome'] }}</h3>
                        <p>{{ eq['descricao'] }}</p>
                        
                        <span class="status {{ 'available' if eq['available'] else 'in-use' }}">
                            {{ eq['status'] }}
                        </span>
                    </div>
                    
                    <a href="/reservar/equipamento/{{ eq['id'] }}" 
                       class="btn" 
                       {{ 'disabled' if not eq['available'] else '' }}>
                       Reservar
                    </a>
                </div>
                % end

                % else:

                  <div class="resource-section">  
                    Nenhum equipamento disponível
                  </div>

                % end

            </div>
        </section>

    </main>

</body>
</html>