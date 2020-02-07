# Aplicação MES  
 
## Tech

- Usando somente Python para desenvolvimento, tanto nos engines como na GUI (Feita com Tkinter);
- Usa lib Pandas para analise dos dados e classificação dos dados seguindo regras para ordenar a fila de produtos de acordo com o melhor setup possível;
- Armazena os dados localmente em SQlite para poder trabalhar offline;
- Instalado em Raspberry Pi para uso de telas touchscreen para facilidade no manuseio;
- Também foi usado Raspberry Pi pois futuramente a ideia é usar os GPIO da Raspberry pi para comunicar diretamente com os equipamentos e captar dados de produção com sensores e usar atuadores para liberar/bloquear equipamentos;


## Geral  
 
- Sistema para controle de produção fabril. 
- Comunica em tempo real com banco de dados Firebird do ERP da fábrica
- Pesca a cada 1 minuto as demandas para cada equipamento onde este sistema está instalado;
- Capaz de trabalhar offline;
- Interface desenhada para touchscreen;
- Imprime etiqueta de produção diretamente a partir de impressora térmica ligada ao Raspberry Pi


## Solução REAL

Sistema atualmente me produção na Datateck Chicotes Elétricos em Guaíba.
