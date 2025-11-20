<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reser-ápido - Painel Admin</title>
    <link rel="stylesheet" href="/static/css/home.css"> 
    <link rel="stylesheet" href="/static/css/admin.css">
</head>
<body>

    %include("header", title="Painel Admin")

    <div class="content">
        <h2>Criação de Novos Recursos</h2>

        <div class="row">
            
            <div class="column">
                <h3>Criar Nova Sala</h3>
                <form action="/admin/create/room" method="POST">
                    <label for="room_name">Nome da Sala</label>
                    <input type="text" id="room_name" name="name" required>
                    
                    <label for="room_description">Descrição</label>
                    <textarea id="room_description" name="description" rows="3"></textarea>

                    <div> <input type="checkbox" id="room_available" name="available"> Habilitar Reservas </div>
                    
                    <button type="submit">Adicionar Sala</button>
                </form>
            </div>

            <div class="column">
                <h3>Criar Novo Equipamento</h3>
                <form action="/admin/create/equipment" method="POST">
                    <label for="equip_name">Nome do Equipamento</label>
                    <input type="text" id="equip_name" name="name" required>
                    
                    <label for="equip_description">Descrição</label>
                    <textarea id="equip_description" name="description" rows="3"></textarea>

                    <div> <input type="checkbox" id="equip_available" name="available"> Habilitar Reservas </div>
                    
                    <button type="submit">Adicionar Equipamento</button>
                </form>
            </div>
        </div>

        <h2>Deletar Recursos Existentes</h2>

        <div class="row">
            
            <div class="column">
                <h3>Salas Existentes</h3>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Ação</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for room in rooms:
                        <tr>
                            <td>{{ room.id }}</td>
                            <td>{{ room.name }}</td>
                            <td>
                                <form action="/admin/delete/room/{{ room.id }}" method="POST">
                                    <button type="submit" class="btn-deletar">Deletar</button>
                                </form>
                            </td>
                        </tr>
                        % end
                        
                        % if not rooms:
                        <tr>
                            <td colspan="3" style="text-align: center;">Nenhuma sala cadastrada.</td>
                        </tr>
                        % end
                    </tbody>
                </table>
            </div>

            <div class="column">
                <h3>Equipamentos Existentes</h3>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Ação</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for equipment in equipments:
                        <tr>
                            <td>{{ equipment.id }}</td>
                            <td>{{ equipment.name }}</td>
                            <td>
                                <form action="/admin/delete/equipment/{{ equipment.id }}" method="POST">
                                    <button type="submit" class="btn-deletar">Deletar</button>
                                </form>
                            </td>
                        </tr>
                        % end
                        
                        % if not equipments:
                        <tr>
                            <td colspan="3" style="text-align: center;">Nenhum equipamento cadastrado.</td>
                        </tr>
                        % end
                    </tbody>
                </table>
            </div>
        </div>

    </div>

</body>
</html>