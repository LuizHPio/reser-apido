<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale-1.0">
    <title>Reser-ápido - Home</title>
    <link rel="stylesheet" href="/static/css/home.css">
</head>
<body>

    %include("header", title="Home", role=role)

    <main class="container">
        
        <section class="resource-section">
            <h2>Salas Disponíveis</h2>
            <div class="resource-list">
                %if salas:
                
                % for sala in salas:

                <div class="resource-item">
                    <div class="resource-info">
                        <h3>{{ sala.name }}</h3>
                        <p>{{ sala.description }}</p>
                        
                        % if sala.available:
                            <span class="status available">Disponível</span>
                        % else:
                            <span class="status in-use">Em Uso</span>
                        % end
                    </div>
                    
                    % if sala.available:
                        <button onclick="window.location.replace('/reservar/sala/{{ sala.id }}')" class="btn">Reservar</button>
                    % else:
                        <button class="btn" disabled>Reservar</button>
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
                
                % if equipment_list:
                
                % for eq in equipment_list:
                <div class="resource-item">
                    <div class="resource-info">
                        <h3>{{ eq.name }}</h3>
                        <p>{{ eq.description }}</p>
                        
                        % if eq.available:
                            <span class="status available">Disponível</span>
                        % else:
                            <span class="status in-use">Em Uso</span>
                        % end
                    </div>
                    
                    % if eq.available:
                        <button onclick="window.location.replace('/reservar/equipamento/{{ eq.id }}')" class="btn">Reservar</button>
                    % else:
                        <button class="btn" disabled>Reservar</button>
                    % end
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