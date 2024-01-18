from pdf2image import convert_from_path
import os
from PIL import Image as PILImage
import numpy as np
import pytesseract
import pandas as pd
import pygsheets
import datetime

st = datetime.datetime.now()
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

current_directory = os.getcwd()
diretorio = os.path.join(current_directory, 'Faturas')
poppler = os.path.join(current_directory, 'poppler-23.11.0\\Library\\bin')

def transform_coordinates(cell_coordinates):
    transformed_array = []

    for row in cell_coordinates:
        row_tuples = []
        for pair in row:
            row_tuples.extend(pair)
        transformed_array.append(tuple(row_tuples))

    return transformed_array

def cleanDB(df):
    df = df.drop_duplicates(subset=[
        'UC', 
        'MES', 
        'CONSUMO KWH PONTA', 
        'CONSUMO KWH FORA PONTA', 
        'CONSUMO REATIVO PONTA', 
        'CONSUMO REATIVO FORA PONTA', 
        'DEMANDA REATIVO PONTA',
        'DEMANDA REATIVO FORA PONTA',
        'DEMANDA MEDIDA PONTA',
        'DEMANDA MEDIDA FORA PONTA'])
    
    duplicate_groups = df[df.duplicated(subset=['UC', 'MES'], keep=False)].groupby(['UC', 'MES'])

    for group_name, group_df in duplicate_groups:
        non_zero_values_value1 = group_df[group_df['CONSUMO KWH PONTA'] != '0,00']
        non_zero_values_value2 = group_df[group_df['CONSUMO KWH FORA PONTA'] != '0,00']
        non_zero_values_value3 = group_df[group_df['CONSUMO REATIVO PONTA'] != '0,00']
        non_zero_values_value4 = group_df[group_df['CONSUMO REATIVO FORA PONTA'] != '0,00']
        non_zero_values_value5 = group_df[group_df['DEMANDA REATIVO PONTA'] != '0,00']
        non_zero_values_value6 = group_df[group_df['DEMANDA REATIVO FORA PONTA'] != '0,00']
        non_zero_values_value7 = group_df[group_df['DEMANDA MEDIDA PONTA'] != '0,00']
        non_zero_values_value8 = group_df[group_df['DEMANDA MEDIDA FORA PONTA'] != '0,00']
        
        if not non_zero_values_value1.empty:
            first_item_value1 = non_zero_values_value1['CONSUMO KWH PONTA'].iloc[0]
            df.loc[group_df.index, 'CONSUMO KWH PONTA'] = first_item_value1

        if not non_zero_values_value2.empty:
            first_item_value2 = non_zero_values_value2['CONSUMO KWH FORA PONTA'].iloc[0]
            df.loc[group_df.index, 'CONSUMO KWH FORA PONTA'] = first_item_value2

        if not non_zero_values_value3.empty:
            first_item_value3 = non_zero_values_value3['CONSUMO REATIVO PONTA'].iloc[0]
            df.loc[group_df.index, 'CONSUMO REATIVO PONTA'] = first_item_value3

        if not non_zero_values_value4.empty:
            first_item_value4 = non_zero_values_value4['CONSUMO REATIVO FORA PONTA'].iloc[0]
            df.loc[group_df.index,'CONSUMO REATIVO FORA PONTA'] = first_item_value4

        if not non_zero_values_value5.empty:
            first_item_value5 = non_zero_values_value5['DEMANDA REATIVO PONTA'].iloc[0]
            df.loc[group_df.index, 'DEMANDA REATIVO PONTA'] = first_item_value5

        if not non_zero_values_value6.empty:
            first_item_value6 = non_zero_values_value6['DEMANDA REATIVO FORA PONTA'].iloc[0]
            df.loc[group_df.index, 'DEMANDA REATIVO FORA PONTA'] = first_item_value6

        if not non_zero_values_value7.empty:
            first_item_value7 = non_zero_values_value7['DEMANDA MEDIDA PONTA'].iloc[0]
            df.loc[group_df.index, 'DEMANDA MEDIDA PONTA'] = first_item_value7

        if not non_zero_values_value8.empty:
            first_item_value8 = non_zero_values_value8['DEMANDA MEDIDA FORA PONTA'].iloc[0]
            df.loc[group_df.index, 'DEMANDA MEDIDA FORA PONTA'] = first_item_value8
    
    df = df.drop_duplicates(subset=[
        'UC', 
        'MES', 
        'CONSUMO KWH PONTA', 
        'CONSUMO KWH FORA PONTA', 
        'CONSUMO REATIVO PONTA', 
        'CONSUMO REATIVO FORA PONTA', 
        'DEMANDA REATIVO PONTA',
        'DEMANDA REATIVO FORA PONTA',
        'DEMANDA MEDIDA PONTA',
        'DEMANDA MEDIDA FORA PONTA'])

    return df

def process_second_page(path, uc, nome_arquivo):
    
    pages = convert_from_path(os.path.join(path, nome_arquivo), 500, poppler_path=poppler)
    
    if len(pages) >= 2:  # Ensure there are at least two pages in the PDF
        page = pages[1]  # Process the second page (index 1)
        
        # Convert the page to a numpy array
        page_np = np.array(page)
        
        try:
            # Crop the region of interest (ROI)
            cropped = page_np[1200:1885, 1080:3300]
            
            # Convert the cropped array to a PIL image
            result_image = PILImage.fromarray(cropped)

            #result_image.save("cropped_image1.png")

            
            cell_coordinates = [

                #SEGUNDA LINHA
                [(12, 65), (177, 118)],
                [(180, 65), (427, 118)],
                [(434, 65), (630, 118)],
                [(636, 65), (823, 118)],
                [(835, 65), (1073, 118)],
                [(1084, 65), (1303, 118)],
                [(1308, 65), (1526, 118)],
                [(1534, 65), (1752, 118)],
                [(1759, 65), (1955, 118)],
                [(1964, 65), (2200, 118)],

                #TERCEIRA LINHA
                [(12, 118), (177, 160)],
                [(180, 118), (427, 160)],
                [(434, 118), (630, 160)],
                [(636, 118), (823, 160)],
                [(835, 118), (1073, 160)],
                [(1084, 118), (1303, 160)],
                [(1308, 118), (1526, 160)],
                [(1534, 118), (1752, 160)],
                [(1759, 118), (1955, 160)],
                [(1964, 118), (2200, 160)],

                #QUARTA LINHA
                [(12, 160), (177, 205)],
                [(180, 160), (427, 205)],
                [(434, 160), (630, 205)],
                [(636, 160), (823, 205)],
                [(835, 160), (1073, 205)],
                [(1084, 160), (1303, 205)],
                [(1308, 160), (1526, 205)],
                [(1534, 160), (1752, 205)],
                [(1759, 160), (1955, 205)],
                [(1964, 160), (2200, 205)],

                #QUINTA LINHA
                [(12, 205), (177, 248)],
                [(180, 205), (427, 248)],
                [(434, 205), (630, 248)],
                [(636, 205), (823, 248)],
                [(835, 205), (1073, 248)],
                [(1084, 205), (1303, 248)],
                [(1308, 205), (1526, 248)],
                [(1534, 205), (1752, 248)],
                [(1759, 205), (1955, 248)],
                [(1964, 205), (2200, 248)],

                #SEXTA LINHA
                [(12, 248), (177, 296)],
                [(180, 248), (427, 296)],
                [(434, 248), (630, 296)],
                [(636, 248), (823, 296)],
                [(835, 248), (1073, 296)],
                [(1084, 248), (1303, 296)],
                [(1308, 248), (1526, 296)],
                [(1534, 248), (1752, 296)],
                [(1759, 248), (1955, 296)],
                [(1964, 248), (2200, 296)],

                #SETIMA LINHA
                [(12, 296), (177, 340)],
                [(180, 296), (427, 340)],
                [(434, 296), (630, 340)],
                [(636, 296), (823, 340)],
                [(835, 296), (1073, 340)],
                [(1084, 296), (1303, 340)],
                [(1308, 296), (1526, 340)],
                [(1534, 296), (1752, 340)],
                [(1759, 296), (1955, 340)],
                [(1964, 296), (2200, 340)],

                #OITAVA LINHA
                [(12, 340), (177, 383)],
                [(180, 340), (427, 383)],
                [(434, 340), (630, 383)],
                [(636, 340), (823, 383)],
                [(835, 340), (1073, 383)],
                [(1084, 340), (1303, 383)],
                [(1308, 340), (1526, 383)],
                [(1534, 340), (1752, 383)],
                [(1759, 340), (1955, 383)],
                [(1964, 340), (2200, 383)],

                #NONA LINHA
                [(12, 383), (177, 433)],
                [(180, 383), (427, 433)],
                [(434, 383), (630, 433)],
                [(636, 383), (823, 433)],
                [(835, 383), (1073, 433)],
                [(1084, 383), (1303, 433)],
                [(1308, 383), (1526, 433)],
                [(1534, 383), (1752, 433)],
                [(1759, 383), (1955, 433)],
                [(1964, 383), (2200, 433)],

                #DECIMA LINHA
                [(12, 433), (177, 483)],
                [(180, 433), (427, 483)],
                [(434, 433), (630, 483)],
                [(636, 433), (823, 483)],
                [(835, 433), (1073, 483)],
                [(1084, 433), (1303, 483)],
                [(1308, 433), (1526, 483)],
                [(1534, 433), (1752, 483)],
                [(1759, 433), (1955, 483)],
                [(1964, 433), (2200, 483)],

                #DECIMA PRIMEIRA LINHA
                [(12, 483), (177, 528)],
                [(180, 483), (427, 528)],
                [(434, 483), (630, 528)],
                [(636, 483), (823, 528)],
                [(835, 483), (1073, 528)],
                [(1084, 483), (1303, 528)],
                [(1308, 483), (1526, 528)],
                [(1534, 483), (1752, 528)],
                [(1759, 483), (1955, 528)],
                [(1964, 483), (2200, 528)],

                #DECIMA SEGUNDA LINHA
                [(12, 528), (177, 574)],
                [(180, 528), (427, 574)],
                [(434, 528), (630, 574)],
                [(636, 528), (823, 574)],
                [(835, 528), (1073, 574)],
                [(1084, 528), (1303, 574)],
                [(1308, 528), (1526, 574)],
                [(1534, 528), (1752, 574)],
                [(1759, 528), (1955, 574)],
                [(1964, 528), (2200, 574)],

                #DECIMA SEGUNDA LINHA
                [(12, 574), (177, 618)],
                [(180, 574), (427, 618)],
                [(434, 574), (630, 618)],
                [(636, 574), (823, 618)],
                [(835, 574), (1073, 618)],
                [(1084, 574), (1303, 618)],
                [(1308, 574), (1526, 618)],
                [(1534, 574), (1752, 618)],
                [(1759, 574), (1955, 618)],
                [(1964, 574), (2200, 618)],

                #DECIMA TERCEIRA LINHA
                [(12, 618), (177, 665)],
                [(180, 618), (427, 665)],
                [(434, 618), (630, 665)],
                [(636, 618), (823, 665)],
                [(835, 618), (1073, 665)],
                [(1084, 618), (1303, 665)],
                [(1308, 618), (1526, 665)],
                [(1534, 618), (1752, 665)],
                [(1759, 618), (1955, 665)],
                [(1964, 618), (2200, 665)],
                # Add more cell coordinates as needed...
            ]
            
            #draw = ImageDraw.Draw(result_image)
            #for i in cell_coordinates:
            #    draw.rectangle(i, outline='black', width=3)

            # Saving the cropped image
            #result_image.save("cropped_image1.png")
            
            
            '''LINHAS E COLUNAS '''
            '''
            draw = ImageDraw.Draw(result_image)
            line_thickness = 3  # Thickness5 of the black lines
            line_positions = [111,152, 197, 240, 286, 332, 376, 425, 470, 520, 565, 610, 655]  # Positions for the black lines
            column_positions = [150, 400,605, 800, 1050, 1275, 1500, 1725, 1930]

            for y in line_positions:
                y = y - 35
                draw.line((19, y, 2150, y), fill='black', width=line_thickness)
            for x in column_positions:
                x = x + 30
                draw.line((x, 30, x, 670), fill='black', width=line_thickness)
            '''      
            ''''
            draw.text((70, 38), text[0], fill=text_color, font=font)
            draw.text((290, 38), text[1], fill=text_color, font=font)
            draw.text((530, 38), text[2], fill=text_color, font=font)
            draw.text((750, 38), text[3], fill=text_color, font=font)
            draw.text((960, 38), text[4], fill=text_color, font=font)
            draw.text((1170, 38), text[5], fill=text_color, font=font)
            draw.text((1400, 38), text[6], fill=text_color, font=font)
            draw.text((1610, 38), text[7], fill=text_color, font=font)
            draw.text((1830, 38), text[8], fill=text_color, font=font)
            draw.text((2050, 38), text[9], fill=text_color, font=font)
            '''
            
            result_image = result_image.convert('L') 
            #result_image.save(os.path.join(path, f"{nome_arquivo.lower().replace('.pdf', '.jpg')}"), 'JPEG')

            cell_coordinates_to_crop = transform_coordinates(cell_coordinates)
            
            content = []

            for i in cell_coordinates_to_crop:
                cropped_region = result_image.crop(i)  
                
                text = pytesseract.image_to_string(cropped_region)
                
                modified_text = text.replace('\n', '')
                modified_text = modified_text.replace(' ', '')
                modified_text = modified_text.replace('.', '')
                modified_text = modified_text.replace('*', '')

                has_numeric = lambda string: any(char.isdigit() for char in string)

                if(modified_text==''):
                    modified_text='0,00'
                #print(modified_text)
                if (modified_text[-3] != ',' and '/' not in modified_text):
                    modified_text =  modified_text[:-2] + ',' + modified_text[-2:]

                content.append(modified_text)
        except:
            cropped = page_np[1430:2115, 1130:3350]
            
            # Convert the cropped array to a PIL image
            result_image = PILImage.fromarray(cropped)

            cell_coordinates = [

                #SEGUNDA LINHA
                [(5, 65), (177, 115)],
                [(180, 65), (427, 115)],
                [(434, 65), (635, 115)],
                [(636, 65), (823, 115)],
                [(831, 65), (1073, 115)],
                [(1084, 65), (1303, 115)],
                [(1308, 65), (1526, 115)],
                [(1534, 65), (1752, 115)],
                [(1769, 65), (1970, 115)],
                [(1973, 65), (2205, 115)],

                #TERCEIRA LINHA
                [(5, 118), (177, 160)],
                [(180, 115), (427, 160)],
                [(434, 115), (635, 160)],
                [(636, 115), (823, 160)],
                [(831, 115), (1073, 160)],
                [(1084, 115), (1303, 160)],
                [(1308, 115), (1526, 160)],
                [(1534, 115), (1752, 160)],
                [(1769, 115), (1970, 160)],
                [(1973, 115), (2205, 160)],

                #QUARTA LINHA
                [(5, 160), (177, 208)],
                [(180, 160), (427, 208)],
                [(434, 160), (635, 208)],
                [(636, 160), (823, 208)],
                [(831, 160), (1073, 208)],
                [(1084, 160), (1303, 208)],
                [(1308, 160), (1526, 208)],
                [(1534, 160), (1752, 208)],
                [(1769, 160), (1970, 208)],
                [(1973, 160), (2205, 208)],

                #QUINTA LINHA
                [(5, 208), (177, 256)],
                [(180, 208), (427, 256)],
                [(434, 208), (635, 256)],
                [(636, 208), (823, 256)],
                [(831, 208), (1073, 256)],
                [(1084, 208), (1303, 256)],
                [(1308, 208), (1526, 256)],
                [(1534, 208), (1752, 256)],
                [(1769, 208), (1970, 256)],
                [(1973, 208), (2205, 256)],

                #SEXTA LINHA
                [(5, 256), (177, 300)],
                [(180, 256), (427, 300)],
                [(434, 256), (635, 300)],
                [(636, 256), (823, 300)],
                [(831, 256), (1073, 300)],
                [(1084, 256), (1303, 300)],
                [(1308, 256), (1526, 300)],
                [(1534, 256), (1752, 300)],
                [(1769, 256), (1970, 300)],
                [(1973, 256), (2205, 300)],

                #SETIMA LINHA
                [(5, 300), (177, 347)],
                [(180, 300), (427, 347)],
                [(434, 300), (635, 347)],
                [(636, 300), (823, 347)],
                [(831, 300), (1073, 347)],
                [(1084, 300), (1303, 347)],
                [(1308, 300), (1526, 347)],
                [(1534, 300), (1752, 347)],
                [(1769, 300), (1970, 347)],
                [(1973, 300), (2205, 347)],

                #OITAVA LINHA
                [(5, 347), (177, 394)],
                [(180, 347), (427, 394)],
                [(434, 347), (635, 394)],
                [(636, 347), (823, 394)],
                [(831, 347), (1073, 394)],
                [(1084, 347), (1303, 394)],
                [(1308, 347), (1526, 394)],
                [(1534, 347), (1752, 394)],
                [(1769, 347), (1970, 394)],
                [(1973, 347), (2205, 394)],

                #NONA LINHA
                [(5, 394), (177, 442)],
                [(180, 394), (427, 442)],
                [(434, 394), (635, 442)],
                [(636, 394), (823, 442)],
                [(831, 394), (1073, 442)],
                [(1084, 394), (1303, 442)],
                [(1308, 394), (1526, 442)],
                [(1534, 394), (1752, 442)],
                [(1769, 394), (1970, 442)],
                [(1973, 394), (2205, 442)],

                #DECIMA LINHA
                [(5, 442), (177, 492)],
                [(180, 442), (427, 492)],
                [(434, 442), (635, 492)],
                [(636, 442), (823, 492)],
                [(831, 442), (1073, 492)],
                [(1084, 442), (1303, 492)],
                [(1308, 442), (1526, 492)],
                [(1534, 442), (1752, 492)],
                [(1769, 442), (1970, 492)],
                [(1973, 442), (2205, 492)],

                #DECIMA PRIMEIRA LINHA
                [(5, 492), (177, 538)],
                [(180, 492), (427, 538)],
                [(434, 492), (635, 538)],
                [(636, 492), (823, 538)],
                [(831, 492), (1073, 538)],
                [(1084, 492), (1303, 538)],
                [(1308, 492), (1526, 538)],
                [(1534, 492), (1752, 538)],
                [(1769, 492), (1970, 538)],
                [(1973, 492), (2205, 538)],

                #DECIMA SEGUNDA LINHA
                [(5, 538), (177, 587)],
                [(180, 538), (427, 587)],
                [(434, 538), (635, 587)],
                [(636, 538), (823, 587)],
                [(831, 538), (1073, 587)],
                [(1084, 538), (1303, 587)],
                [(1308, 538), (1526, 587)],
                [(1534, 538), (1752, 587)],
                [(1769, 538), (1970, 587)],
                [(1973, 538), (2205, 587)],

                #DECIMA SEGUNDA LINHA
                [(5, 587), (177, 631)],
                [(180, 587), (427, 631)],
                [(434, 587), (635, 631)],
                [(636, 587), (823, 631)],
                [(831, 587), (1073, 631)],
                [(1084, 587), (1303, 631)],
                [(1308, 587), (1526, 631)],
                [(1534, 587), (1752, 631)],
                [(1769, 587), (1970, 631)],
                [(1973, 587), (2205, 631)],

                #DECIMA TERCEIRA LINHA
                [(5, 631), (177, 676)],
                [(180, 631), (427, 676)],
                [(434, 631), (635, 676)],
                [(636, 631), (823, 676)],
                [(831, 631), (1073, 676)],
                [(1084, 631), (1303, 676)],
                [(1308, 631), (1526, 676)],
                [(1534, 631), (1752, 676)],
                [(1769, 631), (1970, 676)],
                [(1973, 631), (2205, 676)],
                # Add more cell coordinates as needed...
            ]
            
            '''LINHAS E COLUNAS '''
            '''
            draw = ImageDraw.Draw(result_image)
            line_thickness = 3  # Thickness5 of the black lines
            line_positions = [111,152, 197, 240, 286, 332, 376, 425, 470, 520, 565, 610, 655]  # Positions for the black lines
            column_positions = [150, 400,605, 800, 1050, 1275, 1500, 1725, 1930]

            for y in line_positions:
                y = y - 35
                draw.line((19, y, 2150, y), fill='black', width=line_thickness)
            for x in column_positions:
                x = x + 30
                draw.line((x, 30, x, 670), fill='black', width=line_thickness)
            '''      
            ''''
            draw.text((70, 38), text[0], fill=text_color, font=font)
            draw.text((290, 38), text[1], fill=text_color, font=font)
            draw.text((530, 38), text[2], fill=text_color, font=font)
            draw.text((750, 38), text[3], fill=text_color, font=font)
            draw.text((960, 38), text[4], fill=text_color, font=font)
            draw.text((1170, 38), text[5], fill=text_color, font=font)
            draw.text((1400, 38), text[6], fill=text_color, font=font)
            draw.text((1610, 38), text[7], fill=text_color, font=font)
            draw.text((1830, 38), text[8], fill=text_color, font=font)
            draw.text((2050, 38), text[9], fill=text_color, font=font)
            '''
            
            result_image = result_image.convert('L') 
            #result_image.save(os.path.join(path, f"{nome_arquivo.lower().replace('.pdf', '.jpg')}"), 'JPEG')

            cell_coordinates_to_crop = transform_coordinates(cell_coordinates)
            
            content = []

            for i in cell_coordinates_to_crop:
                cropped_region = result_image.crop(i)  
                
                text = pytesseract.image_to_string(cropped_region)
                
                modified_text = text.replace('\n', '')
                modified_text = modified_text.replace(' ', '')
                modified_text = modified_text.replace('.', '')
                modified_text = modified_text.replace('*', '')

                has_numeric = lambda string: any(char.isdigit() for char in string)

                if(modified_text==''):
                    modified_text='0,00'

                if (modified_text[-3] != ',' and '/' not in modified_text):
                    modified_text =  modified_text[:-2] + ',' + modified_text[-2:]

                content.append(modified_text)
        
        content_reshaped = np.reshape(content, (13, 10))

        fatura = pd.DataFrame(content_reshaped)
        fatura.columns = ["MES","CONSUMO KWH PONTA", "DEMANDA MEDIDA PONTA","X","CONSUMO KWH FORA PONTA","DEMANDA MEDIDA FORA PONTA","CONSUMO REATIVO PONTA","DEMANDA REATIVO PONTA","CONSUMO REATIVO FORA PONTA","DEMANDA REATIVO FORA PONTA"]
        fatura = fatura.drop('X', axis=1)

        fatura['UC'] = uc
        fatura['ARQUIVO'] = nome_arquivo

        fatura = fatura[['ARQUIVO', 'UC', 'MES','CONSUMO KWH PONTA','CONSUMO KWH FORA PONTA','CONSUMO REATIVO PONTA','CONSUMO REATIVO FORA PONTA','DEMANDA REATIVO PONTA','DEMANDA REATIVO FORA PONTA','DEMANDA MEDIDA PONTA','DEMANDA MEDIDA FORA PONTA']]
        #print(fatura)
        return fatura

def write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
    """
    this function takes data_df and writes it under spreadsheet_id
    and sheet_name using your credentials under service_file_path
    """
    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)
    wks_write.clear('A1',None,'*')
    wks_write.set_dataframe(data_df, (1,1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1

def findUC(nome_fatura):

    primeiro_indice = next((i for i, c in enumerate(nome_fatura) if c.isdigit() and c != '0'), None)
    posicao_substring = -2
    if nome_fatura.find('2023')>0:
        posicao_substring = nome_fatura.find('2023')
    elif nome_fatura.find('2024')>0:
        posicao_substring = nome_fatura.find('2024')
    elif nome_fatura.find('2025')>0:
        posicao_substring = nome_fatura.find('2025')
    

    if primeiro_indice is not None:
        matricula = nome_fatura[primeiro_indice:posicao_substring-2]

    return int(matricula)

def iterateOnBills(diretorio):

    tabela = {
    'ARQUIVO': [],
    'UC': [],
    'MES': [],#

    'CONSUMO KWH PONTA': [],
    'CONSUMO KWH FORA PONTA': [],

    'CONSUMO REATIVO PONTA': [],
    'CONSUMO REATIVO FORA PONTA': [],

    'DEMANDA REATIVO PONTA': [],
    'DEMANDA REATIVO FORA PONTA': [],

    'DEMANDA MEDIDA PONTA': [],
    'DEMANDA MEDIDA FORA PONTA': []
}
    df = pd.DataFrame(tabela)
   
    for nome_arquivo in os.listdir(diretorio): 
            if ((nome_arquivo.endswith('.pdf') or nome_arquivo.endswith('.PDF'))):
                nome_fatura = nome_arquivo
                nome_arquivo = diretorio +"\\"+ nome_arquivo
                print("************  LENDO O ARQUIVO: " + nome_fatura)

                matricula = findUC(nome_fatura)

                if (matricula):
                        processamento = process_second_page(diretorio, matricula, nome_fatura)
                        df = pd.concat([df, processamento], ignore_index=True)
                        
    
    processed_df = cleanDB(df)
    
    print(processed_df)
    
    et = datetime.datetime.now()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')

iterateOnBills(diretorio)