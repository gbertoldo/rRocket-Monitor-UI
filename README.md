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
- **Limpar**: limpa os registros de dados.
- **Gerar relatório**: cria uma listagem dos dados registrados. É possível gravar a listagem em arquivo de texto para análise posterior.
    
## Análise

A aba **Análise** permite comparar os dados do rRocket com aqueles obtidos pelo rRocket-Monitor. O gráfico apresentado nesta aba é semelhante ao da aba **Monitor**, exceto pelo fato que aqui são exibidos os dados do altímetro e do rRocket-Monitor.
<p align="center">
<img src="https://github.com/user-attachments/assets/97167212-8f0c-43a0-a38d-df028ecf2bbc">
</p>

Abaixo do gráfico há dois campos onde são informados os caminhos para os arquivos de texto com os dados do rRocket-Monitor e do rRocket. O primeiro arquivo é criado a partir do relatório gerado na aba [Monitor](#monitor). O segundo arquivo é gerado através da aba **Memória** no [rRocket-UI](https://github.com/gbertoldo/rRocket-UI).

Como não há sincronização nas medições do rRocket e do rRocket-Monitor, espera-se defasagem nos gráficos dos dados dos desses dispositivos. Para corrigir essa defasagem, o campo (dt) permite deslocar os dados do rRocket-Monitor com relação ao tempo a fim de que as curvas de altura coincidam. Esse ajuste pode ser feito automaticamente através do botão **Autoajustar**.   

No botão **Gerar relatório** é possível gerar uma listagem das informações da análise e gravar os dados em arquivo de texto para análise posterior.

## Procedimento de teste do rRocket

A figura abaixo apresenta dados coletados em um teste do rRocket.
<p align="center">
<img src="https://github.com/user-attachments/assets/55a9f53d-7b7d-4fd9-8d6a-01743717675a">
</p>

Para obter tais dados, utilizou-se o procedimento a seguir:
1. A memória de voo do rRocket foi apagada.
1. Os fios do rRocket-Monitor foram ligados ao rRocket.
1. O rRocket foi inserido na câmara do rRocket-Monitor.
1. Os terminais jacaré do rRocket-Monitor foram conectados a resistores de 1,5 ohms para simular ignitores.
1. O rRocket-Monitor foi [conectado](#conexão) a sua interface gráfica.
1. O rRocket foi ligado através do botão liga/desliga do rRocket-Monitor.
1. Na aba **Monitor** do rRocket-Monitor, clicou-se em *Iniciar* para dar início ao registro de dados.
1. O êmbolo da seringa do rRocket-Monitor foi movimentado manualmente de modo a tentar se obter uma curva de trajetória semelhante à de um voo real.
1. Clicou-se no botão *Parar* para interromper o registro de dados.
1. O rRocket foi desligado através do botão liga/desliga do rRocket-Monitor.
1. Clicou-se em *Gerar relatório* e a listagem de dados foi salva em arquivo de texto nomeado, arbitrariamente, como "rRocketMonitor.txt"

Há alguns pontos a se destacar com relação aos dados coletados:
1. Como esperado, observa-se através dos picos de tensão que o altímetro (rRocket) realizou três tentativas de acionamento do paraquedas auxiliar (Vdrogue) e três tentativas de acionamento do paraquedas principal (Vparaquedas).
1. Observa-se queda de tensão na bateria a cada tentativa de acionamento dos paraquedas. Baterias reais sofrem queda de tensão quando a demanda por corrente aumenta.
1. O paraquedas auxiliar (drogue) foi acionado antes do apogeu. Isso não representa um problema, pois a curva da trajetória foi gerada pela movimentação do êmbolo e não representa a dinâmica de um voo real. O paraquedas auxiliar é acionado quando a componente vertical da velocidade é zero. Ao analizar os dados do rRocket, observa-se que tal velocidade é nula justamente no instante em que o drogue foi acionado. 
1. O paraquedas auxiliar foi acionado na altura de 200 m, como esperado.


Na figura abaixo são exibidos os dados do rRocket e do rRocket-Monitor obtidos no teste mencionado acima.
<p align="center">
<img src="https://github.com/user-attachments/assets/2af57494-e6f8-4d4d-97f3-5cab29c3d5a0">
</p>

Observe que as curvas de altura são semelhantes, mas estão defasadas. Ao clicar em **Autoajustar**, os dados obtidos do rRocket-Monitor são deslocados no tempo para que as curvas coincidam, como demonstrado na figura abaixo.

<p align="center">
<img src="https://github.com/user-attachments/assets/efefe923-828e-4f9d-a32b-8dc1ecef6605">
</p>

No gráfico acima é possível observar que:
1. As trajetórias registradas por sensores independentes são praticamente idênticas.
1. O instante de acionamento do paraquedas auxiliar registrado pelo rRocket (D) coincide com o primeiro pico de tensão (Vdrogue) registrado pelo rRocket-Monitor.
1. O instante de acionamento do paraquedas principal registrado pelo rRocket (P) coincide com o primeiro pico de tensão (Vparaquedas) registrado pelo rRocket-Monitor.

