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
    
    <script src="/static/js/home-sockets.js"></script>


    <main class="container">
        
        <section class="resource-section">
            <h2>Salas Disponíveis</h2>
            <div class="resource-list" data-type="room">
                %if salas:
                
                % for sala in salas:

                <div class="resource-item" data-id="{{sala.id}}">
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
                        <button onclick='fetch("/reservar/sala/{{ sala.id }}", {method:"POST"})' class="btn">Reservar</button>
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
            <div class="resource-list" data-type="equipment">
                
                % if equipment_list:
                
                % for eq in equipment_list:
                <div class="resource-item" data-id="{{eq.id}}">
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
                        <button onclick='fetch("/reservar/equipamento/{{ eq.id }}", {method:"POST"})' class="btn">Reservar</button>
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