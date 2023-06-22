# MPSPD

Script em python 3 que faz download recursivo das imagens de usuários.

O nome MPSPD remete a 
-__MP__ - site que fazemos o download das imagens
-**SPD** - de speed, pois a primeira versão feita era linear e fazia que o teste ficasse muito mais lento que o atual, que roda em multi threading

## Requisitos
Esse script roda em python 3e foi testado em Mac OS e Linux. Adaptaçõs podem ser necessárias para rodar em todos os sisteas operacionais

O código usa algumas bibliotecas de python, entào caso necessa'rio, instale aquilo que for necessário, conforme erros na execução. Nesse primeiro momento vou manter para quem entende um pouco de python. As bibliotecas podem ser instaladas com o **PIP**

Claro, você precisa de acesso a internet e principalmente uma conta no **MP** para poder referencias a URL da imagem base.

## Como Funciona?

O site do **MP** salva todas as imagens de usuários em um sistema de CDN e respeita uma lógica para gerar o endereço das otos para cada perfil, como no exemplo abaixo:

https://images.meupatrocinio.com/12511238/14882708/15/

Com esse exemplo posso explicar como é feita a composição da URL para que possamos entender como o script atua e ter uma melhor experiência. 

### images.meupatrocinio.com
Aqui é o dominio do servidor onde estão as imagens. Não precisamos no preocuar com esse parametro, pois só precisamos dele para encontrar o servidor. Não é alterado durante a execução do script

### profileid - 12511238
O próximo parametro é o **profile id**, que um ID do perfil do usuário. É aqui que podemos identificar o perfil dono dessa foto, acessando como no modelo abaixo em seu navegador preferico

https://app.meupatrocinio.com/main/profile/**PROFILEID**/

No exemplo ficaria
https://app.meupatrocinio.com/main/profile/12511238/

### photoid - 14882708
Aqui que comena a inteligencia desenvolvida na engenharia reversa do sistema. Cada vez que o usuário sobre uma foto, essa foto tem um **photoid** único. Duas fotos não podem ter o mesmo **photoid** 
Se eu dubir 2 fotos ao mesmo tempo em um perfil novo, o sistema pega o último **photoid** livre e associa a primeira foto e gera um novo **photoid**, incrementalmente para a segunda foto

### photonumber - 15
Aqui é a sequencia da foto no perfil. Nesse exemplo podemos dizer que o número 15 nos diz que essa é a foto que foi subida pelo sistema pelo décima quinta vez. Mas já perceb que essa regra pode ser inválida em alguns casos, prvavelmente por algum erro do sistema do MP, que pode gerar um número repetido quando se realiza o upload. 

### O que o script faz?
O script tenta, atravez de uma URL de referencia de uma foto existente, tentar fazer o download da URL. Caso exista uma foto nesse endereço, ele salva no diretório de execução e incremente ou decrementa os valores de photoid e photonumber para uma nova tentativa em loop, realizando uma recursividade.

## Instalação

Copie o arquivo **mpspd.py** para uma pasta e execute conforme os paramtros necessários

## Como Usar

Eu sugiro que você crie uma pasta para cada perfil do **MP** com o nome do usuário que você vai puxar a imagem. Se o usuário, por exemplo, se chama _Maria_, crie uma pasta _Maria_ e copie para dentro dessa pasta o script **mpspd.py**.

Via terminal, acesse essa pasta com o comando **cd**

Acesse o perfil da pessoa que você quer puxar as fotos em su navegador preferido

Com o perfil aberto, você tem as *thumbs* de todas as fotos. Copie o endereço de uma foto. Sugiro que você em vez de ara todas as fotos do perfil em abas diferentes para poder identificar quais "buracos" existem nas mídias de photonumber e depois abrir cada aba, copiar  URL para executar o comando.

A URLs das photos podem vir assim:

- https://images.meupatrocinio.com/12511238/14882708/15/width=480,height=480
- https://images.meupatrocinio.com/12511238/14882708/15/width=800,height=800
- https://images.meupatrocinio.com/12511238/14882708/15/

No terminal, já dentro da pasta criada par ao script, execute:

python3 mpspd.py [URL da foto] {-1}

Você só vai colocar o -1 ao final caso deseje que o script decremente as URLs, senão deixe sem esse número.

Exemplo:

**_python3 mpspd.py https://images.meupatrocinio.com/12511238/14882708/15/width=480,height=480_**
No primeiro exemplo, o arquivo 15_14882708_14882708.jpeg é salvo e o script vai procurar o arquivo 16

**_python3 mpspd.py https://images.meupatrocinio.com/12511238/14882708/15/width=480,height=480_ -1**
Já no segundo, o mesmo arquivo é salvo e o script vai procurar o arquivo 14 na sequencia.


