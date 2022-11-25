
    
    *** Roadmap/Ajustes minimos p/ data de entrega ***
    
    * possível refatoramento/abstração da base e do index/solicitacoes --> base c/ sidebar + content --> extend p/ --> base + logo c/ table que será usado p/ index e solicitacoes --ok
    * definir quais campos serão necessários para as tabelas do backend -- ok
    * construir todo o banco de dados e criar os métodos via sqlAlchemy -- ok
        -- templates de banco feita -- ok
        -- definir arquivo separado p/ templates de tables -- ok
    * setar .env p/ esconder informações sigilosas >:D -- ok
    * botar a index do Little Samuca p/ rodar (em cima da rota '/') -- ok
    * mudar aquele btn de delete do modal depois
    * preparar pull request pro pythonanywhere -- mais ou menos feito
    * utilização de scss p/ facilidade de utilização de styles -- ok
    * definir .aciive na pag selecionada -- ok
    * fazer tabelas aparecerem/desaparecerem de forma "graciosa" -- revisar
    * talvez margin-top no mobile (5vh) -- ok
    * ver forma de user current_user pra pegar o pharmacyId do user -- session resolveu :D
    * criar CRUD de pedidos e implementar req no front -- quase ok
    * aceitar pharm null no cadastro -- ok
    * login no mobile funcional -- ok
    * "notification is-danger"/flash reject login -- ok
    * add formatCurrency em estoque -- sem necessidade por enquanto
    * add data no /api/order -- ok

    *** LONGO PRAZO (sim, vai ter update nisso dps da entrega do trabalho >:D) ***
    
    separar req de API p/ fora do routes
    fazer "sanitização" de dados recebidos (já tem uma bem básica rodando)
    salvar hash da senha no banco; pegar no minimo 8 caracteres (c/ caractere especial e número)
    criar autenticação p/ certas requisições da API (mais ou menos feito, mas da pra melhorar)
    setar métodos da tabela recipe 
    ter relationships entre as tables de forma funcional
    flask session e flask login devem ter o mesmo lifetime (session = PERMANENT_SESSION_LIFETIME, f_login = REMEMBER_COOKIE_DURATION) -- ok (sou mt bom)
    possível refatoração do modo que os dados p/ modal de edit são pego
    armazenamento em cache de certos arquivos (pasta static inteira praticamente)

    criar dashboard de admin p/ visualização de user/req, etc
        -- tipo de user = "A"
        -- uma pag extra escondida (hehe)

