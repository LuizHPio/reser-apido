<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale-1.0">
    <title>Reser-ápido - Home</title>
    <link rel="stylesheet" href="/static/css/home.css">
</head>
<body>

    %include("header", title="Minhas Reservas", role=role)
    <script src="/static/js/reserves-sockets.js"></script>

    <main class="container">
        
        <section class="resource-section">
            <h2>Salas Reservadas</h2>
            <div class="resource-list" data-type="room">
                %if reserved_rooms:
                
                % for sala in reserved_rooms:

                <div class="resource-item" data-id="{{sala.id}}">
                    <div class="resource-info">
                        <h3>{{ sala.name }}</h3>
                        <p>{{ sala.description }}</p>
                        
                        % if sala.available:
                            <span class="status available">Disponível</span>
                        % else:
                            <span class="status reserved">Reservada</span>
                        % end
                    </div>
                    
                    <button onclick=free_room({{sala.id}}) class="btn">Liberar sala</button>
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
            <h2>Equipamentos Reseravados</h2>
            <div class="resource-list" data-type="equipment">
                %if reserved_equipment:
                
                % for eq in reserved_equipment:

                <div class="resource-item" data-id="{{eq.id}}">
                    <div class="resource-info">
                        <h3>{{ eq.name }}</h3>
                        <p>{{ eq.description }}</p>
                        
                        % if eq.available:
                            <span class="status available">Disponível</span>
                        % else:
                            <span class="status reserved">Reservado</span>
                        % end
                    </div>
                    
                    <button onclick=free_equipment({{eq.id}}) class="btn">Liberar equipamento</button>
                </div>
                % end

                % else:
                
                  <div class="resource-info"> 
                    Nenhuma sala disponível
                  </div>

                % end

            </div>
        </section>

    </main>

    <script>
    function free_room(id){
        choice = confirm("Tem certeza que deseja liberar esse quarto? Sua reserva será desfeita.")

        if (choice) {
            fetch(`/liberar/sala/${id}`,{method:"POST"})
        }
    }

    function free_equipment(id){
        choice = confirm("Tem certeza que deseja liberar esse equipamento? Sua reserva será desfeita.")

        if (choice) {
            fetch(`/liberar/equipamento/${id}`, {method:"POST"})
        }
    }

    </script>

</body>
</html>