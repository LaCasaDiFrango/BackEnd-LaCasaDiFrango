# 🍗 La Casa Di Frango – Backend API

Backend desenvolvido em Django + Django REST Framework para gerenciamento de pedidos, produtos, pagamentos e usuários do sistema **La Casa Di Frango**.

> Projeto acadêmico com estrutura de produção, autenticação com Passage ID, suporte a múltiplas formas de pagamento e filtros dinâmicos de produtos.

---

## 🚀 Funcionalidades Implementadas

* 🔐 Autenticação e cadastro com [Passage ID](https://passage.id/)
* 📟 CRUD de usuários, endereços e cartões
* 📦 Catálogo de produtos com categorias, busca e filtros
* 🛒 Carrinho de compras (pedidos em aberto)
* ✅ Finalização de pedidos com validação de estoque
* 💰 Pagamento vinculado ao pedido
* 📈 Relatório de vendas mensais
* 📊 Produtos mais vendidos

---

## 🛠️ Tecnologias Utilizadas

* Django
* Django REST Framework
* PostgreSQL (produção) / SQLite (dev)
* Passage ID (autenticação)
* Swagger / drf-spectacular (documentação da API)
* Cloudinary (armazenamento de imagens)
* Django-filter, Django-extensions, Corsheaders, Whitenoise
* Render (deploy)
* PDM (gerenciador de pacotes)

---

## 📁 Estrutura de Pastas

```
app/
├── settings.py
└── urls.py
core/
├── models/
│   ├── pedido/
│   ├── produto/
│   ├── usuario/
│   └── pagamento/
├── serializers/
│   ├── pedido/
│   ├── produto/
│   ├── usuario/
│   └── pagamento/
├── views/
│   ├── pedido/
│   ├── produto/
│   ├── usuario/
│   └── pagamento/ 
├── admin.py
└── authentication.py
...
```

---

## 📦 Endpoints Principais

Acesse a documentação completa em: [`/api/schema/swagger-ui`](http://localhost:19003/api/schema/swagger-ui/)

Exemplos:

### 🔐 Autenticação

* `GET /api/users/me/` → Retorna o usuário autenticado

### 📦 Produtos

* `GET /api/produtos/` → Lista com filtros, busca e ordenação
* `PATCH /api/produtos/{id}/alterar_preco/` → Altera o preço
* `POST /api/produtos/{id}/ajustar_estoque/` → Ajusta estoque
* `GET /api/produtos/mais_vendidos/` → Lista produtos mais vendidos

### 🛒 Pedidos

* `POST /api/pedidos/` → Criação de pedido
* `POST /api/pedidos/{id}/finalizar/` → Finaliza pedido (valida estoque)
* `GET /api/pedidos/relatorio_vendas_mes/` → Relatório de vendas

### 📟 Pagamentos

* `POST /api/pagamentos/` → Associa método de pagamento ao pedido

### 👤 Usuário

* `GET /api/users/` → Lista usuários (admin)
* `GET /api/users/me/` → Dados do usuário logado

---

## ⚙️ Como Rodar o Projeto Localmente

1. Instale [Python 3.11+](https://www.python.org/) e [PDM](https://pdm.fming.dev/):

```
pip install pdm
```

2. Clone o repositório e instale dependências:

```bash
pdm install
```

3. Copie o `.env.exemplo` para `.env` e configure:

```bash
cp .env.exemplo .env
```

4. Execute as migrações e inicie o servidor:

```bash
pdm run migrate
pdm run dev
```

5. Acesse:

* API: [http://localhost:19003/api/](http://localhost:19003/api/)
* Swagger: [http://localhost:19003/api/schema/swagger-ui/](http://localhost:19003/api/schema/swagger-ui/)

---

## 📌 Comandos Úteis

* `pdm run dev` – Executa o servidor local
* `pdm run migrate` – Gera e aplica as migrações do banco de dados
* `pdm run createsu` – Cria superusuário (se configurado no `pyproject.toml`)

---

## 📈 Melhorias Futuras

* [ ] Integração com gateway de pagamento Mercado Pago
* [ ] Envio de notificações por email
* [ ] Dashboard de administração com gráficos

---

## 📄 Licença

Distribuído sob licença [GPL](https://www.gnu.org/licenses/gpl-3.0.html).
