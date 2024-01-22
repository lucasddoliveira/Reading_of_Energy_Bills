# Leitura de Faturas de Energia (PT-BR)
Este projeto tem como objetivo compilar o histórico das unidades consumidoras, utilizando as informações contidas nas faturas de energia emitidas pela concessionária local, Energisa, na Paraíba, Brasil. Cada fatura contém uma tabela na segunda página, apresentando dados dos últimos 12 meses de consumo ativo, demanda ativa, consumo reativo e demanda reativa, tanto em períodos "ponta" quanto "fora de ponta". O script em Python foi desenvolvido para analisar arquivos no formato PDF, utilizando a tecnologia OCR Tesseract para extrair dados relevantes. Após a extração, as informações são processadas e exibidas por meio da biblioteca Pandas.

## Como Utilizar

Para utilizar este script, siga os passos abaixo:

1. **Instalação do Tesseract:**
   - Instale o Tesseract via [https://sourceforge.net/projects/tesseract-ocr.mirror/](https://sourceforge.net/projects/tesseract-ocr.mirror/).
   - Declare o caminho local do Tesseract no arquivo .py.

2. **Inserir Arquivos na Pasta "Faturas":**
   - Coloque os arquivos a serem processados na pasta denominada "Faturas". O programa opera de maneira cumulativa. Para construir um histórico mais abrangente, considere inserir duas ou mais faturas em meses distintos da mesma unidade consumidora.

3. **Instalar Dependências:**
   - Certifique-se de instalar todas as dependências necessárias.

4. **Execução:**
   - Execute o script para iniciar o processamento.

Em caso de dúvidas ou sugestões, sinta-se à vontade para contatar: [lucasddoliveira1@gmail.com](mailto:lucasddoliveira1@gmail.com).

## Resultados e Utilização

O dataframe resultante pode ser aproveitado de diversas maneiras, dependendo do seu objetivo. Pode ser utilizado para análise de dados, criação de dashboards ou qualquer outra aplicação desejada. Personalize e explore os resultados conforme suas necessidades.

![image](https://github.com/lucasddoliveira/Reading_of_Energy_Bills/assets/85253035/2c161857-1764-4846-a72a-1c61561211f9)
![image](https://github.com/lucasddoliveira/Reading_of_Energy_Bills/assets/85253035/65ef15ba-c873-4f15-b72c-ec4d96cea08b)
![image](https://github.com/lucasddoliveira/Reading_of_Energy_Bills/assets/85253035/258a3c49-759d-4ab4-85d4-7098367485ec)
![image](https://github.com/lucasddoliveira/Reading_of_Energy_Bills/assets/85253035/fff16d81-8e89-4a86-9497-1179652cced3)

# Energy Bill Reading (EN)
This project aims to compile the history of consumer units using the information contained in the energy bills issued by the local utility company, Energisa, in Paraíba, Brazil. Each bill contains a table on the second page, presenting data for the last 12 months of active consumption, active demand, reactive consumption, and reactive demand, both in "peak" and "off-peak" periods. The Python script was developed to analyze PDF files, using OCR Tesseract technology to extract relevant data. After extraction, the information is processed and displayed using the Pandas library.

## How to Use

To use this script, follow the steps below:

1. **Tesseract Installation:**
   - Install Tesseract via https://sourceforge.net/projects/tesseract-ocr.mirror/.
   - Declare the local path of Tesseract in the .py file.

2. **Insert Files in the "Faturas" Folder:**
   - Place the files to be processed in the folder named "Bills".
   - The program operates cumulatively. To build a more comprehensive history, consider inserting two or more bills in different months for the same consumer unit.
     
3. **Install Dependencies:**
   - Make sure to install all necessary dependencies.

4. **Execution:**
   - Run the script to initiate the processing.

For questions or suggestions, feel free to contact: [lucasddoliveira1@gmail.com](mailto:lucasddoliveira1@gmail.com).

## Results and Usage

The resulting dataframe can be utilized in various ways, depending on your objective. It can be used for data analysis, dashboard creation, or any other desired application. Customize and explore the results according to your needs.

![image](https://github.com/lucasddoliveira/Reading_of_Energy_Bills/assets/85253035/2c161857-1764-4846-a72a-1c61561211f9)
![image](https://github.com/lucasddoliveira/Reading_of_Energy_Bills/assets/85253035/65ef15ba-c873-4f15-b72c-ec4d96cea08b)
![image](https://github.com/lucasddoliveira/Reading_of_Energy_Bills/assets/85253035/258a3c49-759d-4ab4-85d4-7098367485ec)
![image](https://github.com/lucasddoliveira/Reading_of_Energy_Bills/assets/85253035/77026095-7c85-448b-9c32-be776e34619f)

