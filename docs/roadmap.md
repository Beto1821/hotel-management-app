1. 🧑 Módulo de Clientes
Este é o primeiro passo. A recepção precisa cadastrar o cliente antes de associá-lo a uma reserva.

Estrutura de Endpoints (CRUD)
POST /api/v1/clientes


# 🗺️ Roadmap de Funcionalidades

GET /api/v1/clientes/{cliente_id}


PUT /api/v1/clientes/{cliente_id}

Ação: Atualizar os dados de um cliente.
DELETE /api/v1/clientes/{cliente_id}

Ação: Excluir um cliente.

🤖 Prompt para o Copilot (Módulo Clientes)

Crie uma API RESTful em Python usando FastAPI para o gerenciamento de Clientes de um hotel.

1.  **Crie um APIRouter** chamado `router_clientes` com o prefixo `/api/v1/clientes`.

2.  **Defina os Modelos Pydantic (Schemas):**
    * `ClienteBase`: `nome_completo` (str), `email` (EmailStr), `telefone` (str), `documento` (str, ex: CPF ou Passaporte).
    * `ClienteRead` (herda de `ClienteBase` e adiciona `id`: int).

3.  **Implemente os 5 Endpoints CRUD:**
    * **`POST /`**: Cria um novo cliente (recebe `ClienteCreate`, retorna `ClienteRead`).
    * **`GET /`**: Lista todos os clientes (retorna `List[ClienteRead]`). Adicione um query param opcional `nome` para filtrar.
    * **`PUT /{cliente_id}`**: Atualiza um cliente (recebe `ClienteCreate`, retorna `ClienteRead`).
    * **`DELETE /{cliente_id}`**: Deleta um cliente.

Simule a lógica principal dentro das funções, incluindo os imports necessários (FastAPI, APIRouter, Pydantic, List, EmailStr).

2. 🛏️ Módulo de Quartos
Este módulo gerencia o inventário (os quartos) e, o mais importante, fornece os dados para a visualização de ocupação (o calendário).

Estrutura de Endpoints
POST /api/v1/quartos
Ação: Criar um novo quarto (Ex: Quarto 101, Tipo Standard, R$ 250/dia).

GET /api/v1/quartos


PUT /api/v1/quartos/{quarto_id}

Ação: Atualizar dados do quarto, principalmente o valor da diária (como você pediu).
GET /api/v1/quartos/{quarto_id}

Ação: Ver detalhes de um quarto (tipo, status, diária).

GET /api/v1/quartos/calendario (Endpoint Especial)


Query Params: ?data_inicio=YYYY-MM-DD&data_fim=YYYY-MM-DD

Justificativa: Este é o endpoint que vai alimentar o "render de tipo calendário" que você mencionou.
🤖 Prompt para o Copilot (Módulo Quartos)

Crie uma API RESTful em Python usando FastAPI para o gerenciamento de Quartos de um hotel.

1.  **Crie um APIRouter** chamado `router_quartos` com o prefixo `/api/v1/quartos`.

2.  **Defina os Enums:**
    * `StatusQuarto` (Enum): "livre", "ocupado", "limpeza", "manutencao".
    * `TipoQuarto` (Enum): "standard", "deluxe", "suite".

3.  **Defina os Modelos Pydantic (Schemas):**
    * `QuartoBase`: `numero` (str, ex: "101"), `tipo` (TipoQuarto), `valor_diaria` (float).
    * `QuartoCreate` (herda de `QuartoBase`).
    * `QuartoRead` (herda de `QuartoBase`, adiciona `id`: int e `status`: StatusQuarto).
    * `QuartoUpdateDiaria`: (só `valor_diaria`: float)

4.  **Implemente os Endpoints de Gerenciamento:**
    * **`POST /`**: Cria um novo quarto (recebe `QuartoCreate`).
    * **`GET /`**: Lista todos os quartos (retorna `List[QuartoRead]`).
    * **`GET /{quarto_id}`**: Retorna um quarto específico.
    * **`PUT /{quarto_id}/diaria`**: Atualiza o valor da diária de um quarto (recebe `QuartoUpdateDiaria`).

5.  **Implemente o Endpoint de Visualização:**
    * **`GET /calendario`**:
        * Deve aceitar query params `data_inicio` (date) e `data_fim` (date).
        * A função deve simular a busca por reservas nesse período e retornar uma estrutura (ex: um dicionário ou lista) que mostre a ocupação (status e ID da reserva) para cada quarto em cada dia do intervalo.
        * Este endpoint é apenas para visualização.

Simule a lógica, incluindo imports (FastAPI, APIRouter, Pydantic, List, Enum, date).

3. 🗓️ Módulo de Agendamentos (Reservas)
Este módulo é o "coração" que conecta um Cliente a um Quarto por um período, gerando os KPIs de "Reservas Ativas" e "Receita".

Estrutura de Endpoints
POST /api/v1/reservas

Ação: Criar uma nova reserva (associando cliente_id e quarto_id).

GET /api/v1/reservas

Ação: Listar reservas (Para "Reservas Ativas" e "Receita do Mês").

Filtros: ?status=ativa, ?mes=...

GET /api/v1/reservas/{reserva_id}

Ação: Ver detalhes de uma reserva.

POST /api/v1/reservas/{reserva_id}/check-in

Ação: Realiza check-in (muda status da reserva para "ativa" e status do quarto para "ocupado").

POST /api/v1/reservas/{reserva_id}/check-out

Ação: Realiza check-out (muda status da reserva para "concluida" e status do quarto para "limpeza").

DELETE /api/v1/reservas/{reserva_id}

Ação: Cancelar uma reserva.

🤖 Prompt para o Copilot (Módulo Reservas)

Crie uma API RESTful em Python usando FastAPI para o gerenciamento de Reservas (Agendamentos) de um hotel.

1.  **Crie um APIRouter** chamado `router_reservas` com o prefixo `/api/v1/reservas`.

2.  **Defina o Enum:**
    * `StatusReserva` (Enum): "pendente", "ativa", "concluida", "cancelada".

3.  **Defina os Modelos Pydantic (Schemas):**
    * `ReservaBase`: `cliente_id` (int), `quarto_id` (int), `data_check_in` (date), `data_check_out` (date).
    * `ReservaCreate` (herda de `ReservaBase`).
    * `ReservaRead` (herda de `ReservaBase`, adiciona `id`: int e `status`: StatusReserva).

4.  **Implemente os Endpoints CRUD:**
    * **`POST /`**: Cria uma nova reserva (status inicial "pendente") (recebe `ReservaCreate`).
    * **`GET /`**: Lista reservas (retorna `List[ReservaRead]`). Deve aceitar um query param `status` (StatusReserva) opcional.
    * **`GET /{reserva_id}`**: Retorna uma reserva específica.
    * **`DELETE /{reserva_id}`**: Cancela uma reserva (muda status para "cancelada" ou deleta).

5.  **Implemente os Endpoints de Ação (Check-in/Check-out):**
    * **`POST /{reserva_id}/check-in`**: Simule a lógica de mudar o status da reserva para "ativa".
    * **`POST /{reserva_id}/check-out`**: Simule a lógica de mudar o status da reserva para "concluida".

Inclua os imports (FastAPI, APIRouter, Pydantic, List, Enum, date) e simule a lógica.

