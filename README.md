# rRocket-Monitor-UI
Interface gráfica para o [rRocket-Monitor](https://github.com/gbertoldo/rRocket-Monitor)

# Versão
Versão 1.0.0

# Como usar
1. [Baixe](https://github.com/gbertoldo/rRocket-Monitor-UI/releases) a versão mais recente do executável (disponível apenas para Windows).
1. Não é necessário realizar instalações, basta rodar o arquivo executável. Se não houver erros, surgirá uma janela como ilustrado na figura abaixo:
<p align="center">
<img src="https://github.com/user-attachments/assets/d9c8a878-f264-4b62-bc95-1ba7f56be6de">
</p>

A janela da  interface gráfica está organizada em três abas, detalhadas a seguir.

## Conexão
Algumas das funcionalidades da interface gráfica são habilitadas apenas se o rRocket-Monitor estiver conectado. Para realizar a conexão:
1. Na aba **Conexão**, verifique as portas USB disponíveis, como ilustrado a seguir:
<p align="center">
<img src="https://github.com/user-attachments/assets/caaf5ef6-676d-477b-9f76-0eebcc7bc446" width=300>
</p> 

**Observação: a numeração das portas varia de um computador para outro.**

2. Conecte o rRocket-Monitor a uma porta USB do computador.
   
4. Clique no botão para atualizar a lista de portas USB disponíveis:
<p align="center">
<img src="https://github.com/user-attachments/assets/ef589657-1311-4361-aa65-6f988ca14d4d" width=50>.
</p>

4. Selecione a porta que apareceu após a conexão do rRocket-Monitor (passo 2).
<p align="center">
<img src="https://github.com/user-attachments/assets/1569bac2-ff04-4f5a-9920-1fe8743dad14">
</p>

5. Clique no botão **Conectar**. Se a conexão for bem sucedida, o ícone de _status_ de conexão mudará de vermelho para verde.

## Monitor
⚠️ As funcionalidades desta aba são habilitadas apenas se o rRocket-Monitor estiver conectado.

O espaço central da aba **Monitor** é ocupado pelo gráfico que exibe a altura registrada pelo barômetro BMP280 do rRocket-Monitor e das medidas de tensão nos terminais da bateria, do paraquedas auxiliar e do paraquedas principal. O gráfico possui dois eixos verticais: o da esquerda representa a altura e o da direita a tensão. 
<p align="center">
<img src="https://github.com/user-attachments/assets/a6840e08-8fc2-4dca-8574-b988f150927a">
</p>

Abaixo do gráfico há três botões:
- **Iniciar/Parar**: inicia/para o registro de dados enviados pelo rRocket-Monitor para a interface gráfica.
- **Limpar**: limpa o registro de dados.
- **Gerar relatório**: cria uma listagem dos dados registrados. É possível gravar a listagem em arquivo de texto para análise posterior.
    
## Análise

A aba **Análise** permite comparar os dados do rRocket com aqueles obtidos pelo rRocket-Monitor. O gráfico apresentado nesta aba é semelhante ao da aba **Monitor**, exceto pelo fato que aqui são exibidos os dados do altímetro e do rRocket-Monitor.
<p align="center">
<img src="https://github.com/user-attachments/assets/97167212-8f0c-43a0-a38d-df028ecf2bbc">
</p>

Abaixo do gráfico há dois campos onde são informados os caminhos para os arquivos de texto com os dados do rRocket-Monitor e do rRocket. O primeiro arquivo é criado a partir do relatório gerado na aba [Monitor](#monitor). O segundo arquivo é gerado através da aba **Memória** no [rRocket-UI](https://github.com/gbertoldo/rRocket-UI).

Como não há sincronização nas medições do rRocket e do rRocket-Monitor, espera-se defasagem nos gráficos dos dados dos dispositivos. Para corrigir essa defasagem, o campo (dt) permite deslocar os dados do rRocket-Monitor com relação ao tempo a fim de que as curvas de altura coincidam. Esse ajuste pode ser feito automaticamente através do botão **Autoajustar**.   

No botão **Gerar relatório** é possível gerar uma listagem das informações da análise e gravar os dados em arquivo de texto para análise posterior.

## Procedimento de teste do rRocket

O seguinte procedimento de teste deve ser aplicado antes do primeiro voo do rRocket:

1. Apagar a memória de voo do rRocket.
1. Ligar os fios do rRocket-Monitor ao rRocket.
1. Inserir o rRocket na câmara do rRocket-Monitor.
1. Conectar os terminais jacaré do rRocket-Monitor a resistores de 1,5 ohms para simular ignitores.
1. [Conectar](#conexão) o rRocket-Monitor a sua interface gráfica.
1. Ligar o rRocket através do botão liga/desliga do rRocket-Monitor.
1. Na aba **Monitor** do rRocket-Monitor, clicar em *Iniciar* para dar início ao registro de dados.
1. Mover o êmbolo da seringa do rRocket-Monitor  de modo a tentar se obter uma curva de trajetória semelhante à de um voo real.
1. Clicar no botão *Parar* para interromper o registro de dados.
1. Desligar o rRocket através do botão liga/desliga do rRocket-Monitor.
1. Clicar em *Gerar relatório* e salvar a listagem de dados. Para fins de demonstração, considere que o arquivo foi nomeado "rRocketMonitor.txt"

Antes de prosseguir, observe a figura abaixo, que apresenta dados coletados em um teste do rRocket utilizando os passos acima.
<p align="center">
<img src="https://github.com/user-attachments/assets/55a9f53d-7b7d-4fd9-8d6a-01743717675a">
</p>

Há alguns pontos a se destacar com relação aos dados coletados:

- Como esperado, observa-se através dos picos de tensão que o altímetro (rRocket) realizou três tentativas de acionamento do paraquedas auxiliar (Vdrogue) e três tentativas de acionamento do paraquedas principal (Vparaquedas).
- Observa-se queda de tensão na bateria a cada tentativa de acionamento dos paraquedas. Baterias reais sofrem queda de tensão quando a demanda por corrente aumenta.
- O paraquedas auxiliar (drogue) foi acionado antes do apogeu. Isso não representa um problema, pois a curva da trajetória foi gerada pela movimentação do êmbolo e não representa a dinâmica de um voo real. O paraquedas auxiliar é acionado quando a componente vertical da velocidade é zero. Ao analizar os dados do rRocket, observa-se que tal velocidade é nula justamente no instante em que o drogue foi acionado. 
- O paraquedas auxiliar foi acionado na altura de 200 m, como esperado.

Para continuar com o teste, os seguintes passos devem ser executados:

12. Desconectar o rRocket do rRocket-Monitor;
1. Acessar a memória do rRocket utilizando sua interface gráfica, o [rRocket-UI](https://github.com/gbertoldo/rRocket-UI).
1. Gerar o relatório da memória de voo e salvá-lo em arquivo. Para fins de demonstração, considere que o arquivo foi nomeado "rRocket.txt"
1. De volta ao rRocket-Monitor, na aba **Análise**, carreguar os arquivos "rRocketMonitor.txt" e "rRocket.txt".
1. Clicar em **Autoajustar** para remover a defasagem de tempo entre os dados.

As figuras abaixo exibidem os dados do rRocket e do rRocket-Monitor obtidos no exemplo de teste mencionado acima antes e depois de se realizar o autoajuste, respectivamente.
<p align="center">
<img src="https://github.com/user-attachments/assets/2af57494-e6f8-4d4d-97f3-5cab29c3d5a0">
</p>

<p align="center">
<img src="https://github.com/user-attachments/assets/efefe923-828e-4f9d-a32b-8dc1ecef6605">
</p>
Para completar o teste deve-se:

17. Repetir os passos 1 a 16, substituindo os resistores de 1,5 ohms do passo 4 por ignitores (squibs).

Para que o rRocket seja aprovado neste teste, é necessário que:
1. O desvio das trajetórias registradas pelo rRocket e pelo rRocket-Monitor estejam dentro da margem de erro ( $\pm 2$ m).
1. O instante de acionamento do paraquedas auxiliar registrado pelo rRocket (D) deve coincidir com o primeiro pico de tensão (Vdrogue) registrado pelo rRocket-Monitor.
1. O instante de acionamento do paraquedas principal registrado pelo rRocket (P) deve coincidir com o primeiro pico de tensão (Vparaquedas) registrado pelo rRocket-Monitor.
1. Os ignitores elétricos (squibs) devem ser acionados corretamente.
