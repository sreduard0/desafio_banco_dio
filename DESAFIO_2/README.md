O aplicativo permite que os usuários façam login, realizem saques, depósitos, visualizem o extrato da conta e façam logout. Os dados dos usuários e suas contas são armazenados em arquivos JSON.

Ao iniciar o aplicativo, o usuário é apresentado a um menu inicial com opções para fazer login, se cadastrar ou sair do aplicativo. Se o usuário escolher fazer login, ele deverá fornecer seu login e senha. Se as informações forem válidas, ele será autenticado e poderá acessar as funcionalidades do banco.

Após o login bem-sucedido, o usuário é redirecionado para um menu principal, onde pode escolher entre sacar dinheiro, depositar dinheiro, visualizar o extrato da conta ou sair do aplicativo. Dependendo da opção selecionada, a ação correspondente é executada.

Ao fazer um saque, o usuário pode inserir o valor desejado. O aplicativo verifica se o valor é válido e se o saldo da conta é suficiente. Também é verificado se o usuário já realizou o máximo de saques permitidos para o dia.

Ao fazer um depósito, o usuário pode inserir o valor a ser depositado. O valor é adicionado ao saldo da conta.

Ao visualizar o extrato da conta, o usuário pode ver todas as transações realizadas, incluindo a data, o valor e o tipo de transação (saque ou depósito).

O usuário pode fazer logout a qualquer momento, retornando ao menu inicial.

O código é escrito de forma modular, com funções separadas para cada funcionalidade, facilitando a leitura e a manutenção.
